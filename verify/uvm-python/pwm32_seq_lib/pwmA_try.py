from uvm.seq import UVMSequence
from uvm.macros.uvm_object_defines import uvm_object_utils
from uvm.macros.uvm_message_defines import uvm_fatal
from uvm.base.uvm_config_db import UVMConfigDb
from cocotb.triggers import Timer
from uvm.macros.uvm_sequence_defines import uvm_do_with, uvm_do
import random
from EF_UVM.bus_env.bus_seq_lib.bus_seq_base import bus_seq_base


class pwmA_try(bus_seq_base):

    def __init__(self, name="pwmA_try"):
        super().__init__(name)

    async def body(self):
        # get register names/address conversion dict
        await super().body()
        three_rand = sorted(random.sample(range(1, 0xFF), 3))
        print(f"three_rand = {three_rand}")
        three_rand = [26, 84, 118]
        GENA = 0b100100
        GENB = 0b011011
        # enable control
        await self.send_req(is_write=True, reg="CLKGATE", data_condition=lambda data: data == 1)
        
        await self.send_req(is_write=True, reg="CLKDIV", data_condition=lambda data: data in [0b1, 0b10, 0b100, 0b1000])
        # await self.send_req(is_write=True, reg="CLKDIV", data_condition=lambda data: data in [0b100])
        await self.send_req(is_write=True, reg="TOP", data_condition=lambda data: data == three_rand[2])
        await self.send_req(is_write=True, reg="GENA", data_condition=lambda data: data == GENA)
        await self.send_req(is_write=True, reg="GENB", data_condition=lambda data: data == GENB)
        await self.send_req(is_write=True, reg="CMPA", data_condition=lambda data: data == three_rand[0])
        await self.send_req(is_write=True, reg="CMPB", data_condition=lambda data: data == three_rand[1])
        await self.send_req(is_write=True, reg="CONTROL", data_condition=lambda data: data == 0b111)
        await Timer(11500, "ns")
        # await self.send_req(is_write=True, reg="GENA")
        await Timer(515500, "ns")


uvm_object_utils(pwmA_try)
