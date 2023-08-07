/*
	Copyright 2023 Mohamed Shalan


*/


`timescale			1ns/1ns
`default_nettype	none

`define		WB_BLOCK(name, init)	always @(posedge clk_i or posedge rst_i) if(rst_i) name <= init;
`define		WB_REG(name, init)		`WB_BLOCK(name, init) else if(wb_we & (adr_i==``name``_ADDR)) name <= dat_i;
`define		WB_ICR(sz)				`WB_BLOCK(ICR_REG, sz'b0) else if(wb_we & (adr_i==ICR_REG_ADDR)) ICR_REG <= dat_i; else ICR_REG <= sz'd0;

module EF_PWM32_wb (
	output	wire 		pwmA,
	output	wire 		pwmB,
	input	wire 		clk_i,
	input	wire 		rst_i,
	input	wire [31:0]	adr_i,
	input	wire [31:0]	dat_i,
	output	wire [31:0]	dat_o,
	input	wire [3:0]	sel_i,
	input	wire 		cyc_i,
	input	wire 		stb_i,
	output	reg 		ack_o,
	input	wire 		we_i
);
	localparam[15:0] CMPA_REG_ADDR = 16'h0000;
	localparam[15:0] CMPB_REG_ADDR = 16'h0004;
	localparam[15:0] LOAD_REG_ADDR = 16'h0008;
	localparam[15:0] CLKDIV_REG_ADDR = 16'h000c;
	localparam[15:0] CONTROL_REG_ADDR = 16'h0010;
	localparam[15:0] GENA_REG_ADDR = 16'h0014;
	localparam[15:0] GENB_REG_ADDR = 16'h0018;

	reg	[31:0]	CMPA_REG;
	reg	[31:0]	CMPB_REG;
	reg	[31:0]	LOAD_REG;
	reg	[3:0]	CLKDIV_REG;
	reg	[5:0]	CONTROL_REG;
	reg	[11:0]	GENA_REG;
	reg	[11:0]	GENB_REG;

	wire[31:0]	cmpA	= CMPA_REG[31:0];
	wire[31:0]	cmpB	= CMPB_REG[31:0];
	wire[31:0]	load	= LOAD_REG[31:0];
	wire[3:0]	clkdiv	= CLKDIV_REG[3:0];
	wire		en	= CONTROL_REG[0:0];
	wire		enA	= CONTROL_REG[1:1];
	wire		enB	= CONTROL_REG[2:2];
	wire		invA	= CONTROL_REG[3:3];
	wire		invB	= CONTROL_REG[4:4];
	wire		cntr_mode	= CONTROL_REG[5:5];
	wire[1:0]	pwmA_e0a	= GENA_REG[1:0];
	wire[1:0]	pwmA_e1a	= GENA_REG[3:2];
	wire[1:0]	pwmA_e2a	= GENA_REG[5:4];
	wire[1:0]	pwmA_e3a	= GENA_REG[7:6];
	wire[1:0]	pwmA_e4a	= GENA_REG[9:8];
	wire[1:0]	pwmA_e5a	= GENA_REG[11:10];
	wire[1:0]	pwmB_e0a	= GENB_REG[1:0];
	wire[1:0]	pwmB_e1a	= GENB_REG[3:2];
	wire[1:0]	pwmB_e2a	= GENB_REG[5:4];
	wire[1:0]	pwmB_e3a	= GENB_REG[7:6];
	wire[1:0]	pwmB_e4a	= GENB_REG[9:8];
	wire[1:0]	pwmB_e5a	= GENB_REG[11:10];
	wire		wb_valid	= cyc_i & stb_i;
	wire		wb_we	= we_i & wb_valid;
	wire		wb_re	= ~we_i & wb_valid;
	wire[3:0]	wb_byte_sel	= sel_i & {4{wb_we}};
	wire		_clk_	= clk_i;
	wire		_rst_	= rst_i;

	EF_PWM32 inst_to_wrap (
		.clk(_clk_),
		.rst_n(~_rst_),
		.pwmA(pwmA),
		.pwmB(pwmB),
		.cmpA(cmpA),
		.cmpB(cmpB),
		.load(load),
		.clkdiv(clkdiv),
		.cntr_mode(cntr_mode),
		.enA(enA),
		.enB(enB),
		.invA(invA),
		.invB(invB),
		.pwmA_e0a(pwmA_e0a),
		.pwmA_e1a(pwmA_e1a),
		.pwmA_e2a(pwmA_e2a),
		.pwmA_e3a(pwmA_e3a),
		.pwmA_e4a(pwmA_e4a),
		.pwmA_e5a(pwmA_e5a),
		.pwmB_e0a(pwmB_e0a),
		.pwmB_e1a(pwmB_e1a),
		.pwmB_e2a(pwmB_e2a),
		.pwmB_e3a(pwmB_e3a),
		.pwmB_e4a(pwmB_e4a),
		.pwmB_e5a(pwmB_e5a)
	);

	always @ (posedge clk_i or posedge rst_i)
		if(rst_i) ack_o <= 1'b0;
		else
			if(wb_valid & ~ack_o)
				ack_o <= 1'b1;
			else
				ack_o <= 1'b0;

	`WB_REG(CMPA_REG, 0)
	`WB_REG(CMPB_REG, 0)
	`WB_REG(LOAD_REG, 0)
	`WB_REG(CLKDIV_REG, 0)
	`WB_REG(CONTROL_REG, 0)
	`WB_REG(GENA_REG, 0)
	`WB_REG(GENB_REG, 0)
	assign	dat_o = 
			(adr_i == CMPA_REG_ADDR) ? CMPA_REG :
			(adr_i == CMPB_REG_ADDR) ? CMPB_REG :
			(adr_i == LOAD_REG_ADDR) ? LOAD_REG :
			(adr_i == CLKDIV_REG_ADDR) ? CLKDIV_REG :
			(adr_i == CONTROL_REG_ADDR) ? CONTROL_REG :
			(adr_i == GENA_REG_ADDR) ? GENA_REG :
			(adr_i == GENB_REG_ADDR) ? GENB_REG :
			32'hDEADBEEF;

endmodule
