import math
from bus import BUS

class COMP:
    def __init__(self):
        self.name = ""
        self.module = ""
        self.module_postfix = ""
        self.pins = []
        self.registers = []

    def print_header(self):
        #nm = self.module
        #if len(self.module_postfix) > 0:
        #    nm = self.module + f"_{self.module_postfix}"
        print(f"\t{self.module} {self.name} (")

    def print_pins(self, i):
        e = 0
        for p in self.pins:
            (name, dir, sz) = p
            if dir != 2:
                print(f"\t\t.{name}({self.name}_{name})", end="")
            else:
                print(f"\t\t.{name}_in({self.name}_{name}_in),")
                print(f"\t\t.{name}_out({self.name}_{name}_out),")
                print(f"\t\t.{name}_outen({self.name}_{name}_outen)", end="")
            e = e + 1
            if e < len(self.pins):
                print(",")
            else:
                print("")

class SLAVE(COMP):
    def __init__(self):
        super().__init__()
        self.bus_type = BUS.AHBL

    def set_bus_type(self, bus_type):
        self.bus_type = bus_type

    def check_bus_type(self, bus):
        if bus not in BUS.BUS_TYPEs:
            raise Exception("Unsupported bus type for the slave")

class MASTER(COMP):
    def __init__(self):
        super().__init__()
        self.space = 0x10000000
    def get_num_addr_lines(self):
        return int(math.log2(self.space))
