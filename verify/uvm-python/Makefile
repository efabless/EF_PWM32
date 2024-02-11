PLUSARGS += "+UVM_VERBOSITY=UVM_MEDIUM"
TOPLEVEL := top
MODULE   ?= top_module
VERILOG_SOURCES ?=  $(PWD)/top.v $(PWD)/../../hdl/rtl/bus_wrappers/EF_PWM32_apb.v  $(PWD)/../../hdl/rtl/EF_PWM32.v
RTL_MACROS ?= ""
YAML_FILE = $(PWD)/../../EF_PWM32.json
MAKEFLAGS += --no-print-directory

# List of tests
TESTS := PWM32_Try

# Variable for tag - set this as required
SIM_TAG ?= default_tag

# Define SIM_PATH variable
SIM_PATH := $(PWD)/sim/$(SIM_TAG)

include EF_UVM/Makefile.test
