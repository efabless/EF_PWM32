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

class BUSBRIDGE:
    def __init__(self, ratio=2):
        #self.space = 0x10000000
        self.ratio = ratio
        self.sbus = BUS(name="")
        self.space = 0x10000000

    #def set_space(slef, space):
    #    self.space = spacepython3 