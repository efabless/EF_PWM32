from bus import BUS

class CPU:
    SUPPORTED_CPU = ['vexLite', 'vexSmall', 'vexBig', "picoLite", "dummy_cpu_ahb"]
    def __init__(self, name):
        if name not in self.SUPPORTED_CPU:
            raise Exception(f'Unsupported CPU: {name}')
        self.name = name
        self.ibus = BUS(name="")
        self.dbus = BUS(name="")
        self.split_bus = 1
    
    def set_ibus(self, bus):
        self.ibus = bus

    def set_dbus(self, bus):
        self.dbus = bus

    def set_bus(self, bus):
        self.ibus = bus
        self.split_bus = 0

class SOC:
    def __init__(self, name, cpu):
        self.name = name
        self.cpu = cpu
        self.comps = []
        self.pins = []

    def add_comp(self, comp):
        self.comps.append(comp)
        for c in self.comps:
            #print(c)
            if hasattr(c, 'get_pins'):
                #print(c, "has pins")
                for p in c.get_pins():
                    self.pins.append(p)
                    
        #print("=====>", self.pins)
    def gen_ahbl_wires(self):
        print()
        #print("\twire\t\tHCLK;")
        #print("\twire\t\tHRSETn;")
        print("\twire\t\tHWRITE;")
        print("\twire\t\tHREADY;")
        print("\twire [ 2:0]\tHSIZE;")
        print("\twire [ 1:0]\tHTRANS;")
        print("\twire [31:0]\tHADDR;")
        print("\twire [31:0]\tHWDATA;")
        print("\twire [31:0]\tHRDATA;")
        print()

    def gen(self):
        dir = ""
        x = 0
        print(f"module {self.name}(")
        print("\tinput\twire\t\tHCLK,\n\tinput\twire\t\tHRESETn,")
        for p in self.pins:
            (s, nm, d, sz) = p
            if d == 0:
                dir = "output"
            else:
                dir = "input"
            print(f"\t{dir}\twire [{sz-1}:{0}]\t{s}_{nm}", end="")  
            if x == len(self.pins)-1:
                print()
            else:
                print(",")
            x = x + 1
        print(");")
        self.gen_ahbl_wires()
        self.cpu.gen_inst()
        self.cpu.ibus.gen_inst("hsbus")
        print("endmodule")

    def print(self):
        print("SoC : ", self.name)
        print("CPU : ", self.cpu.name)
        for c in self.comps:
            c.print()
