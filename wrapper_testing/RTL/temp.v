/*
	Copyright 2023 Mohamed Shalan

	Permission is hereby granted, free of charge, to any person obtaining
	a copy of this software and associated documentation files (the
	"Software"), to deal in the Software without restriction, including
	without limitation the rights to use, copy, modify, merge, publish,
	distribute, sublicense, and/or sell copies of the Software, and to
	permit persons to whom the Software is furnished to do so, subject to
	the following conditions:

	The above copyright notice and this permission notice shall be
	included in all copies or substantial portions of the Software.

	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
	EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
	MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
	NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
	LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
	OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
	WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/


`timescale			1ns/1ns
`default_nettype	none
`define			WB_REG(name, init_value)    always @(posedge clk_i or posedge rst_i) if(rst_i) name <= init_value; else if(wb_we & (adr_i==``name``_ADDR)) name <= dat_i;
// `define		WB_ICR(sz)    always @(posedge clk_i or posedge rst_i) if(rst_i) name <= sz'b0; else if(we_we & (adr_i==ICR_REG_ADDR)) ICR_REG <= dat_i; else ICR_REG <= sz'd0; // ERROR 

module ms_tmr32_wb (
	input	wire 		ext_clk,
	output	wire 		pwm_out,
	input	wire 		clk_i,
	input	wire 		rst_i,
	input	wire [31:0]	adr_i,
	input	wire [31:0]	dat_i,
	output	wire [31:0]	dat_o,
	input	wire [3:0]	sel_i,
	input	wire 		cyc_i,
	input	wire 		stb_i,
	output	reg 		ack_o,
	input	wire 		we_i,
	output	wire 		irq
);
 // Dump waves
  initial begin
    $dumpfile("dump.vcd");
	$dumpvars (0, ms_tmr32_wb);
  end
	localparam[15:0] TIMER_REG_ADDR = 16'h0000;
	localparam[15:0] PERIOD_REG_ADDR = 16'h0004;
	localparam[15:0] PWMCMP_REG_ADDR = 16'h0008;
	localparam[15:0] COUNTER_REG_ADDR = 16'h000c;
	localparam[15:0] CONTROL_REG_ADDR = 16'h0010;
	localparam[15:0] MATCH_REG_ADDR = 16'h0014;
	localparam[15:0] ISR_REG_ADDR = 16'h0114;
	localparam[15:0] ICR_REG_ADDR = 16'h0f00;
	localparam[15:0] RIS_REG_ADDR = 16'h0f04;
	localparam[15:0] IM_REG_ADDR = 16'h0f08;
	localparam[15:0] MIS_REG_ADDR = 16'h0f0c;

	reg	[31:0]	PERIOD_REG;
	reg	[31:0]	PWMCMP_REG;
	reg	[31:0]	CONTROL_REG;
	reg	[31:0]	MATCH_REG;
	reg	[2:0]	ISR_REG;
	reg	[2:0]	ICR_REG;
	reg	[2:0]	IM_REG;

	wire[31:0]	tmr;
	wire[31:0]	cp_count;
	wire[31:0]	TIMER_REG	= tmr;
	wire[31:0]	period	= PERIOD_REG[31:0];
	wire[31:0]	pwm_cmp	= PWMCMP_REG[31:0];
	wire[31:0]	COUNTER_REG	= cp_count;
	wire		en	= CONTROL_REG[0:0];
	wire		tmr_en	= CONTROL_REG[1:1];
	wire		pwm_en	= CONTROL_REG[2:2];
	wire		cp_en	= CONTROL_REG[3:3];
	wire[3:0]	clk_src	= CONTROL_REG[11:8];
	wire		up	= CONTROL_REG[16:16];
	wire		one_shot	= CONTROL_REG[17:17];
	wire[1:0]	cp_event	= CONTROL_REG[25:24];
	wire[31:0]	cp_match	= MATCH_REG[31:0];
	wire		to_flag;
	wire		_TO_FLAG_	= to_flag;
	wire		match_flag;
	wire		_MATCH_FLAG_	= match_flag;
	wire		cp_flag;
	wire		_CP_FLAG_	= cp_flag;
	reg[2:0] RIS_REG;
	wire[2:0]	MIS_REG	= RIS_REG & IM_REG;
	wire		wb_valid	= cyc_i & stb_i;
	wire		wb_we	= we_i & wb_valid;
	wire		wb_re	= ~we_i & wb_valid;
	wire[3:0]	wb_byte_sel	= sel_i & {4{wb_we}};
	wire		_clk_	= clk_i;
	wire		_rst_	= rst_i;
	wire ctr_in;
	wire ctr_match;
	ms_tmr32 inst_to_wrap (
		.clk(_clk_),
		.rst_n(~_rst_),
		.ctr_in(ctr_in),
		.pwm_out(pwm_out),
		.period(period),
		.pwm_cmp(pwm_cmp),
		.ctr_match(ctr_match),
		.tmr(tmr),
		.cp_count(cp_count),
		.clk_src(clk_src),
		.to_flag(to_flag),
		.match_flag(match_flag),
		.tmr_en(tmr_en),
		.one_shot(one_shot),
		.up(up),
		.pwm_en(pwm_en),
		.cp_en(cp_en),
		.cp_event(cp_event),
		.cp_flag(cp_flag),
		.en(en)
	);

	always @ (posedge clk_i or posedge rst_i)
		if(rst_i) ack_o <= 1'b0; 
		else
			if(wb_valid & ~ack_o)
				ack_o <= 1'b1;
			else
				ack_o <= 1'b0;

	`WB_REG(PERIOD_REG, 0)
	`WB_REG(PWMCMP_REG, 0)
	`WB_REG(CONTROL_REG, 0)
	`WB_REG(MATCH_REG, 0)

	// `WB_ICR(3) 

	always @(posedge clk_i or negedge rst_i)
		if(~rst_i) RIS_REG <= 32'd0;
		else begin
			if(_TO_FLAG_) RIS_REG[0] <= 1'b1; else if(ICR_REG[0]) RIS_REG[0] <= 1'b0;
			if(_MATCH_FLAG_) RIS_REG[1] <= 1'b1; else if(ICR_REG[1]) RIS_REG[1] <= 1'b0;
			if(_CP_FLAG_) RIS_REG[2] <= 1'b1; else if(ICR_REG[2]) RIS_REG[2] <= 1'b0;

		end

	assign irq = |MIS_REG;

	assign	dat_o = 
			(adr_i == PERIOD_REG_ADDR) ? PERIOD_REG :
			(adr_i == PWMCMP_REG_ADDR) ? PWMCMP_REG :
			(adr_i == CONTROL_REG_ADDR) ? CONTROL_REG :
			(adr_i == MATCH_REG_ADDR) ? MATCH_REG :
			(adr_i == ISR_REG_ADDR) ? ISR_REG :
			(adr_i == ICR_REG_ADDR) ? ICR_REG :
			(adr_i == IM_REG_ADDR) ? IM_REG :
			(adr_i == TIMER_REG_ADDR) ? TIMER_REG :
			(adr_i == COUNTER_REG_ADDR) ? COUNTER_REG :
			(adr_i == MIS_REG_ADDR) ? MIS_REG :
			32'hDEADBEEF;

endmodule
