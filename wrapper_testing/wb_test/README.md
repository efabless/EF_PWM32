# run wishbone test

## Requirements

Before running the tests, make sure you have the following tools installed:

- [Cocotb](https://github.com/cocotb/cocotb): A Python-based framework for testbenches.
- [Icarus Verilog (iverilog)](http://iverilog.icarus.com/): A Verilog simulation and synthesis tool.

## Running the Tests

To run the tests, follow these steps:

1. Update the RTL paths in the Makefile:

   Open the `Makefile` in the project directory and locate the variable `VERILOG_SOURCES`. Update this variable with the paths to your Verilog RTL files that you want to test. For example:

   ```make
   VERILOG_SOURCES = path/to/rtl1.v path/to/rtl2.v path/to/rtl3.v
Replace path/to/rtl1.v, path/to/rtl2.v, etc. with the actual paths to your Verilog RTL files.

Run the tests:

Open a terminal or command prompt, navigate to the project directory, and use the make command to execute the tests:

`make`

The tests will be executed using Cocotb with Icarus Verilog as the simulator. The test results will be displayed in the terminal.

That's it! You have successfully run the test.

