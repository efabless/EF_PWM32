import cocotb
from uvm.comps import UVMTest
from uvm import UVMCoreService
from uvm.macros import uvm_component_utils, uvm_fatal, uvm_info
from uvm.base.uvm_config_db import UVMConfigDb
from uvm.base.uvm_printer import UVMTablePrinter
from uvm.base.sv import sv
from uvm.base.uvm_object_globals import UVM_FULL, UVM_LOW, UVM_ERROR
from uvm.base.uvm_globals import run_test
from EF_UVM.top_env import top_env
from pwm32_interface.pwm32_if import pwm32_if
from EF_UVM.bus_env.bus_interface.bus_if import (
    bus_apb_if,
    bus_irq_if,
    bus_ahb_if,
    bus_wb_if,
)
from cocotb_coverage.coverage import coverage_db
from cocotb.triggers import Event, First
from EF_UVM.bus_env.bus_regs import bus_regs
from uvm.base.uvm_report_server import UVMReportServer

# seq
from EF_UVM.bus_env.bus_seq_lib.write_read_regs import write_read_regs
from uvm.base import UVMRoot

# override classes
from EF_UVM.ip_env.ip_agent.ip_driver import ip_driver
from pwm32_agent.pwm32_driver import pwm32_driver
from EF_UVM.ip_env.ip_agent.ip_monitor import ip_monitor
from pwm32_agent.pwm32_monitor import pwm32_monitor
from EF_UVM.ref_model.ref_model import ref_model
from ref_model.ref_model import PWM32_VIP
from EF_UVM.scoreboard import scoreboard
from EF_UVM.ip_env.ip_coverage.ip_coverage import ip_coverage
from pwm32_coverage.pwm32_coverage import pwm32_coverage
from EF_UVM.ip_env.ip_logger.ip_logger import ip_logger
from pwm32_logger.pwm32_logger import pwm32_logger

#
from EF_UVM.bus_env.bus_agent.bus_ahb_driver import bus_ahb_driver
from EF_UVM.bus_env.bus_agent.bus_apb_driver import bus_apb_driver
from EF_UVM.bus_env.bus_agent.bus_wb_driver import bus_wb_driver
from EF_UVM.bus_env.bus_agent.bus_ahb_monitor import bus_ahb_monitor
from EF_UVM.bus_env.bus_agent.bus_apb_monitor import bus_apb_monitor
from EF_UVM.bus_env.bus_agent.bus_wb_monitor import bus_wb_monitor

from EF_UVM.base_test import base_test
from pwm32_seq_lib.pwmA_try import pwmA_try
# import cProfile
# import pstats

@cocotb.test()
async def module_top(dut):
    # profiler = cProfile.Profile()
    # profiler.enable()
    BUS_TYPE = cocotb.plusargs["BUS_TYPE"]
    print(f"plusr agr value = {BUS_TYPE}")

    pif = pwm32_if(dut)
    if BUS_TYPE == "APB":
        w_if = bus_apb_if(dut)
    elif BUS_TYPE == "AHB":
        w_if = bus_ahb_if(dut)
    elif BUS_TYPE == "WISHBONE":
        w_if = bus_wb_if(dut)
    else:
        uvm_fatal("module_top", f"unknown bus type {BUS_TYPE}")
    # w_irq_if = bus_irq_if(dut)
    UVMConfigDb.set(None, "*", "ip_if", pif)
    UVMConfigDb.set(None, "*", "bus_if", w_if)
    # UVMConfigDb.set(None, "*", "wrapper_irq_if", w_irq_if)
    yaml_file = []
    UVMRoot().clp.get_arg_values("+YAML_FILE=", yaml_file)
    yaml_file = yaml_file[0]
    regs = bus_regs(yaml_file)
    UVMConfigDb.set(None, "*", "bus_regs", regs)
    UVMConfigDb.set(None, "*", "irq_exist", regs.get_irq_exist())
    UVMConfigDb.set(None, "*", "insert_glitches", False)
    UVMConfigDb.set(None, "*", "collect_coverage", False)
    UVMConfigDb.set(None, "*", "disable_logger", False)
    test_path = []
    UVMRoot().clp.get_arg_values("+TEST_PATH=", test_path)
    test_path = test_path[0]
    await run_test()
    coverage_db.export_to_yaml(filename=f"{test_path}/coverage.yalm")
    # profiler.disable()
    # profiler.dump_stats("profile_result.prof")


class pwm32_base_test(base_test):
    def __init__(self, name="base_test", parent=None):
        BUS_TYPE = cocotb.plusargs["BUS_TYPE"]
        super().__init__(name, bus_type=BUS_TYPE, parent=parent)
        self.tag = name

    def build_phase(self, phase):
        # UVMConfigDb.set(self, "example_tb0.wrapper_env.wrapper_agent.wrapper_sequencer.run_phase", "default_sequence", write_seq.type_id.get())
        super().build_phase(phase)
        # override 
        self.set_type_override_by_type(ip_driver.get_type(), pwm32_driver.get_type())
        self.set_type_override_by_type(ip_monitor.get_type(), pwm32_monitor.get_type())
        self.set_type_override_by_type(ref_model.get_type(), PWM32_VIP.get_type())
        self.set_type_override_by_type(ip_coverage.get_type(), pwm32_coverage.get_type())
        self.set_type_override_by_type(ip_logger.get_type(), pwm32_logger.get_type())

uvm_component_utils(pwm32_base_test)


class PWM32_Try(pwm32_base_test):
    def __init__(self, name="PWM32_Try", parent=None):
        super().__init__(name, parent)
        self.tag = name

    async def main_phase(self, phase):
        uvm_info(self.tag, f"Starting test {self.__class__.__name__}", UVM_LOW)
        phase.raise_objection(self, f"{self.__class__.__name__} OBJECTED")
        bus_seq = pwmA_try("pwmA_try")
        await bus_seq.start(self.bus_sqr)
        phase.drop_objection(self, f"{self.__class__.__name__} drop objection")


uvm_component_utils(PWM32_Try)

