import math
from amba import *

'''
    A Python library to generate SoCs
    Peripherals:
        - 8-bit SAR ADC + AMUX
        - 8-bit DAC
        - SPI Master
        - I2C Master
    - Every slave gets a num that startes with 0; need to do code cleanups to remove not used code/properties
    - Th epin is named after the instance name
'''
        


class FLASH(AHBLSLAVE):
    def __init__(self, name, writer=False, lines=16, bus_type=BUS.AHBL):
        super().__init__
        self.name = name
        self.writer = writer
        self.lines = lines
        self.module = "FLASH"
        #self.module_postfix = "AHBL"
        if not self.check_bus_type(bus_type):
            raise Exception("Unsupported bus type")
        self.bus_type = bus_type;
        self.pins = [("sck", 0, 1),("csn", 0, 1),("io", 2, 4)]
    
    def gen_inst(self, i):
        self.print_header()
        if self.bus_type == BUS.AHBL:
            AHBLSLAVE.print_bus_ifc(self,i)
        else:
            pass
        if len(self.pins) > 0:
            print(",")
            self.print_pins(i)
        print("\n\t);")
    
    def check_bus_type(self, bus_type):
        if bus_type != BUS.AHBL:
            return False
        else:
            return True

class SRAM(AHBLSLAVE):
    SRAM_TYPES = ["dffram", "openram"]
    SRAM_SIZES = [[512, 1024, 2048], [1024, 2048]]
    DFFRAM = 0
    OPENRAM = 1
    def __init__(self, name, type=0, size=1024, bus_type=BUS.AHBL):
        self.name = name
        self.check_bus_type(bus_type)
        self.bus_type = bus_type
        if type > len(self.SRAM_TYPES):
            raise Exception("Unsupported SRAM type")
        self.type = type
        if size not in self.SRAM_SIZES[self.type]:
            raise Exception("Unsupported SRAM size")
        self.size = size
        self.module = "SRAM"
        self.module_postfix = "AHBL"
        self.pins = []

    def gen_inst(self, i):
        self.print_header()
        if self.bus_type == BUS.AHBL:
            AHBLSLAVE.print_bus_ifc(self,i)
        elif self.bus_type == BUS.APB:
            APBSLAVE.print_bus_ifc(self, i)
        else:
            pass
        print("\n\t);")

class PSRAM(AHBLSLAVE):
    def __init__(self, name, bus_type=BUS.AHBL):
        self.name = name
        self.module = "PSRAM_CTRL"
        self.module_postfix = ""
        self.pins = [("sck", 0, 1),("csn", 0, 1),("io", 2, 4)]
        self.check_bus_type(bus_type)
        self.bus_type = bus_type;
    
    def gen_inst(self, i):
        self.print_header()
        if self.bus_type == BUS.AHBL:
            AHBLSLAVE.print_bus_ifc(self,i)
        elif self.bus_type == BUS.APB:
            APBSLAVE.print_bus_ifc(self, i)
        else:
            pass
        if len(self.pins) > 0:
            print(",")
            self.print_pins(i)
        print("\n\t);")

class EF_TMR32(AHBLSLAVE, APBSLAVE):
    def __init__(self, name, bus_type=BUS.AHBL):
        self.check_bus_type(bus_type)
        self.name = name
        self.bus_type = bus_type
        self.module = "EF_TMR32"
        self.module_postfix = ""
        self.pins = [("pwm", 0, 1),("cp", 1, 1)]
    
    def gen_inst(self, i):
        self.print_header()
        if self.bus_type == BUS.AHBL:
            AHBLSLAVE.print_bus_ifc(self,i)
        elif self.bus_type == BUS.APB:
            APBSLAVE.print_bus_ifc(self, i)
        else:
            pass
        if len(self.pins) > 0:
            print(",")
            self.print_pins(i)
        print("\n\t);")

class EF_UART(AHBLSLAVE, APBSLAVE):
    def __init__(self, name, bus_type=BUS.AHBL):
        self.name = name
        self.module = "EF_UART"
        self.module_postfix = ""
        self.pins = [("tx", 0, 1),("rx", 1, 1)]
        self.bus_type = bus_type;

    def gen_inst(self, i):
        self.print_header()
        if self.bus_type == BUS.AHBL:
            AHBLSLAVE.print_bus_ifc(self,i)
        elif self.bus_type == BUS.APB:
            APBSLAVE.print_bus_ifc(self, i)
        else:
            pass
        if len(self.pins) > 0:
            print(",")
            self.print_pins(i)
        print("\n\t);")

class EF_ADCS8(AHBLSLAVE, APBSLAVE):
    def __init__(self, name, bus_type=BUS.AHBL):
        self.name = name
        self.module = "EF_ADCS8"
        #self.module_postfix = ""
        self.pins = [("Ain", 3, 1)]      # 3 means Analog!
        self.bus_type = bus_type;

    def gen_inst(self, i):
        self.print_header()
        if self.bus_type == BUS.AHBL:
            AHBLSLAVE.print_bus_ifc(self,i)
        elif self.bus_type == BUS.APB:
            APBSLAVE.print_bus_ifc(self, i)
        else:
            pass
        if len(self.pins) > 0:
            print(",")
            self.print_pins(i)
        print("\n\t);")

class EF_ADCC10(AHBLSLAVE, APBSLAVE):
    def __init__(self, name, bus_type=BUS.AHBL):
        self.name = name
        self.module = "EF_ADCC10"
        #self.module_postfix = ""
        self.pins = [("Ain", 3, 1)]      # 3 means Analog!
        self.bus_type = bus_type;

    def gen_inst(self, i):
        self.print_header()
        if self.bus_type == BUS.AHBL:
            AHBLSLAVE.print_bus_ifc(self,i)
        elif self.bus_type == BUS.APB:
            APBSLAVE.print_bus_ifc(self, i)
        else:
            pass
        if len(self.pins) > 0:
            print(",")
            self.print_pins(i)
        print("\n\t);")

class EF_ADCS8_8CH(AHBLSLAVE, APBSLAVE):
    def __init__(self, name, bus_type=BUS.AHBL):
        self.name = name
        self.module = "EF_ADCS8_8CH"
        #self.module_postfix = ""
        self.pins = [("Ain", 3, 8)]      # 3 means Analog!
        self.bus_type = bus_type;

    def gen_inst(self, i):
        self.print_header()
        if self.bus_type == BUS.AHBL:
            AHBLSLAVE.print_bus_ifc(self,i)
        elif self.bus_type == BUS.APB:
            APBSLAVE.print_bus_ifc(self, i)
        else:
            pass
        if len(self.pins) > 0:
            print(",")
            self.print_pins(i)
        print("\n\t);")

class EF_ADCC10_8CH(AHBLSLAVE, APBSLAVE):
    def __init__(self, name, bus_type=BUS.AHBL):
        self.name = name
        self.module = "EF_ADCC10_8CH"
        #self.module_postfix = ""
        self.pins = [("Ain", 3, 8)]      # 3 means Analog!
        self.bus_type = bus_type;

    def gen_inst(self, i):
        self.print_header()
        if self.bus_type == BUS.AHBL:
            AHBLSLAVE.print_bus_ifc(self,i)
        elif self.bus_type == BUS.APB:
            APBSLAVE.print_bus_ifc(self, i)
        else:
            pass
        if len(self.pins) > 0:
            print(",")
            self.print_pins(i)
        print("\n\t);")



