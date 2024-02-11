from uvm.base.uvm_component import UVMComponent
from uvm.macros import uvm_component_utils
from uvm.tlm1.uvm_analysis_port import UVMAnalysisImp
from uvm.base.uvm_object_globals import UVM_HIGH, UVM_LOW, UVM_MEDIUM 
from uvm.macros import uvm_component_utils, uvm_fatal, uvm_info
from uvm.base.uvm_config_db import UVMConfigDb
from uvm.tlm1.uvm_analysis_port import UVMAnalysisExport
from EF_UVM.vip.vip import VIP 
from EF_UVM.wrapper_env.wrapper_item import wrapper_bus_item
from pwm32_item.pwm32_item import pwm32_item


class PWM32_VIP(VIP):
    def __init__(self, name="PWM32_VIP", parent=None):
        super().__init__(name, parent)

    def build_phase(self, phase):
        super().build_phase(phase)
        arr = []
        if (not UVMConfigDb.get(self, "", "wrapper_regs", arr)):
            uvm_fatal(self.tag, "No json file wrapper regs")
        else:
            self.regs = arr[0]
    
    def write_bus(self, tr):
        uvm_info(self.tag, "Vip write: " + tr.convert2string(), UVM_MEDIUM)
        if tr.reset:
            self.wrapper_bus_export.write(tr)
            return
        if tr.kind == wrapper_bus_item.WRITE:
            self.regs.write_reg_value(tr.addr, tr.data)
            self.wrapper_bus_export.write(tr)
        elif tr.kind == wrapper_bus_item.READ:
            data = self.regs.read_reg_value(tr.addr)
            td = tr.do_clone()
            td.data = data
            self.wrapper_bus_export.write(td)

    def write_ip(self, tr):
        uvm_info(self.tag, "ip Vip write: " + tr.convert2string(), UVM_MEDIUM)
        # when monitor detect patterns the vip should also send pattern
        td = pwm32_item.type_id.create("td", self)
        td.source = tr.source
        td.pattern = self.generate_patterns(tr.source)
        self.ip_export.write(td)
    
    def generate_patterns(self, source):
        def merge_similar(pattern1):
            if len(pattern1) < 2:
                return pattern1
            if pattern1[0][0] == pattern1[-1][0]:
                new_element = (pattern1[0][0], pattern1[0][1] + pattern1[-1][1])
                pattern1 = pattern1[:-1]
                pattern1[0] = new_element
            return pattern1

        def rearrange_actions(actions):
            # remove if number of cycles == 0
            # before remove it should affect the next action
            to_remove = []
            for i in range(len(actions)):
                if actions[i][1] == 0:
                    to_remove.append(i)
                    if actions[i][0] == "no change": # no change should not affect the next action
                        continue
                    elif actions[i + 1][0] == "no change":
                        actions[i + 1] = (actions[i][0], actions[i + 1][1])
                    # elif actions[i + 1][0] == "inverted":
                    #     if actions[i][0] == "high":
                    #         actions[i + 1] = ("low", actions[i + 1][1])
                    #     elif actions[i][0] == "low":
                    #         actions[i + 1][0] = ("high", actions[i + 1][1])
                    #     elif actions[i][0] == "inverted":
                    #         actions[i + 1][0] = ("no change", actions[i + 1][1])
            actions = [i for i in actions if i not in to_remove]
                    
            actions = [action for action in actions if action[1] != 0]
            # can't begin the action with no change
            if actions[0][0] not in ["no change"]:
                return actions
            i = 0
            for index, action in enumerate(actions):
                if action[0] not in ["no change"]:
                    i = index
                    break
            actions = actions[i:] + actions[:i]
            return actions

        def try_initial(actions, initial):
            for action in actions:
                if action[0] == "no change":
                    continue
                elif action[0] == "high":
                    initial = 1
                elif action[0] == "low":
                    initial = 0
                elif action[0] == "inverted":
                    initial = 1 - initial
            return initial

        def pattern_from_action(actions):
            pattern = []
            # check if the initial value matter
            if actions[0][0] in ["high", "low"]:
                initial_values = [0]  # initial doesn't matter
            elif actions[0][0] in ["inverted"]:
                if try_initial(actions, 0) == 0 and try_initial(actions, 1) == 1:  # loop the same value
                    initial_values = [0] # assume 0 is initial value after reset
                elif try_initial(actions, 0) == try_initial(actions, 1):
                    initial_values = [try_initial(actions, 0)]
                else:
                    initial_values = [try_initial(actions, 1), try_initial(actions, 0)]
            else:
                initial_values = [0]
            # for action in actions:
            #     if action[0] == "high":
            #         initial_values = [1]
            #     elif action[0] == "low":
            #         initial_values = [0]
            #     elif action[0] == "inverted":
            #         if len(initial_values) == 1:
            #             initial_values = [1 - initial_values[0]]

            uvm_info(self.tag, f"initial_values: {initial_values}", UVM_MEDIUM)
            # if there is no fixed value 2 initial values are needed
            for i in initial_values:
                old_val = i
                count = 0
                for i, action in enumerate(actions):
                    if action[0] == "no change":
                        val = old_val
                    elif action[0] == "high":
                        val = 1
                    elif action[0] == "low":
                        val = 0
                    elif action[0] == "inverted":
                        val = 1 - old_val
                    if val == old_val or i == 0:
                        count += action[1]
                    elif val != old_val:
                        pattern.append((old_val, count))
                        count = action[1]
                    old_val = val
                if count > 0:
                    pattern.append((old_val, count))
            return pattern
        def invert_pattern(pattern):
            for i in range(len(pattern)):
                if pattern[i][0] == 1:
                    pattern[i] = (0, pattern[i][1])
                elif pattern[i][0] == 0:
                    pattern[i] = (1, pattern[i][1])
            return pattern
        def process_action(actions, is_inverted):
            compare_vals = {"cmpA":self.regs.read_reg_value("cmpA"), "cmpB":self.regs.read_reg_value("cmpB"), "top":self.regs.read_reg_value("top")}
            actions_types = ["no change", "high", "low", "inverted"]
            clk_div = self.regs.read_reg_value("clkdiv") * 2
            action_length = [compare_vals["cmpA"], compare_vals["cmpB"]-compare_vals["cmpA"], compare_vals["top"]-compare_vals["cmpB"] ]
            action_length += action_length[::-1]
            action_length = [val * clk_div for val in action_length]
            actions = [(actions_types[type], action_length[index]) for index, type in enumerate(actions)]
            mode = (self.regs.read_reg_value("control") >> 5) & 0b1
            if mode == 0:
                actions = actions[:3] + [(actions[3][0], clk_div)]
            uvm_info(self.tag, f"actions: {actions}", UVM_MEDIUM)
            actions = rearrange_actions(actions)
            uvm_info(self.tag, f"actions after rearrange: {actions}", UVM_MEDIUM)
            pattern = pattern_from_action(actions)
            pattern = merge_similar(pattern)
            if is_inverted:
                pattern = [(1 - pulse_type, cycles) for pulse_type, cycles in pattern]
            return pattern

        if source == pwm32_item.pwmA:
            # check if pwmA is disabled don't send patterns
            if self.regs.read_reg_value("control") & 0b11 != 0b11:
                return None
            actions = [(self.regs.read_reg_value("GENA") >> i) & 0b11 for i in range(0, 12, 2)]
            is_inverted = (self.regs.read_reg_value("control") >> 3) & 0b1
            return process_action(actions, is_inverted)
        elif source == pwm32_item.pwmB:
            if self.regs.read_reg_value("control") & 0b101 != 0b101:
                return None
            actions = [(self.regs.read_reg_value("GENB") >> i) & 0b11 for i in range(0, 12, 2)]
            is_inverted = (self.regs.read_reg_value("control") >> 4) & 0b1
            return process_action(actions, is_inverted)
            

uvm_component_utils(PWM32_VIP)
