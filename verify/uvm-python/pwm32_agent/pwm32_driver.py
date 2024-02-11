from uvm.macros import uvm_component_utils, uvm_fatal, uvm_info, uvm_warning
from uvm.comps.uvm_driver import UVMDriver
from uvm.base.uvm_config_db import UVMConfigDb
from uvm.base.uvm_object_globals import UVM_HIGH, UVM_LOW, UVM_MEDIUM
from cocotb.triggers import Timer, ClockCycles, FallingEdge, Event, RisingEdge
from EF_UVM.wrapper_env.wrapper_agent.wrapper_driver import wrapper_driver


class pwm32_driver(wrapper_driver):
    def __init__(self, name="pwm32_driver", parent=None):
        super().__init__(name, parent)
        self.tag = name

    async def run_phase(self, phase):
        return


uvm_component_utils(pwm32_driver)
