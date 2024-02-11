from uvm.base.sv import sv_if


class pwm32_if(sv_if):

    #  // Actual Signals
    # wire 		pwmA;
    # wire 		pwmB;

    def __init__(self, dut):
        bus_map = {"PCLK": "PCLK", "pwmA": "pwmA", "pwmB": "pwmB"}
        super().__init__(dut, "", bus_map)
