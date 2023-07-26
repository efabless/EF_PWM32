import cocotb 
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge
import random
import json
import os


@cocotb.test()
async def ahb_test(dut):
    cocotb.log.info("Starting test wb wrapper generated")
    json_path = os.environ.get("IP_JSON")
    regs = WrapperRegs(json_path)
    inputs = {"clk": dut.HCLK, "rst": dut.HRESETn, "ready": dut.HREADY, "we": dut.HWRITE, "size": dut.HSIZE, "sel": dut.HSEL, "trans": dut.HTRANS, "addr": dut.HADDR, "data": dut.HWDATA}
    outputs = {"data": dut.HRDATA, "ready": dut.HREADYOUT}
    await setup_clock_reset(inputs["clk"], 25, inputs["rst"])
    wb = AHB(inputs, outputs)
    for reg in regs.regs:
        rand_32 = random.randint(0, 0xffffffff)
        cocotb.log.info(f"writing  {hex(rand_32)} to {reg.name} ")
        await wb.ahb_write(reg.address, rand_32)
        actual = await wb.ahb_read(reg.address)
        actual = await wb.ahb_read(reg.address)
        if actual != rand_32:
            if "w" in reg.access:
                cocotb.log.error(f"read {hex(actual)} from {reg.name} after writing {hex(rand_32)}")
            else: 
                cocotb.log.info(f"read diffrent value {hex(actual)} from {reg.name} after writing {hex(rand_32)} because it's not writable reg")
        else:
            cocotb.log.info(f"read same value written {hex(actual)} from {reg.name} ")


async def setup_clock_reset(clk, period, reset):
    clock_obj = Clock(clk, period, "ns") 
    cocotb.start_soon(clock_obj.start())  # Start the clock
    reset.value = 0
    await ClockCycles(clk, 5)
    reset.value = 1


class AHB:
    def __init__(self, inputs, outputs) -> None:
        self.inputs = inputs
        self.outputs = outputs
        self.data_out = None
        pass

    async def _ahb_address_phase(self, address, write=True):
        #address phase
        if self.outputs["ready"].value == 0: # wait until slave is ready
            await RisingEdge(self.outputs["ready"])
        self.inputs["ready"].value = 1
        self.inputs["size"].value = 4
        self.inputs["we"].value = 1 if write else 0
        self.inputs["trans"].value = int("10", 2) # NONSEQ
        self.inputs["sel"].value = 1
        self.inputs["addr"].value = address
        await ClockCycles(self.inputs["clk"], 1)

    async def _ahb_data_phase(self, data=None):
        if data is not None:
            self.inputs["data"].value = data
            if self.outputs["ready"].value == 0: # wait until slave is ready
                await RisingEdge(self.outputs["ready"])
            await ClockCycles(self.inputs["clk"], 1)
            self.data_out = None
        else:
            if self.outputs["ready"].value == 0: # wait until slave is ready
                await RisingEdge(self.outputs["ready"])
            await ClockCycles(self.inputs["clk"], 1)
            self.data_out = self.outputs["data"].value

    async def ahb_write(self, address, data):
        await self._ahb_address_phase(address)
        await cocotb.start(self._ahb_data_phase(data))
        return self.data_out

    async def ahb_read(self, address):
        await self._ahb_address_phase(address, write=False)
        await cocotb.start(self._ahb_data_phase())
        return self.data_out


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