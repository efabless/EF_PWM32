from uvm.seq import UVMSequence
from uvm.macros.uvm_object_defines import uvm_object_utils
from uvm.macros.uvm_message_defines import uvm_fatal
from EF_UVM.wrapper_env.wrapper_item import wrapper_bus_item
from uvm.base.uvm_config_db import UVMConfigDb
from EF_UVM.wrapper_env.wrapper_seq_lib.wrapper_seq_base import wrapper_seq_base
from cocotb.triggers import Timer
from uvm.macros.uvm_sequence_defines import uvm_do_with, uvm_do
import random


class pwmA_try(wrapper_seq_base):

    def __init__(self, name="pwmA_try"):
        super().__init__(name)

    async def body(self):
        # get register names/address conversion dict
        await super().body()
        three_rand = sorted(random.sample(range(1, 0xFF), 3))
        # enable control
        await self.send_req(is_write=True, reg="clkdiv", data_condition=lambda data: data in [0b1, 0b10, 0b100, 0b1000])
        await self.send_req(is_write=True, reg="top", data_condition=lambda data: data == three_rand[2])
        await self.send_req(is_write=True, reg="GENA")
        await self.send_req(is_write=True, reg="GENB")
        await self.send_req(is_write=True, reg="cmpA", data_condition=lambda data: data == three_rand[0])
        await self.send_req(is_write=True, reg="cmpB", data_condition=lambda data: data == three_rand[1])
        await self.send_req(is_write=True, reg="control", data_condition=lambda data: data & 0b111 == 0b111)
        await Timer(11500, "ns")
        # await self.send_req(is_write=True, reg="GENA")
        await Timer(515500, "ns")


uvm_object_utils(pwmA_try)
