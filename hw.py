import math
from verilog_gen import *

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
class BUS:
    AHBL = 0
    AHB = 1
    APB = 2
    WB = 3
    BUS_NAMES = ["AHBL", "AHB", "APB", "WB"]
    BUS_TYPEs = [AHBL, AHB, APB, WB]
    
    def __init__(self, name, type = AHBL, base=0, num_pages=8):
        self.name = name
        self.base = base
        self.type = type
        self.num_pages = num_pages
        self.slaves =[]
        #self.page_size = 0
        self.space = 0x100000000
        self.page_size = self.space/self.num_pages
        self.slave_start_num = 0
        self.snum = 0

    def add_slave(self, slave, page=0):
        if(issubclass(type(slave), BUSBRIDGE)):
            slave.sbus.set_space(self.page_size)
            slave.set_space(self.page_size)
            #slave.sbus.set_slave_start_num(self.snum)
            #self.snum = self.snum + len(slave.sbus.slaves)
        slave.set_bus_type(self.type)
        self.slaves.append(tuple((slave, page, self.snum)))
        self.snum = self.snum + 1

    def set_space(self, space):
        self.space = space
        self.page_size = self.space/self.num_pages
        #print(f"setting the space of bus {self.name} to {hex(self.space)}")

    def set_slave_start_num(self, n):
        self.slave_start_num = n
        #self.adjust_slave_nums()
        print(f"====> {self.name} : {self.slave_start_num}")

    def adjust_slave_nums(self):
        ns = []
        #print(self.slaves)
        for s in self.slaves:
            (slave, page, num) = s
            ns.append(tuple((slave, page, num+self.slave_start_num)))
            #print(ns)
        self.slaves = ns
        #print(ns)
        #print(self.slaves)

    def get_pins(self):
        pins = []
        for s in self.slaves:
            (slave, page, num) = s
            if(issubclass(type(slave), BUSBRIDGE)):
                for ss in slave.sbus.slaves:
                    (bslave, bpage, bnum) = ss
                    for p in bslave.pins:
                        (nm, sz, d) = p
                        pins.append(tuple((bslave.name, nm, sz, d)))
            else:
                for p in slave.pins:
                    (nm, sz, d) = p
                    pins.append(tuple((slave.name, nm, sz, d)))
                    
        return pins
    
    def print(self):
        print(f"{self.name} : {self.BUS_NAMES[self.type]} bus with {len(self.slaves)} slaves:")
        for s in self.slaves:
            (slave, page, num) = s
            print(f"\tSlave: {slave.name} @ {'0x{:08x}'.format(int(self.base+self.page_size*page))}")
            if(issubclass(type(slave), BUSBRIDGE)):
                for ss in slave.sbus.slaves:
                    (bslave, bpage, bnum) = ss
                    print(f"\t\tSlave: {bslave.name} @ {'0x{:08x}'.format(int(slave.sbus.base+slave.sbus.page_size*bpage))}")
        pins = self.get_pins()
        print(f"Pins ({len(pins)}) : ", pins)

    def print_slaves(self):
        print(f"Bus: {self.name} [{hex(int(self.page_size))}]")
        for s in self.slaves:
            (slave, page, num) = s
            print(s)
            if(issubclass(type(slave), BUSBRIDGE)):
                print(f"\tBus: {slave.sbus.name} [{hex(int(slave.sbus.page_size))}]")
                for ss in slave.sbus.slaves:
                    (bslave, bpage, bnum) = ss
                    print(f"\t{ss}")
        
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
        self.add_ports()
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
        self.add_ports()
        self.gen_bus_dec()
        self.mod.print_header()
        self.mod.print_localparams()
        self.mod.print_wires()
        self.mod.print_regs()
        self.gen_bus_mux()
        self.mod.print_ports_assign()
        self.gen_slave_instances()
        self.mod.print_footer()

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

class FLASH(AHBLSLAVE):
    def __init__(self, name, writer=False, lines=16, bus_type=BUS.AHBL):
        super().__init__
        self.name = name
        self.writer = writer
        self.lines = lines
        self.module = "FLASH"
        self.module_postfix = "AHBL"
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

class MS_TMR32(AHBLSLAVE, APBSLAVE):
    def __init__(self, name, bus_type=BUS.AHBL):
        self.check_bus_type(bus_type)
        self.name = name
        self.bus_type = bus_type
        self.module = "MS_TMR32"
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

class MS_UART(AHBLSLAVE, APBSLAVE):
    def __init__(self, name, bus_type=BUS.AHBL):
        self.name = name
        self.module = "MS_UART"
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

class BUSBRIDGE:
    def __init__(self, ratio=2):
        #self.space = 0x10000000
        self.ratio = ratio
        self.sbus = BUS(name="")
        self.space = 0x10000000

    #def set_space(slef, space):
    #    self.space = space

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

class CPU:
    SUPPORTED_CPU = ['vexLite', 'vexSmall', 'vexBig', "picoLite"]
    def __init__(self, name):
        if name not in self.SUPPORTED_CPU:
            raise ValueError(f'Unsupported CPU: {name}')
        self.name = name
        self.ibus = BUS(name="")
        self.dbus = BUS(name="")   

class SOC:
    def __init__(self, name, cpu):
        self.name = name
        self.cpu = cpu
        self.comps = []

    def add_comp(self, comp):
        self.comps.append(comp)

    def print(self):
        print("SoC : ", self.name)
        print("CPU : ", self.cpu.name)
        for c in self.comps:
            c.print()

#my_tmr0 = MS_TMR32(name="S0", bus_type="ahbl")
#my_tmr1 = MS_TMR32(name="S2", bus_type="apb")
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

ls_bus0.add_slave(slave=MS_UART(name="uart0"), page=4)
ls_bus0.add_slave(slave=MS_UART(name="uart1"), page=6)
ls_bus0.add_slave(slave=MS_TMR32(name="tmr0"), page=7)
ls_bus0.add_slave(slave=MS_TMR32(name="tmr1"), page=8)

ls_bus1.add_slave(slave=MS_UART(name="uart2"), page=4)
ls_bus1.add_slave(slave=MS_TMR32(name="uart3"), page=6)
ls_bus1.add_slave(slave=MS_TMR32(name="tmr2"), page=7)
ls_bus1.add_slave(slave=MS_TMR32(name="tmr3"), page=8)

my_cpu = CPU(name="vexLite")
cpu_bus_mux = AHBL_MMUX(name="mmux", port0=my_cpu.dbus, port1=my_cpu.ibus, outport=hs_bus)
my_soc = SOC(name="raptor", cpu=my_cpu)
my_soc.add_comp(cpu_bus_mux)
my_soc.add_comp(hs_bus)
#my_soc.print()

#ahb_bus = AHBL(name="AHBL_BUS", type=BUS.AHBL, base=0, num_pages=16)
hs_bus.gen_bus_logic()
ls_bus0.gen_bus_logic()
ls_bus1.gen_bus_logic()
#hs_bus.print_slaves()
hs_bus.print()
#print(hs_bus.get_pins())