from bus import *
from comp import *
from verilog_gen import *
import math


class AHBL(BUS):
    def __init__(self, name, base=0, num_pages=8):
        super().__init__(name=name, type=BUS.AHBL, base=base, num_pages=num_pages)
        self.mod = Module(self.name)

    def add_ports(self):
        self.mod.add_port(Port(dir="input", name="HCLK", type="wire", size=1))
        self.mod.add_port(Port(dir="input", name="HRESETn", type="wire", size=1))
        self.mod.add_port(Port(dir="input", name="HADDR", type="wire", size=32))
        self.mod.add_port(Port(dir="input", name="HWDATA", type="wire", size=32))
        self.mod.add_port(Port(dir="input", name="HWRITE", type="wire", size=1))
        self.mod.add_port(Port(dir="input", name="HTRANS", type="wire", size=2))
        self.mod.add_port(Port(dir="input", name="HSIZE", type="wire", size=3))
        self.mod.add_port(Port(dir="output", name="HRDATA", type="wire", size=32))
        self.mod.add_port(Port(dir="output", name="HREADY", type="wire", size=1))

    def gen_bus_dec(self):
        i = 0
        ns = len(self.slaves)
        n = int(math.log2(self.num_pages))
        p_f = 32 - n
        p_t = 31
        self.mod.add_wire(Wire(name="page", size=n, value=f"HADDR[{p_t}:{p_f}]"))
        self.mod.add_reg(Reg(name="apage", size=n).set_rst_pol(pol=0).always(clk="HCLK", rst="HRESETn", init="0", value="page"))
        for s in self.slaves:
            (slave, page, num) = s
            self.mod.add_localparam(LocalParam(name=f"S{str(i)}_PAGE", size=n, value=page ))
            i = i + 1

    def gen_bus_mux(self):
        dmux = Mux(name="HRDATA", sel="apage", default="32'hdead_beef")
        rmux = Mux(name="HREADY", sel="apage", default="1")
        i = 0
        for s in self.slaves:
            dmux.add_case(sel_value=f"S{i}_PAGE", value=f"HRDATA_S{i}")
            rmux.add_case(sel_value=f"S{i}_PAGE", value=f"HREADY_S{i}")
            i = i + 1
        dmux.print()
        rmux.print()
        
    def gen_slave_instances(self):
        i = 0;
        for slave in self.slaves:
            (s,p,n) = slave
            s.gen_inst(n)
            i = i + 1

    def gen_bus_logic(self):
        self.add_ports()
        i = 0
        for s in self.slaves:
            (slave, page, num) = s
            w = Wire(name="HSEL_S"+str(i), size=1)
            w.assign(f"HSEL & (page == S{i}_PAGE)")
            self.mod.add_wire(w)
            self.mod.add_wire(Wire(name="HREADY_S"+str(i), size=1))
            self.mod.add_wire(Wire(name="HRDATA_S"+str(i), size=32))
            for p in slave.pins:
                (name, d, s) = p
                dir = "output"
                if d == 1:
                    dir = "input"
                elif d == 2:
                    dir = "inout"
                if d != 2:
                    self.mod.add_port(Port(name=f"{slave.name}_{name}", dir=dir, type="wire", size=s))
                else:
                    self.mod.add_port(Port(name=f"{slave.name}_{name}_in", dir="input", type="wire", size=s))
                    self.mod.add_port(Port(name=f"{slave.name}_{name}_out", dir="output", type="wire", size=s))
                    self.mod.add_port(Port(name=f"{slave.name}_{name}_outen", dir="output", type="wire", size=s))
            i=i+1
        
        self.gen_bus_dec()
        self.mod.print_header()
        self.mod.print_localparams()
        self.mod.print_wires()
        self.mod.print_regs()
        self.gen_bus_mux()
        self.mod.print_ports_assign()
        self.gen_slave_instances()
        self.mod.print_footer()

'''
    APB Class
'''
class APB(BUS):
    type = BUS.AHBL

    def __init__(self, name, base=0, num_pages=8): 
        super().__init__(name=name, type=BUS.APB, base=base, num_pages=num_pages)
        self.mod = Module(self.name)
               
    def add_ports(self):
        self.mod.add_port(Port(dir="input", name="PCLK", type="wire", size=1))
        self.mod.add_port(Port(dir="input", name="PRESETn", type="wire", size=1))
        self.mod.add_port(Port(dir="input", name="PADDR", type="wire", size=int(math.log2(self.space))))
        self.mod.add_port(Port(dir="input", name="PWDATA", type="wire", size=32))
        self.mod.add_port(Port(dir="input", name="PWRITE", type="wire", size=1))
        self.mod.add_port(Port(dir="output", name="PRDATA", type="wire", size=32))
        self.mod.add_port(Port(dir="output", name="PREADY", type="wire", size=1))
        self.mod.add_port(Port(dir="input", name="PENABLE", type="wire", size=1)) 

    def gen_bus_dec(self):
        i = 0
        ns = len(self.slaves)
        n = int(math.log2(self.num_pages))
        m = int(math.log2(self.space))
        p_f = m - n
        p_t = m - 1
        self.mod.add_wire(Wire(name="page", size=n, value=f"PADDR[{p_t}:{p_f}]"))
        #self.mod.add_reg(Reg(name="apage", size=n).set_rst_pol(pol=0).always(clk="HCLK", rst="HRESETn", init="0", value="page"))
        for s in self.slaves:
            (slave, page, num) = s
            self.mod.add_localparam(LocalParam(name=f"S{str(i)}_PAGE", size=n, value=page ))
            i = i + 1
    
    def gen_bus_mux(self):
        dmux = Mux(name="PRDATA", sel="page", default="32'hdead_beef")
        rmux = Mux(name="PREADY", sel="page", default="1")
        i = 0
        for s in self.slaves:
            dmux.add_case(sel_value=f"S{i}_PAGE", value=f"PRDATA_S{i}")
            rmux.add_case(sel_value=f"S{i}_PAGE", value=f"PREADY_S{i}")
        dmux.print()
        rmux.print()
    
    def gen_slave_instances(self):
        i = 0;
        for slave in self.slaves:
            (s,p,n) = slave
            #print(f"\t{s.module} {s.name} (")
            s.gen_inst(i)
            i = i + 1

    def gen_bus_logic(self):
        self.add_ports()
        i = 0
        for s in self.slaves:
            (slave, page, num) = s
            #print(f"====> {slave.name}")
            w = Wire(name="PSEL_S"+str(i), size=1)
            w.assign(f"PSEL & (page == S{i}_PAGE)")
            self.mod.add_wire(w)
            #self.mod.add_wire(Wire(name="PSEL_S"+str(i), size=1))
            self.mod.add_wire(Wire(name="PREADY_S"+str(i), size=1))
            self.mod.add_wire(Wire(name="PRDATA_S"+str(i), size=32))
            for p in slave.pins:
                (name, d, s) = p
                #print(f"+++ {name}")
                dir = "output"
                if d == 1:
                    dir = "input"
                elif d == 2:
                    dir = "inout"
                if d != 2:
                    self.mod.add_port(Port(name=f"{slave.name}_{name}", dir=dir, type="wire", size=s))
                else:
                    self.mod.add_port(Port(name=f"{slave.name}_{name}_in", dir="input", type="wire", size=s))
                    self.mod.add_port(Port(name=f"{slave.name}_{name}_out", dir="output", type="wire", size=s))
                    self.mod.add_port(Port(name=f"{slave.name}_{name}_outen", dir="output", type="wire", size=s))
            i=i+1

        self.gen_bus_dec()
        self.mod.print_header()
        self.mod.print_localparams()
        self.mod.print_wires()
        self.mod.print_regs()
        self.gen_bus_mux()
        self.mod.print_ports_assign()
        self.gen_slave_instances()
        self.mod.print_footer()

class AHBLSLAVE(SLAVE):
    def __init__(self):
        super().__init__()

    def print_bus_ifc(self, i):
        print(f"\t\t.HCLK(HCLK),")
        print(f"\t\t.HRESETn(HRESETn),")
        print(f"\t\t.HADDR(HADDR),")
        print(f"\t\t.HWDATA(HWDATA),")
        print(f"\t\t.HWRITE(HWRITE),")
        print(f"\t\t.HTRANS(HTRANS),")
        print(f"\t\t.HSIZE(HSIZE),")
        print(f"\t\t.HSEL(HSEL_S{i}),")
        print(f"\t\t.HREADY(HREADY_S{i}),")
        print(f"\t\t.HRDATA(HRDATA_S{i})", end="")

class APBSLAVE(SLAVE):
    def __init__(self):
        super().__init__()

    def print_bus_ifc(self, i):
        print(f"\t\t.PCLK(PCLK),")
        print(f"\t\t.PRESETn(PRESETn),")
        print(f"\t\t.PSEL(PSEL_S{i}),")
        print(f"\t\t.PADDR(PADDR[11:2]),")
        print(f"\t\t.PREADY(PREADY_S{i}),")
        print(f"\t\t.PWRITE(PWRITE),")
        print(f"\t\t.PWDATA(PWDATA),")
        print(f"\t\t.PRDATA(PRDATA_S{i}),")
        print(f"\t\t.PENABLE(PENABLE)", end="")

class AHBLMASTER(MASTER):
    def __init__(self):
        super().__init__()

    def print_bus_ifc(self):
        print(f"\t\t.HCLK(HCLK),")
        print(f"\t\t.HRESETn(HRESETn),")
        print(f"\t\t.HADDR(HADDR),")
        print(f"\t\t.HWDATA(HWDATA),")
        print(f"\t\t.HWRITE(HWRITE),")
        print(f"\t\t.HTRANS(HTRANS),")
        print(f"\t\t.HSIZE(HSIZE),")
        print(f"\t\t.HSEL(HSEL),")
        print(f"\t\t.HREADY(HREADY),")
        print(f"\t\t.HRDATA(HRDATA)", end="")


class APBMASTER(MASTER):
    def __init__(self):
        super().__init__()

    def print_bus_ifc(self):
        nal = self.get_num_addr_lines()
        print(f"\t\t.PCLKEN(PCLKEN)")
        print(f"\t\t.PCLK(PCLK),")
        print(f"\t\t.PRESETn(PRESETn),")
        print(f"\t\t.PADDR(PADDR[{nal-1}:0]),")
        print(f"\t\t.PSEL(PSEL),")
        print(f"\t\t.PWRITE(PWRITE),")
        print(f"\t\t.PWDATA(PWDATA[31:0]),")
        print(f"\t\t.PENABLE(PENABLE),")
        print(f"\t\t.PREADY(PREADY),")
        print(f"\t\t.PRDATA(PRDATA[31:0])")
        #print(f"\t\t.PSLVERR(1'b0)", end="")

class AHBL2APB(APBMASTER, AHBLSLAVE, BUSBRIDGE):
    def __init__(self, sbus, name):
        super().__init__()
        self.sbus = sbus
        self.name = name
        self.module = "AHBL2APB"
        
    def gen_inst(self, i):
        self.print_header()
        AHBLSLAVE.print_bus_ifc(self, i)
        print(",")
        APBMASTER.print_bus_ifc(self)
        if len(self.pins) > 0:
            print(",")
            self.print_pins(i)
        print("\t);")

    def set_space(self, space):
        self.space = space

class AHBL_MMUX:
    port0 = BUS(name="b0")
    port1 = BUS(name="b1")
    outport = BUS(name="b2")
    name = ""
    def __init__(self, name, port0, port1, outport):
        self.port0 = port0
        self.port1 = port1
        self.outport = outport
        self.name = name
    
    def print(self):
        print(self.name,": AHBL Master MUX (2x1)")
