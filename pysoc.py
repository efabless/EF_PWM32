from bus import BUS

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
