import cocotb 
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge
import random
import json
import os


@cocotb.test()
async def wb_test(dut):
    cocotb.log.info("Starting test wb wrapper generated")
    json_path = os.environ.get("IP_JSON")
    regs = WrapperRegs(json_path)
    inputs = {"clk": dut.clk_i, "rst": dut.rst_i, "stb": dut.stb_i, "we": dut.we_i, "cyc": dut.cyc_i, "sel": dut.sel_i, "addr": dut.adr_i, "data": dut.dat_i}
    outputs = {"data": dut.dat_o, "ack": dut.ack_o}
    await setup_clock_reset(inputs["clk"], 25, inputs["rst"])
    wb = Wishbone(inputs, outputs)
    for reg in regs.regs:
        rand_32 = random.randint(0, 0xffffffff)
        cocotb.log.info(f"writing  {hex(rand_32)} to {reg.name} ")
        await wb.wb_write(reg.address, rand_32)
        actual = await wb.wb_read(reg.address)
        if actual != rand_32:
            if "w" in reg.access:
                cocotb.log.error(f"read {hex(actual)} from {reg.name} after writing {rand_32}")
            else: 
                cocotb.log.info(f"read diffrent value {hex(actual)} from {reg.name} after writing {hex(rand_32)} because it's not writable reg")
        else:
            cocotb.log.info(f"read same value written {hex(actual)} from {reg.name} ")


async def setup_clock_reset(clk, period, reset):
    clock_obj = Clock(clk, period, "ns") 
    cocotb.start_soon(clock_obj.start())  # Start the clock
    reset.value = 1
    await ClockCycles(clk, 5)
    reset.value = 0

class Wishbone:
    def __init__(self, inputs, outputs) -> None:
        self.inputs = inputs
        self.outputs = outputs
        pass

    async def wb_write(self, address, data):
        await ClockCycles(self.inputs["clk"], 1)
        self.inputs["data"].value = data
        self.inputs["stb"].value = 1
        self.inputs["we"].value = 1
        self.inputs["cyc"].value = 1
        self.inputs["sel"].value = 0xF
        self.inputs["addr"].value = address
        await RisingEdge (self.outputs["ack"])
        self.inputs["data"].value = 0
        self.inputs["stb"].value = 0
        self.inputs["we"].value = 0
        self.inputs["cyc"].value = 0
        self.inputs["sel"].value = 0
        self.inputs["addr"].value = 0
        await ClockCycles(self.inputs["clk"], 1)

    async def wb_read(self, address):
        await ClockCycles(self.inputs["clk"], 1)
        self.inputs["stb"].value = 1
        self.inputs["we"].value = 0
        self.inputs["cyc"].value = 1
        self.inputs["sel"].value = 0xF
        self.inputs["addr"].value = address
        await RisingEdge (self.outputs["ack"])
        output = self.outputs["data"].value
        self.inputs["stb"].value = 0
        self.inputs["we"].value = 0
        self.inputs["cyc"].value = 0
        self.inputs["sel"].value = 0
        self.inputs["addr"].value = 0
        await ClockCycles(self.inputs["clk"], 1)
        return output

class WrapperRegs():
    def __init__(self, ip_json_path):
        self.ip_json_path = ip_json_path
        self.regs = []
        self.create_regs()

    def create_regs(self):
        regs_list = self._read_regs_from_json()
        address = 0
        for reg in regs_list:
            self._add_register(reg["name"], address, size=int(reg["size"]), access=reg["mode"])
            address += 4

    def _read_regs_from_json(self):
        with open(self.ip_json_path, 'r') as file:
            data = json.load(file)
        return data["regs"]

    def _add_register(self, reg_name, address, size, access):
        self.regs.append(register(reg_name, address, size, access))

class register():
    def __init__(self, name, address, size, access):
        self.name = name
        self.address = address
        self.size = size
        self.access = access
        cocotb.log.info(f"found register {self.name} with address {self.address} and size {self.size} and access {self.access}")