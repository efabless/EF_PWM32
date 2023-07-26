# This file is public domain, it can be freely copied without restrictions.
# SPDX-License-Identifier: CC0-1.0

TOPLEVEL_LANG ?= verilog
export IP_JSON = $(shell pwd)/../../ip.json

VERILOG_SOURCES = $(shell pwd)/../RTL/temp.v
VERILOG_SOURCES += $(shell pwd)/../RTL/ms_tmr32.v
MODULE = wb_test
TOPLEVEL = ms_tmr32_wb

include $(shell cocotb-config --makefiles)/Makefile.sim