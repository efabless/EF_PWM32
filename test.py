from amba import *
from iplib import *
from pysoc import *
from cuproj import *


#my_tmr0 = EF_TMR32(name="S0", bus_type="ahbl")
#my_tmr1 = EF_TMR32(name="S2", bus_type="apb")
#my_bridge = AHBL2APB(sbus="", name="APB_BRIDGE")

#my_tmr0.gen_inst(0)#
#my_tmr1.gen_inst(2)
#my_bridge.gen_instance(1)


hs_bus = AHBL(name="mainbus", base=0, num_pages=256)
ls_bus0 = APB(name="pbus0", base=0x40000000, num_pages=16)
ls_bus1 = APB(name="pbus1", base=0x41000000, num_pages=16)
hs_bus.add_slave(slave=FLASH(name="flash", writer=True, lines=32), page=0x00)
hs_bus.add_slave(slave=SRAM(name="sram", type=SRAM.DFFRAM, size=1024), page=0x20)
hs_bus.add_slave(slave=PSRAM(name="psram"), page=0x21)
hs_bus.add_slave(slave=AHBL2APB(name="bridge2bus0", sbus=ls_bus0), page=0x4)
hs_bus.add_slave(slave=AHBL2APB(name="bridge2bus1", sbus=ls_bus1), page=0x41)

ls_bus0.add_slave(slave=EF_UART(name="uart0"), page=4)
ls_bus0.add_slave(slave=EF_UART(name="uart1"), page=6)
ls_bus0.add_slave(slave=EF_TMR32(name="tmr0"), page=7)
ls_bus0.add_slave(slave=EF_TMR32(name="tmr1"), page=8)
ls_bus0.add_slave(slave=EF_ADCC10(name="adc0"), page=0)


ls_bus1.add_slave(slave=EF_UART(name="uart2"), page=4)
ls_bus1.add_slave(slave=EF_TMR32(name="uart3"), page=6)
ls_bus1.add_slave(slave=EF_TMR32(name="tmr2"), page=7)
ls_bus1.add_slave(slave=EF_TMR32(name="tmr3"), page=8)

my_cpu = CPU(name="vexLite")
cpu_bus_mux = AHBL_MMUX(name="mmux", port0=my_cpu.dbus, port1=my_cpu.ibus, outport=hs_bus)
my_soc = SOC(name="raptor", cpu=my_cpu)
my_soc.add_comp(cpu_bus_mux)
my_soc.add_comp(hs_bus)
#my_soc.print()

#ahb_bus = AHBL(name="AHBL_BUS", type=BUS.AHBL, base=0, num_pages=16)
#hs_bus.gen_bus_logic()
#ls_bus0.gen_bus_logic()
#ls_bus1.gen_bus_logic()
#hs_bus.print()
#my_soc.print()

pinmap = [
    ('flash', 'sck', [10]),
    ('flash', 'csn', [11]),
    ('flash', 'io', [12, 13, 14, 15])
]

my_cup = CUPROJ(name="soc", type=CUPROJ.CARAVEL)
my_cup.add_design(design=my_soc, pinmap=pinmap)