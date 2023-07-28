from amba import *
from iplib import *
from pysoc import *
from cuproj import *


class DUMMY(AHBLSLAVE, APBSLAVE):
    def __init__(self, name, bus_type=BUS.AHBL):
        super().__init__
        self.name = name
        self.module = "dummy_ahbl"
        self.supported_buses=[BUS.AHBL, BUS.APB]
        if not self.check_bus_type(bus_type):
            raise Exception("Unsupported bus type")
        self.bus_type = bus_type;
        self.pins = [("tx", 0, 1),("rx", 1, 1)]
        
    def gen_inst(self, i):
        self.print_header()
        if self.bus_type == BUS.AHBL:
            AHBLSLAVE.print_bus_ifc(self,i)
        else:
            APBSLAVE.print_bus_ifc(self,i)
        if len(self.pins) > 0:
            print(",")
            self.print_pins(i)
        print("\n\t);")
    
    def check_bus_type(self, bus_type):
        if bus_type not in self.supported_buses:
            return False
        else:
            return True

class DUMMY_CPU_AHB(CPU, AHBLMASTER):
    def __init__(self, name):
        if name not in self.SUPPORTED_CPU:
            raise Exception(f'Unsupported CPU: {name}')
        self.name = name
        self.ibus = BUS(name="")
        self.dbus = BUS(name="")
        self.module="dummy_cpu_ahb"

    def gen_inst(self):
        print(f"\t{self.name} cpu (")
        self.print_bus_ifc()
        print("\n\t);\n")
    
hs_bus = AHBL(name="mainbus", base=0, num_pages=256)
hs_bus.add_slave(slave=DUMMY(name="s0"), page=0x00)
hs_bus.add_slave(slave=DUMMY(name="s1"), page=0x02)

ls_bus = APB(name="pbus", base=0x40000000, num_pages=256)
ls_bus.add_slave(slave=DUMMY(name="s10", bus_type=BUS.APB),page = 0)

hs_bus.add_slave(slave=AHBL2APB(name="mainbus2pbus", sbus=ls_bus), page=0x40)

my_cpu = DUMMY_CPU_AHB(name="dummy_cpu_ahb")
my_cpu.set_bus(hs_bus)

my_soc = SOC(name="dummy_soc", cpu=my_cpu)
my_soc.add_comp(hs_bus)
#my_soc.add_comp(ls_bus)

hs_bus.gen_bus_logic()
ls_bus.gen_bus_logic()
my_soc.gen()
#my_cpu.gen_inst()

#my_soc.print()