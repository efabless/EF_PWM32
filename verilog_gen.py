class Port:
    def __init__(self, dir, name, type, size, value=""):
        self.name = name
        self.dir = dir
        self.type = type
        self.size = size
        self.value = value

    def assign(self, value):
        self.value = value
        return self

    def print(self):
        if self.size > 1:
            range = f"[{self.size -1}:0]"
        else:
            range = "\t"
        print(f"\t{self.dir}\t{self.type}{range}\t{self.name}", end="")
    
    def print_assign(self):
        if self.value != "":
            print(f"\tassign\t{self.name} = {self.value};")
    
    
class Wire:
    def __init__(self, name, size, value=""):
        self.name = name
        self.size = size
        self.value = value
        
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
        value = ""
        self.init = ""
        self.clk = ""
        self.rst = ""
        self.clk_pol = 1
        self.rst_pol = 1
        
    def always(self, clk, rst, init, value):
        self.value = value
        self.rst = rst
        self.init = init
        self.clk = clk
        return self
        
    def clk_pol(self, pol):
        self.clk_pol = pol
        return self
        
    def set_rst_pol(self, pol):
        self.rst_pol = pol
        return self

    def set_set_init(self, init):
        self.init = init
        return self
        
    def print_def(self):
        if self.size > 1:
            range = f"[{self.size -1}:0]"
        else:
            range = "\t"
        print(f"\treg\t{range}\t{self.name};");
        
    def print_always(self):
        if self.clk_pol == 0:
            clk_edge = "negedge"
        else:
            clk_edge = "posedge"

        if self.rst_pol == 0:
            rst_edge = "negedge"
        else:
            rst_edge = "posedge"

        print(f"\talways @ ({clk_edge} {self.clk} or {rst_edge} {self.rst})")
        rst_value = f"1'b{self.rst_pol}"
        print(f"\t\tif({self.rst} == {rst_value})")
        print(f"\t\t\t{self.name} <= {self.init};")
        print(f"\t\telse")
        print(f"\t\t\t{self.name} <= {self.value};")
        

class LocalParam:
    def __init__(self, name, size, value):
        self.name = name
        self.size = size 
        self.value = value

    def print(self):
        v = self.value
        hs = int(self.size/4)
        print(f"\tlocalparam[{self.size-1}:0] {self.name} = {self.size}'h" + f"{v:#0{hs}}" + ";")

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

    def add_port(self, port):
        self.ports.append(port)
         
    def add_wire(self, wire):
        self.wires.append(wire)

    def add_reg(self, reg):
        self.regs.append(reg)
      
    def add_localparam(self, p):
        self.localparams.append(p)

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
        print("")

    def print_footer(self):
        print("\nendmodule")

    def print_wires(self):
        for w in self.wires:
            w.print()
        print("")

    def print_regs(self):
        for r in self.regs:
            r.print_def()
            r.print_always()
        print("")

    def print_localparams(self):
        for lp in self.localparams:
            lp.print()
        print("")

    def print_muxes(self):
        for m in self.muxes:
            m.print()
        print("")
    
    def print_ports_assign(self):
        for p in self.ports:
            p.print_assign()
        print("")