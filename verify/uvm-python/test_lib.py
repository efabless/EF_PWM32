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
from EF_UVM.wrapper_env.wrapper_interface.wrapper_if import wrapper_bus_if, wrapper_irq_if
from cocotb_coverage.coverage import coverage_db
from cocotb.triggers import Event, First
from EF_UVM.wrapper_env.wrapper_regs import wrapper_regs
from uvm.base.uvm_report_server import UVMReportServer
from uvm.base import UVMRoot

# seq
from EF_UVM.wrapper_env.wrapper_seq_lib.write_read_regs import write_read_regs
from pwm32_seq_lib.pwmA_try import pwmA_try

# override classes
from EF_UVM.ip_env.ip_agent.ip_driver import ip_driver
from pwm32_agent.pwm32_driver import pwm32_driver
from EF_UVM.ip_env.ip_agent.ip_monitor import ip_monitor
from pwm32_agent.pwm32_monitor import pwm32_monitor
from EF_UVM.vip.vip import VIP
from vip.vip import PWM32_VIP
from EF_UVM.ip_env.ip_coverage.ip_coverage import ip_coverage
from pwm32_coverage.pwm32_coverage import pwm32_coverage
from EF_UVM.ip_env.ip_logger.ip_logger import ip_logger
from pwm32_logger.pwm32_logger import pwm32_logger

# import cProfile
# import pstats

@cocotb.test()
async def module_top(dut):
    # profiler = cProfile.Profile()
    # profiler.enable()

    pif = pwm32_if(dut)
    w_if = wrapper_bus_if(dut)
    w_irq_if = wrapper_irq_if(dut)
    UVMConfigDb.set(None, "*", "ip_if", pif)
    UVMConfigDb.set(None, "*", "wrapper_bus_if", w_if)
    UVMConfigDb.set(None, "*", "wrapper_irq_if", w_irq_if)
    yaml_file = []
    UVMRoot().clp.get_arg_values("+YAML_FILE=", yaml_file)
    yaml_file = yaml_file[0]
    regs = wrapper_regs(yaml_file)
    UVMConfigDb.set(None, "*", "wrapper_regs", regs)
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




class base_test(UVMTest):
    def __init__(self, name="base_test", parent=None):
        super().__init__(name, parent)
        self.test_pass = True
        self.top_env = None
        self.printer = None

    def build_phase(self, phase):
        # UVMConfigDb.set(self, "example_tb0.wrapper_env.wrapper_agent.wrapper_sequencer.run_phase", "default_sequence", write_seq.type_id.get())
        super().build_phase(phase)
        # override 
        self.set_type_override_by_type(ip_driver.get_type(), pwm32_driver.get_type())
        self.set_type_override_by_type(ip_monitor.get_type(), pwm32_monitor.get_type())
        self.set_type_override_by_type(VIP.get_type(), PWM32_VIP.get_type())
        self.set_type_override_by_type(ip_coverage.get_type(), pwm32_coverage.get_type())
        self.set_type_override_by_type(ip_logger.get_type(), pwm32_logger.get_type())
        # self.set_type_override_by_type(ip_item.get_type(),pwm32_item.get_type())
        # Enable transaction recording for everything
        UVMConfigDb.set(self, "*", "recording_detail", UVM_FULL)
        # Create the tb
        self.example_tb0 = top_env.type_id.create("example_tb0", self)
        # Create a specific depth printer for printing the created topology
        self.printer = UVMTablePrinter()
        self.printer.knobs.depth = -1

        arr = []
        if UVMConfigDb.get(None, "*", "ip_if", arr) is True:
            UVMConfigDb.set(self, "*", "ip_if", arr[0])
        else:
            uvm_fatal("NOVIF", "Could not get ip_if from config DB")

        if UVMConfigDb.get(None, "*", "wrapper_bus_if", arr) is True:
            UVMConfigDb.set(self, "*", "wrapper_bus_if", arr[0])
        else:
            uvm_fatal("NOVIF", "Could not get wrapper_bus_if from config DB")
        # set max number of uvm errors 
        server = UVMReportServer()
        server.set_max_quit_count(1)
        UVMCoreService.get().set_report_server(server)


    def end_of_elaboration_phase(self, phase):
        # Set verbosity for the bus monitor for this demo
        uvm_info(self.get_type_name(), sv.sformatf("Printing the test topology :\n%s", self.sprint(self.printer)), UVM_LOW)

    def start_of_simulation_phase(self, phase):
        self.wrapper_sqr = self.example_tb0.wrapper_env.wrapper_agent.wrapper_sequencer
        self.ip_sqr = self.example_tb0.ip_env.ip_agent.ip_sequencer

    async def run_phase(self, phase):
        uvm_info("sequence", "Starting test", UVM_LOW)

    def extract_phase(self, phase):
        super().check_phase(phase)
        server = UVMCoreService.get().get_report_server()
        errors = server.get_severity_count(UVM_ERROR)
        if errors > 0:
            uvm_fatal("FOUND ERRORS", "There were " + str(errors) + " UVM_ERRORs in the test")

    def report_phase(self, phase):
        uvm_info(self.get_type_name(), "report_phase", UVM_LOW)
        if self.test_pass:
            uvm_info(self.get_type_name(), "** UVM TEST PASSED **", UVM_LOW)
        else:
            uvm_fatal(self.get_type_name(), "** UVM TEST FAIL **\n" +
                self.err_msg)


uvm_component_utils(base_test)


class PWM32_Try(base_test):
    def __init__(self, name="PWM32_Try", parent=None):
        super().__init__(name, parent)
        self.tag = name

    async def run_phase(self, phase):
        uvm_info(self.tag, f"Starting test {self.__class__.__name__}", UVM_LOW)
        phase.raise_objection(self, f"{self.__class__.__name__} OBJECTED")
        wrapper_seq = pwmA_try("pwmA_try")
        await wrapper_seq.start(self.wrapper_sqr)
        phase.drop_objection(self, f"{self.__class__.__name__} drop objection")


uvm_component_utils(PWM32_Try)

