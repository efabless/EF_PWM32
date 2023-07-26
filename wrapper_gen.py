import json
import sys
import os.path
import datetime
import math

class Port:
    def __init__(self, dir, name, type, size):
        self.name = name
        self.dir = dir
        self.type = type
        self.size = size

    def assign(self, value):
        self.value = value
        return self

    def print(self):
        if self.size > 1:
            range = f"[{self.size -1}:0]"
        else:
            range = "\t"
        print(f"\t{self.dir}\t{self.type} {range}\t{self.name}", end="")
    
    def print_assign(self):
        if self.value != "":
            print(f"\tassign\t{self.name} = {self.value};")
    
    
class Wire:
    
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.value = ""
        
    def assign(self, value):
        self.value = value
        
    def print(self):
        if self.size > 1:
            range = f"[{self.size -1}:0]"
        else:
            range = "\t"
        if self.value == "":
            print(f"\twire{range}\t{self.name};");
        else:
            print(f"\twire{range}\t{self.name}\t= {self.value};");
        

class Reg:
    
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.value = ""
        self.init = ""
        self.clk = ""
        self.rst = ""
        self.clk_pol = ""
        self.rst_pol = ""
            
    def always(self, clk, rst, init, value):
        self.value = value
        self.rst = rst
        self.init = init
        self.clk = clk
        
    def clk_pol(self, pol):
        self.clk_pol = pol
        
    def rst_pol(self, pol):
        self.rst_pol = pol

    def set_init(self, init):
        self.init = init
        
    def print_def(self):
        if self.size > 1:
            range = f"[{self.size -1}:0]"
        else:
            range = "\t"
        print(f"\treg\t{range}\t{self.name};");
        
    def print_always(self):
        print(f"\talways @ ({self.clk_pol} {self.clk} or {self.rst_pol} {self.rst})")
        if self.rst_pol == "negedge":
            rst_value = "1'b0"
        else:
            rst_value = "1'b1"
        print(f"\t\tif({self.rst} == {rst_value})")
        print(f"\t\t\t{self.name} <= {self.init};")
        print(f"\t\telse")
        print(f"\t\t\t{self.name} <= {self.value};")
        
class LocalParam:
    def __init__(self, name, size, value):
        self.name = name
        self.size = size 
        self.value = value

    def set_size(self, size):
        self.size = size
        return self

    def print(self):
        v = self.value
        hs = int(self.size/4)
        print(f"\tlocalparam[{self.size-1}:0] {self.name} = {self.size}'h" + f"{v:0{hs}x}" + ";")


class Mux:
    def __init__(self, name, sel, default="0"):
        self.name = name
        self.sel = sel
        self.default = default
        self.cases = []

    def add_case(self, sel_value, value):
        self.cases.append(tuple((sel_value, value)))

    def print(self):
        print(f"\tassign\t{self.name} = ")
        for c in self.cases:
            (sv,v) = c
            print(f"\t\t\t({self.sel} == {sv}) ? {v} :")
        print(f"\t\t\t{self.default};")

class Module:
    def __init__(self, name):
        self.name = name
        self.ports = []
        self.wires = []
        self.regs = []
        self.localparams = []
        self.muxes = []

    def add_localparam(self, p):
        self.localparams.append(p)

    def add_port(self, port):
        self.ports.append(port)
         
    def add_wire(self, wire):
        self.wires.append(wire)

    def add_reg(self, reg):
        self.regs.append(reg)

    def add_mux(self, m):
        self.muxes.append(m)
      
    def print_header(self):
        print(f"module {self.name} (")
        for p in self.ports:
            p.print()
            if p == self.ports[-1]:
                print("\n);")
            else:
                print(",")

    def print_wires(self):
        for w in self.wires:
            w.print()
        print("")

    def print_regs(self):
        for r in self.regs:
            r.print_def()
        print("")

    def print_localparams(self):
        for lp in self.localparams:
            lp.print()
        print("")
    
    def print_muxes(self):
        for m in self.muxes:
            m.print()
        print("")

class IP:
    def __init__(self, fname):
        self.data = []
        self.regs = []
        self.wires = []
        self.localparams = []

        with open(fname, 'r') as jfile:
            self.data = json.load(jfile)
        
        self.parse_regs()
        if self.has_flags():
            self.parse_flags()

    def get_interface(self):
        ports = []
        for i in self.data["interface"]:
            p = Port(i["dir"], i["name"], "wire", int(i["size"]))
            ports.append(p)
            if i["name"] != i["port"]:
                w = Wire(name=i["port"], size=int(i["size"]))
                w.assign(value=i["name"])
                self.wires.append(w)
        return ports
    
    def parse_regs(self):
        v = 0
        for r in self.data["regs"]:
            reg_name = f"{r['name'].upper()}_REG"
            if r["mode"] == "rw":
                reg = Reg(reg_name, int(r['size']))
                reg.set_init(r["init"])
                self.regs.append(reg)
                for f in r["fields"]:
                    wf = Wire(f['port'], int(f['size']))
                    wf.assign(f"{reg_name}[{int(f['from'])+int(f['size'])-1}:{f['from']}]")
                    self.wires.append(wf)
            elif r["mode"] == "ro":
                w = Wire(r['fields'][0]['port'], int(r['fields'][0]['size']))
                self.wires.append(w)
                w = Wire(reg_name, int(r['size']))
                w.assign(f"{r['fields'][0]['port']}")
                self.wires.append(w)
            else:
                sys.exit(f"Invalid Register mode ({reg_name})")
            self.localparams.append(LocalParam(name=f"{reg_name}_ADDR", size=16, value=v))
            v = v + 4
    
    def parse_flags(self):
        self.ris_value = ""
        i = 0
        sz = len(self.data["flags"])
        for flag in self.data["flags"]:
            w0 = Wire(name=flag["port"], size=1)
            w1 = Wire(name=f"_{flag['name'].upper()}_FLAG_", size=1)
            w1.assign(value=flag["port"])
            self.wires.append(w0)
            self.wires.append(w1)
            self.ris_value = self.ris_value + f"\t\t\tif(_{flag['name'].upper()}_FLAG_) RIS_REG[{i}] <= 1'b1; else if(ICR_REG[{i}]) RIS_REG[{i}] <= 1'b0;\n"
            i = i+ 1

        isr = Reg(name="RIS_REG", size=sz)
        icr = Reg(name="ICR_REG", size=sz)   
        im = Reg(name="IM_REG", size=sz)
        mis = Wire(name="MIS_REG", size=sz)
        mis.assign(value="RIS_REG & IM_REG")
        self.regs.append(isr)
        self.regs.append(icr)
        self.regs.append(im)
        self.wires.append(mis)

        

    def get_localparams(self):
        return self.localparams
    
    def get_regs(self):
        return self.regs
    
    def get_wires(self):
        return self.wires
    
    def get_name(self):
        return self.data["name"]
    
    def get_author(self):
        return self.data["author"]
    
    def get_license(self):
        return self.data["license"]

    def get_email(self):
        return self.data["email"]
    
    def has_flags(self):
        return "flags" in self.data
    
    def get_num_flags(self):
        return len(self.data["flags"])
    
    def get_ris_value(self):
        return self.ris_value
        
    def get_instance(self):
        inst = f"\t{self.data['name']} inst_to_wrap (\n"
        inst += f"\t\t.{self.data['clock']}(_clk_),\n"
        pol=""
        if self.data["reset"]["pol"] == "0":
            pol="~"
        inst += f"\t\t.{self.data['reset']['name']}({pol}_rst_),\n"
        
        for p in self.data["ports"]:
            inst += f"\t\t.{p['name']}({p['name']})" 
            if p == self.data["ports"][-1]:
                inst += "\n\t);\n"
            else:
                inst += ",\n"
        return inst
    

class Wrapper:
    def __init__(self, ip, page_size=math.pow(2,16)):
        self.ip = ip
        self.page_size = page_size
        self.wrapper = Module("wrapper")
        self.wrapper.name = f"{ip.get_name()}_wb"
        self.lic = ip.get_license()
        self.author = ip.get_author()
        self.email = ip.get_email()
        self._clk_ = Wire("_clk_", 1)
        self._rst_ = Wire("_rst_", 1)
        self.add_interface(ip.get_interface())
        self.add_regs(ip.get_regs())
        self.add_wires(ip.get_wires())
        self.set_instance(ip.get_instance())
        v = 0
        for lp in ip.get_localparams():
            self.wrapper.add_localparam(lp.set_size(int(math.log2(self.page_size))))
            v = v + 4
        if self.ip.has_flags:
            self.wrapper.add_localparam(LocalParam(name="ICR_REG_ADDR", size=int(math.log2(self.page_size)), value = 0xF00))
            self.wrapper.add_localparam(LocalParam(name="RIS_REG_ADDR", size=int(math.log2(self.page_size)), value = 0xF04))
            self.wrapper.add_localparam(LocalParam(name="IM_REG_ADDR", size=int(math.log2(self.page_size)), value = 0xF08))
            self.wrapper.add_localparam(LocalParam(name="MIS_REG_ADDR", size=int(math.log2(self.page_size)), value = 0xF0C))
        

    def print_front_matter(self):
        print("`timescale\t\t\t1ns/1ns")
        print("`default_nettype\tnone")

    def print_license(self):
        print(f"/*\n\tCopyright {datetime.date.today().year} {self.author}\n")

        if "MIT" in self.lic:
            print("\tPermission is hereby granted, free of charge, to any person obtaining")
            print("\ta copy of this software and associated documentation files (the")
            print("\t\"Software\"), to deal in the Software without restriction, including")
            print("\twithout limitation the rights to use, copy, modify, merge, publish,")
            print("\tdistribute, sublicense, and/or sell copies of the Software, and to")
            print("\tpermit persons to whom the Software is furnished to do so, subject to")
            print("\tthe following conditions:\n")

            print("\tThe above copyright notice and this permission notice shall be")
            print("\tincluded in all copies or substantial portions of the Software.\n")

            print("\tTHE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND,")
            print("\tEXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF")
            print("\tMERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND")
            print("\tNONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE")
            print("\tLIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION")
            print("\tOF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION")
            print("\tWITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.")
        elif "APACHE 2.0" in self.lic:
            print("\tLicensed under the Apache License, Version 2.0 (the \"License\");")
            print("\tyou may not use this file except in compliance with the License.")
            print("\tYou may obtain a copy of the License at\n")
            print("\t    http://www.apache.org/licenses/LICENSE-2.0\n")
            print("\tUnless required by applicable law or agreed to in writing, software")
            print("\tdistributed under the License is distributed on an \"AS IS\" BASIS,")
            print("\tWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.")
            print("\tSee the License for the specific language governing permissions and")
            print("\tlimitations under the License.")
        elif "BSD" in self.lic:
            print("\tRedistribution and use in source and binary forms, with or without modification,") 
            print("\tare permitted provided that the following conditions are met:\n")
            print("\t1. Redistributions of source code must retain the above copyright notice,") 
            print("\tthis list of conditions and the following disclaimer.\n")
            print(f"\tTHIS SOFTWARE IS PROVIDED BY {self.author} \“AS IS\” AND ANY EXPRESS OR ")
            print("\tIMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF ")
            print("\tMERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT ")
            print(f"\tSHALL {self.author} BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, ")
            print("\tSPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, ")
            print("\tPROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; ")
            print("\tOR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER ")
            print("\tIN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING ")
            print("\tIN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF ")
            print("\tSUCH DAMAGE.")
        print("\n*/\n\n")
    

    def add_interface(self, ports):
        for p in ports:
            self.wrapper.add_port(p)    

    def add_regs(self, regs):
        for r in regs:
            self.wrapper.add_reg(r)    

    def add_wires(self, wires):
        for w in wires:
            self.wrapper.add_wire(w)    
                    
    def set_instance(self, inst):
        self.inst = inst;

    def print(self):
        self.print_license()
        self.print_front_matter()
        self.wrapper.print_header()
        self.wrapper.print_localparams()
        if type(self) is AHBL_Wrapper:
            self.print_epilogue() 
        self.wrapper.print_regs()
        self.wrapper.print_wires()
        print(self.inst)

    def gen_driver(self):
        ip_nm = self.ip.data['name'].upper()
        self.print_license()
        print(f"#define {ip_nm}_BASE\t\t\t\t0x00000000\n")
        for p in self.ip.localparams:
            print(f"#define\t{ip_nm}_{p.name}\t\t({ip_nm}_BASE+{hex(p.value)})")
        print()
        for r in self.ip.data["regs"]:
            for f in r["fields"]:
                if int(f['size']) != 32:
                    print(f"#define {ip_nm}_{r['name'].upper()}_REG_{f['name'].upper()}\t\t{f['from']}")
                    print(f"#define {ip_nm}_{r['name'].upper()}_REG_{f['name'].upper()}_LEN\t{f['size']}")
                    

        print()
        for p in self.ip.localparams:
            print(f"volatile unsigned int * {ip_nm.lower()}_{p.name.lower()}\t= (volatile unsigned int *) {ip_nm}_{p.name};") 


class AHBL_Wrapper(Wrapper):
    valid = Wire("ahbl_valid", 1)
    we = Wire("ahbl_we", 1)
    re = Wire("ahbl_re", 1)

    def __init__(self, ip):
        super().__init__(ip)
        self.wrapper.name = f"{ip.get_name()}_ahbl"
        self.wrapper.add_port(Port("input", "HCLK", "wire", 1))
        self.wrapper.add_port(Port("input", "HRESETn", "wire", 1))
        self.wrapper.add_port(Port("input", "HADDR", "wire", 32))
        self.wrapper.add_port(Port("input", "HWRITE", "wire", 1))
        self.wrapper.add_port(Port("input", "HTRANS", "wire", 2))
        self.wrapper.add_port(Port("input", "HREADY", "wire", 1))
        self.wrapper.add_port(Port("input", "HSEL", "wire", 1))
        self.wrapper.add_port(Port("input", "HSIZE", "wire", 3))
        self.wrapper.add_port(Port("input", "HWDATA", "wire", 32))
        self.wrapper.add_port(Port("output", "HRDATA", "wire", 32))
        self.wrapper.add_port(Port("output", "HREADYOUT", "wire", 1))

        if ip.has_flags():
            self.wrapper.add_port(Port("output", "irq", "wire", 1).assign(value="|MIS_REG"))

        self.valid.assign("last_HSEL & last_HTRANS[1]")
        self.wrapper.add_wire(self.valid)
        self.we.assign("last_HWRITE & ahbl_valid")
        self.wrapper.add_wire(self.we)
        self.re.assign("~last_HWRITE & ahbl_valid")
        self.wrapper.add_wire(self.re)
        
        self._clk_.assign("HCLK")
        self.wrapper.add_wire(self._clk_)
        self._rst_.assign("~HRESETn")
        self.wrapper.add_wire(self._rst_)

        hrdata = Mux(name="HRDATA", sel="last_HADDR", default="32'hDEADBEEF")
        for r in self.wrapper.regs:
            hrdata.add_case(sel_value=r.name+"_ADDR", value=r.name)
        for w in self.wrapper.wires:
            if "_REG" in w.name:
                hrdata.add_case(sel_value=w.name+"_ADDR", value=w.name)
        self.wrapper.add_mux(hrdata)

    def print_epilogue(self):
        print("\treg             last_HSEL;")
        print("\treg [31:0]      last_HADDR;")
        print("\treg             last_HWRITE;")
        print("\treg [1:0]       last_HTRANS;\n") 
        print("\talways@ (posedge HCLK) begin")
        print("\t\tif(HREADY) begin")
        print("\t\t\tlast_HSEL       <= HSEL;")
        print("\t\t\tlast_HADDR      <= HADDR;")
        print("\t\t\tlast_HWRITE     <= HWRITE;")
        print("\t\t\tlast_HTRANS     <= HTRANS;")
        print("\t\tend")
        print("\tend\n")

    def print_front_matter(self):
        super().print_front_matter()
        print("\n`define\t\tAHB_BLOCK(name, init)\talways @(posedge HCLK or negedge HRESETn) if(~HRESETn) name <= init;")
        print("`define\t\tAHB_REG(name, init)\t\t`AHB_BLOCK(name, init) else if(ahbl_we & (last_HADDR==``name``_ADDR)) name <= HWDATA;")
        print("`define\t\tAHB_ICR(sz)\t\t\t\t`AHB_BLOCK(ICR_REG, sz'b0) else if(ahbl_we & (last_HADDR==ICR_REG_ADDR)) ICR_REG <= HWDATA; else ICR_REG <= sz'd0;\n")
        
    def print_ICR_REG(self):
        sz=self.ip.get_num_flags()
        print(f"\t`AHB_ICR({sz})")

    def print(self):
        super().print()
        for r in self.wrapper.regs:
            if r.name not in ["RIS_REG", "ICR_REG", "IM_REG"]:
                print(f"\t`AHB_REG({r.name}, {r.init})")
        
        if self.ip.has_flags():
            print()
            self.print_ICR_REG()
            print("\n\talways @(posedge HCLK or negedge HRESETn)")
            print("\t\tif(~HRESETn) RIS_REG <= 32'd0;")
            print("\t\telse begin")
            print(self.ip.get_ris_value())
            print("\t\tend\n")
            print("\tassign irq = |MIS_REG;\n")

        self.wrapper.print_muxes()

        print("\n\tassign HREADYOUT = 1'b1;\n")

        print("endmodule")
    
class APB_Wrapper(Wrapper):
    #wrapper = Module("apb_wrapper")
    valid = Wire("apb_valid", 1)
    we = Wire("apb_we", 1)
    re = Wire("apb_re", 1)

    def __init__(self, ip):
        super().__init__(ip)
        self.wrapper.name = f"{ip.get_name()}_apb"
        self.wrapper.add_port(Port("input", "PCLK", "wire", 1))
        self.wrapper.add_port(Port("input", "PRESETn", "wire", 1))
        self.wrapper.add_port(Port("input", "PADDR", "wire", 32))
        self.wrapper.add_port(Port("input", "PWRITE", "wire", 1))
        self.wrapper.add_port(Port("input", "PSEL", "wire", 1))
        self.wrapper.add_port(Port("input", "PENABLE", "wire", 1))
        self.wrapper.add_port(Port("input", "PWDATA", "wire", 32))
        self.wrapper.add_port(Port("output", "PRDATA", "wire", 32))
        self.wrapper.add_port(Port("output", "PREADY", "wire", 1))

        if ip.has_flags():
            self.wrapper.add_port(Port("output", "irq", "wire", 1).assign(value="|MIS_REG"))

        self.valid.assign("PSEL & PENABLE")
        self.wrapper.add_wire(self.valid)
        self.we.assign("PWRITE & apb_valid")
        self.wrapper.add_wire(self.we)
        self.re.assign("~PWRITE & apb_valid")
        self.wrapper.add_wire(self.re)
        
        self._clk_.assign("PCLK")
        self.wrapper.add_wire(self._clk_)
        self._rst_.assign("~PRESETn")
        self.wrapper.add_wire(self._rst_)

        prdata = Mux(name="PRDATA", sel="PADDR", default="32'hDEADBEEF")
        for r in self.wrapper.regs:
            prdata.add_case(sel_value=r.name+"_ADDR", value=r.name)
        for w in self.wrapper.wires:
            if "_REG" in w.name:
                prdata.add_case(sel_value=w.name+"_ADDR", value=w.name)
        self.wrapper.add_mux(prdata)
        
    def print_front_matter(self):
        super().print_front_matter()
        print("\n`define\t\tAPB_BLOCK(name, init)\talways @(posedge PCLK or negedge PRESETn) if(~PRESETn) name <= init;")
        print("`define\t\tAPB_REG(name, init)\t\t`APB_BLOCK(name, init) else if(apb_we & (PADDR==``name``_ADDR)) name <= PWDATA;")
        print("`define\t\tAPB_ICR(sz)\t\t\t\t`APB_BLOCK(ICR_REG, sz'b0) else if(apb_we & (PADDR==ICR_REG_ADDR)) ICR_REG <= PWDATA; else ICR_REG <= sz'd0;\n")
        
    def print_ICR_REG(self):
        sz=self.ip.get_num_flags()
        print(f"\t`APB_ICR({sz})")

    def print(self):
        super().print()
        for r in self.wrapper.regs:
            if r.name not in ["RIS_REG", "ICR_REG", "IM_REG"]:
                print(f"\t`APB_REG({r.name}, {r.init})")
        
        if self.ip.has_flags:
            print()
            self.print_ICR_REG()
            print("\n\talways @(posedge PCLK or negedge PRESETn)")
            print("\t\tif(~PRESETn) RIS_REG <= 32'd0;")
            print("\t\telse begin")
            print(self.ip.get_ris_value())
            print("\t\tend\n")
            print("\tassign irq = |MIS_REG;\n")

        self.wrapper.print_muxes()

        print("\n\tassign PREADY = 1'b1;\n")

        print("endmodule")

class WB_Wrapper(Wrapper):
    #wrapper = Module("wb_wrapper")
    valid = Wire("wb_valid", 1)
    we = Wire("wb_we", 1)
    re = Wire("wb_re", 1)
    wr_sel = Wire("wb_byte_sel", 4)
    #io_regs = []
    #inst = ""
    
    def __init__(self, ip):
        super().__init__(ip)
        self.wrapper.name = f"{ip.get_name()}_wb"
        self.wrapper.add_port(Port("input", "clk_i", "wire", 1));
        self.wrapper.add_port(Port("input", "rst_i", "wire", 1));
        self.wrapper.add_port(Port("input", "adr_i", "wire", 32));
        self.wrapper.add_port(Port("input", "dat_i", "wire", 32));
        self.wrapper.add_port(Port("output", "dat_o", "wire", 32));
        self.wrapper.add_port(Port("input", "sel_i", "wire", 4));
        self.wrapper.add_port(Port("input", "cyc_i", "wire", 1));
        self.wrapper.add_port(Port("input", "stb_i", "wire", 1));
        self.wrapper.add_port(Port("output", "ack_o", "reg", 1));
        self.wrapper.add_port(Port("input", "we_i", "wire", 1));

        if ip.has_flags():
            self.wrapper.add_port(Port("output", "irq", "wire", 1).assign(value="|MIS_REG"))
        
        self.valid.assign("cyc_i & stb_i")
        self.wrapper.add_wire(self.valid)
        self.we.assign("we_i & wb_valid")
        self.wrapper.add_wire(self.we)
        self.re.assign("~we_i & wb_valid")
        self.wrapper.add_wire(self.re)
        self.wr_sel.assign("sel_i & {4{wb_we}}")
        self.wrapper.add_wire(self.wr_sel)

        self._clk_.assign("clk_i")
        self.wrapper.add_wire(self._clk_)
        self._rst_.assign("rst_i")
        self.wrapper.add_wire(self._rst_)

        dat_o = Mux(name="dat_o", sel="adr_i", default="32'hDEADBEEF")
        for r in self.wrapper.regs:
            dat_o.add_case(sel_value=r.name+"_ADDR", value=r.name)
        for w in self.wrapper.wires:
            if "_REG" in w.name:
                dat_o.add_case(sel_value=w.name+"_ADDR", value=w.name)
        self.wrapper.add_mux(dat_o)
        
    def print_front_matter(self):
        super().print_front_matter()
        print("\n`define\t\tWB_BLOCK(name, init)\talways @(posedge clk_i or posedge rst_i) if(rst_i) name <= init;")
        print("`define\t\tWB_REG(name, init)\t\t`WB_BLOCK(name, init) else if(wb_we & (adr_i==``name``_ADDR)) name <= dat_i;")
        print("`define\t\tWB_ICR(sz)\t\t\t\t`WB_BLOCK(ICR_REG, sz'b0) else if(wb_we & (adr_i==ICR_REG_ADDR)) ICR_REG <= dat_i; else ICR_REG <= sz'd0;\n")
 
    def print_ICR_REG(self):
        sz=self.ip.get_num_flags()
        print(f"\t`WB_ICR({sz})")

    def print(self):
        super().print()
        print("\talways @ (posedge clk_i or posedge rst_i)")
        print("\t\tif(rst_i) ack_o <= 1'b0;")
        print("\t\telse")
        print("\t\t\tif(wb_valid & ~ack_o)")
        print("\t\t\t\tack_o <= 1'b1;")
        print("\t\t\telse\n\t\t\t\tack_o <= 1'b0;\n")

        for r in self.wrapper.regs:
            if r.name not in ["RIS_REG", "ICR_REG", "IM_REG"]:
                print(f"\t`WB_REG({r.name}, {r.init})")
        if self.ip.has_flags:
            print()
            self.print_ICR_REG()
            print("\n\talways @ (posedge clk_i or posedge rst_i)")
            print("\t\tif(rst_i) RIS_REG <= 32'd0;")
            print("\t\telse begin")
            print(self.ip.get_ris_value())
            print("\t\tend\n")
            print("\tassign irq = |MIS_REG;\n")

        self.wrapper.print_muxes()
        
        print("endmodule")
        
if len(sys.argv) < 3 or len(sys.argv) > 4:
    sys.exit("use: wrapper_gen.py ip.json [-drv] AHBL|APB|WB")

if len(sys.argv) == 3:
    bus = sys.argv[2]
else:
    bus = sys.argv[3]
    if sys.argv[2] != "-drv":
        sys.exit(f"Unsupported argument {sys.argv[2]}.\nuse: wrapper_gen.py ip.json [-drv] AHBL|APB|WB")

if bus not in ["AHBL", "WB", "APB"]:
    sys.exit(f"Unsupported bus type {sys.argv[2]}.\nuse: wrapper_gen.py ip.json [-drv] AHBL|APB|WB")

if not os.path.isfile(sys.argv[1]):
    sys.exit(f"File not found ({sys.argv[1]}).\nuse: wrapper_gen.py ip.json [-drv] AHBL|APB|WB")

ip = IP(sys.argv[1])

if bus == "WB":
    w = WB_Wrapper(ip)
elif bus == "AHBL":
    w = AHBL_Wrapper(ip)
elif bus == "APB":
    w = APB_Wrapper(ip)

if len(sys.argv) == 3:
    w.print()
else:
    w.gen_driver()
