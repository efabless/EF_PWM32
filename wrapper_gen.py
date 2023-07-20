import json
import sys

class Port:
    def __init__(self, dir, name, type, size):
        self.name = name
        self.dir = dir
        self.type = type
        self.size = size

    def print(self):
        if self.size > 1:
            range = f"[{self.size -1}:0]"
        else:
            range = ""
        print(f"\t{self.dir}\t{self.type}\t{range}\t{self.name}", end="")
    
    
class Wire:
    value = ""
    def __init__(self, name, size):
        self.name = name
        self.size = size
        
    def assign(self, value):
        self.value = value
        
    def print(self):
        if self.size > 1:
            range = f"[{self.size -1}:0]"
        else:
            range = ""
        if self.value == "":
            print(f"\twire\t{range}\t{self.name};");
        else:
            print(f"\twire\t{range}\t{self.name}\t= {self.value};");
        

class Reg:
    value = ""
    init = ""
    clk = ""
    rst = ""
    clk_pol = ""
    rst_pol = ""
    def __init__(self, name, size):
        self.name = name
        self.size = size
        
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
        
class Module:
    ports = []
    wires = []
    regs = []

    def __init__(self, name):
        self.name = name

    def add_port(self, port):
        self.ports.append(port)
         
    def add_wire(self, wire):
        self.wires.append(wire)

    def add_reg(self, reg):
        self.regs.append(reg)
      
    def print_header(self):
        print(f"module {self.name} (")
        for p in self.ports:
            p.print()
            if p == self.ports[-1]:
                print("\n);")
            else:
                print(",")

    #def add_assign(self, wire, value):


    def print_wires(self):
        for w in self.wires:
            w.print()

    def print_regs(self):
        for r in self.regs:
            r.print_def()

class IP:
    data = []
    regs = []
    wires = []
    def __init__(self, fname):
        with open(fname, 'r') as jfile:
            self.data = json.load(jfile)

    def get_interface(self):
        ports = []
        for i in self.data["interface"]:
            p = Port(i["dir"], i["name"], "wire", int(i["size"]))
            ports.append(p)
        return ports
    
    def parse(self):
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
                w = Wire(reg_name, int(r['size']))
                w.assign(f"{r['fields'][0]['port']}")
                self.wires.append(w)

            else:
                sys.exit(f"Invalid Register mode ({reg_name})")

                
    def get_regs(self):
        return self.regs
    
    def get_wires(self):
        return self.wires
    
    def get_name(self):
        return self.data["name"]
    
    def get_instance(self):
        inst = f"\t{self.data['name']} timer(\n"
        inst += f"\t\t.{self.data['clock']}(clk_i),\n"
        pol=""
        if self.data["reset"]["pol"] == "0":
            pol="~"
        inst += f"\t\t.{self.data['reset']['name']}({pol}rst_i),\n"
        
        for p in self.data["ports"]:
            inst += f"\t\t.{p['name']}({p['name']})" 
            if p == self.data["ports"][-1]:
                inst += "\n\t);\n"
            else:
                inst += ",\n"
        return inst

class WB_Wrapper:
    wrapper = Module("wb_wrapper")
    valid = Wire("wb_valid", 1)
    we = Wire("wb_we", 1)
    re = Wire("wb_re", 1)
    wr_sel = Wire("wb_byte_sel", 4)
    io_regs = []
    inst = ""
    front_matter = """
`timescale          1ns/1ns
`default_nettype    none

`define     WB_REG(name, init_value)    always @(posedge clk_i or posedge rst_i) if(rst_i) name <= init_value; else if(wb_we & (adr_i==``name``_ADDR)) name <= dat_i;
    """
    
    def __init__(self, name):
        self.wrapper.name = name
        self.wrapper.add_port(Port("input", "clk_i", "wire", 1));
        self.wrapper.add_port(Port("input", "rst_i", "wire", 1));
        self.wrapper.add_port(Port("input", "adr_i", "wire", 32));
        self.wrapper.add_port(Port("input", "dat_i", "wire", 32));
        self.wrapper.add_port(Port("output", "dat_o", "wire", 32));
        self.wrapper.add_port(Port("input", "sel_i", "wire", 4));
        self.wrapper.add_port(Port("input", "cyc_i", "wire", 1));
        self.wrapper.add_port(Port("input", "stb_i", "wire", 1));
        self.wrapper.add_port(Port("output", "ack_o", "wire", 1));
        self.wrapper.add_port(Port("input", "we_i", "wire", 1));
        
        self.valid.assign("cyc_i & stb_i")
        self.wrapper.add_wire(self.valid)
        self.we.assign("we_i & wb_valid")
        self.wrapper.add_wire(self.we)
        self.re.assign("~we_i & wb_valid")
        self.wrapper.add_wire(self.re)
        self.wr_sel.assign("sel_i & {4{wb_we}}")
        self.wrapper.add_wire(self.wr_sel)

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
        print(self.front_matter)
        self.wrapper.print_header()
        self.wrapper.print_regs()
        self.wrapper.print_wires()
        print(self.inst)
        for r in self.wrapper.regs:
            #print(r.name)
            #print(r["name"])
            #reg_name = f"{r['name'].upper()}_REG"
            print(f"\t`WB_REG({r.name}, {r.init})")
        print("endmodule")
        
timer = IP('../repo/ms_tmr32/ip.json')

w1 = WB_Wrapper(f"{timer.get_name()}_wb")
w1.add_interface(timer.get_interface())

timer.parse()
w1.add_regs(timer.get_regs())
w1.add_wires(timer.get_wires())
#print(timer.get_instance())
w1.set_instance(timer.get_instance())
#print(timer.get_regs())

#w1.add_io_regs(data["regs"])
w1.print()
