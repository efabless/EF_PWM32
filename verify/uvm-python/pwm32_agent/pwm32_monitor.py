from uvm.macros import uvm_component_utils, uvm_fatal, uvm_info, uvm_error, uvm_warning
from uvm.comps.uvm_monitor import UVMMonitor
from uvm.tlm1.uvm_analysis_port import UVMAnalysisPort
from uvm.base.uvm_config_db import UVMConfigDb
from cocotb.triggers import Timer, ClockCycles, FallingEdge, Event, RisingEdge, Combine, First, Edge
from pwm32_item.pwm32_item import pwm32_item
from uvm.base.uvm_object_globals import UVM_HIGH, UVM_LOW, UVM_MEDIUM
import cocotb
import math
from EF_UVM.ip_env.ip_agent.ip_monitor import ip_monitor


class pwm32_monitor(ip_monitor):
    def __init__(self, name="pwm32_monitor", parent=None):
        super().__init__(name, parent)

    async def run_phase(self, phase):
        sample_pwmA = await cocotb.start(self.sample_pwmA())
        sample_pwmB = await cocotb.start(self.sample_pwmB())
        await Combine(sample_pwmA, sample_pwmB)

    async def sample_pwmA(self):
        # wait until clk isn't 0
        while self.regs.read_reg_value("clkdiv") == 0:
            await ClockCycles(self.vif.PCLK, 1)
        while True:
            await Edge(self.vif.pwmA)
            old_val = self.vif.pwmA.value
            count = 0
            pattern_int = []
            clk_div = self.regs.read_reg_value("clkdiv") * 2
            max_count = 0xFF * clk_div * 10  # large possible value for top * number of div cycles * 5
            count_sum = 0
            extracted_pattern = None
            while extracted_pattern is None:
                # start detect pattern
                await RisingEdge(self.vif.PCLK)
                if old_val != self.vif.pwmA.value or count_sum == max_count:
                    pattern_int.append((old_val, count))
                    old_val = self.vif.pwmA.value
                    count = 1
                    count_sum += 1
                    if len(pattern_int) > 6 * 5 or count_sum >= max_count:
                        uvm_info(self.tag, f"count_sum: {count_sum} max_count: {max_count} pattern numbers {len(pattern_int)}", UVM_LOW)
                        extracted_pattern = self.find_repeating_pattern(pattern_int)
                        if extracted_pattern is not None:
                            uvm_info(self.tag, f"sampled PWM A pattern:  {pattern_int} pattern extracted: {extracted_pattern} sum cycles {sum(cycle[1] for cycle in extracted_pattern)}", UVM_LOW)
                        else:
                            uvm_info(self.tag, f"sampled PWM A pattern:  {pattern_int} pattern extracted: {extracted_pattern}", UVM_LOW)
                    else:
                        uvm_info(self.tag, f"sampled PWM A pattern:  {pattern_int}", UVM_LOW)
                else:
                    count += 1
                    count_sum += 1
        
            tr = pwm32_item.type_id.create("tr", self)
            tr.pattern = extracted_pattern
            tr.source = pwm32_item.pwmA
            self.monitor_port.write(tr)
            uvm_info(self.tag, "sampled PWM A transaction: " + tr.convert2string(), UVM_LOW)

    async def sample_pwmB(self):
        # wait until clk isn't 0
        while self.regs.read_reg_value("clkdiv") == 0:
            await ClockCycles(self.vif.PCLK, 1)
        while True:
            await Edge(self.vif.pwmB)
            old_val = self.vif.pwmB.value
            count = 0
            pattern_int = []
            clk_div = self.regs.read_reg_value("clkdiv") * 2
            max_count = 0xFF * clk_div * 10  # large possible value for top * number of div cycles * 5
            count_sum = 0
            extracted_pattern = None
            while extracted_pattern is None:
                # start detect pattern
                await RisingEdge(self.vif.PCLK)
                if old_val != self.vif.pwmB.value or count_sum == max_count:
                    pattern_int.append((old_val, count))
                    old_val = self.vif.pwmB.value
                    count = 1
                    count_sum += 1
                    if len(pattern_int) > 6 * 5 or count_sum >= max_count:
                        uvm_info(self.tag, f"count_sum: {count_sum} max_count: {max_count} pattern numbers {len(pattern_int)}", UVM_LOW)
                        extracted_pattern = self.find_repeating_pattern(pattern_int)
                        if extracted_pattern is not None:
                            uvm_info(self.tag, f"sampled PWM B pattern:  {pattern_int} pattern extracted: {extracted_pattern} sum cycles {sum(cycle[1] for cycle in extracted_pattern)}", UVM_LOW)
                        else:
                            uvm_info(self.tag, f"sampled PWM B pattern:  {pattern_int} pattern extracted: {extracted_pattern}", UVM_LOW)
                    else:
                        uvm_info(self.tag, f"sampled PWM B pattern:  {pattern_int}", UVM_LOW)
                else:
                    count += 1
                    count_sum += 1
        
            tr = pwm32_item.type_id.create("tr", self)
            tr.pattern = extracted_pattern
            tr.source = pwm32_item.pwmB
            self.monitor_port.write(tr)
            uvm_info(self.tag, "sampled PWM A transaction: " + tr.convert2string(), UVM_LOW)

    def find_repeating_pattern(self, lst):
        n = len(lst)
        if n < 2:
            return lst
        # Function to check if the pattern repeats in the remainder of the list
        def find_element_indexes(lst, element):
            return [index for index, value in enumerate(lst) if value == element]

        def check_equal_spaces(pattern):
            for i in range(len(pattern) - 1):
                if pattern[i+1] - pattern[i] != pattern[1] - pattern[0]:
                    return False
            return True

        for i in range(int(n - n/2)):
            possible_pattern = find_element_indexes(lst, lst[i])
            uvm_info(self.tag, f"possible_pattern: {possible_pattern}", UVM_LOW)
            if len(possible_pattern) > 1:
                if check_equal_spaces(possible_pattern):
                    correct_pattern = True
                    for k in range(1, possible_pattern[1]-possible_pattern[0]):
                        expected_pattern = [j + k for j in possible_pattern][:-1] # remove the last one as it might not exist
                        all_equal = all(lst[expected_pattern[0]] == lst[i] for i in expected_pattern)
                        if not all_equal:
                            uvm_info(self.tag, f"[NOT_EQUAL]expected_pattern: {expected_pattern} actual_pattern: {possible_pattern}", UVM_LOW)
                            correct_pattern =  False
                            break
                    if correct_pattern:
                        pattern = lst[possible_pattern[0]:possible_pattern[1]]
                        return pattern
            else:
                continue


uvm_component_utils(pwm32_monitor)
