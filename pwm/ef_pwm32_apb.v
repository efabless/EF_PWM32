/*
	Copyright 2023 Mohamed Shalan


*/


`timescale			1ns/1ns
`default_nettype	none

`define		APB_BLOCK(name, init)	always @(posedge PCLK or negedge PRESETn) if(~PRESETn) name <= init;
`define		APB_REG(name, init)		`APB_BLOCK(name, init) else if(apb_we & (PADDR==``name``_ADDR)) name <= PWDATA;
`define		APB_ICR(sz)				`APB_BLOCK(ICR_REG, sz'b0) else if(apb_we & (PADDR==ICR_REG_ADDR)) ICR_REG <= PWDATA; else ICR_REG <= sz'd0;

module ef_pwm32_apb (
	output	wire 		pwmA,
	output	wire 		pwmB,
	input	wire 		PCLK,
	input	wire 		PRESETn,
	input	wire [31:0]	PADDR,
	input	wire 		PWRITE,
	input	wire 		PSEL,
	input	wire 		PENABLE,
	input	wire [31:0]	PWDATA,
	output	wire [31:0]	PRDATA,
	output	wire 		PREADY
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
	wire		apb_valid	= PSEL & PENABLE;
	wire		apb_we	= PWRITE & apb_valid;
	wire		apb_re	= ~PWRITE & apb_valid;
	wire		_clk_	= PCLK;
	wire		_rst_	= ~PRESETn;

	ef_pwm32 inst_to_wrap (
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

	`APB_REG(CMPA_REG, 0)
	`APB_REG(CMPB_REG, 0)
	`APB_REG(LOAD_REG, 0)
	`APB_REG(CLKDIV_REG, 0)
	`APB_REG(CONTROL_REG, 0)
	`APB_REG(GENA_REG, 0)
	`APB_REG(GENB_REG, 0)
	assign	PRDATA = 
			(PADDR == CMPA_REG_ADDR) ? CMPA_REG :
			(PADDR == CMPB_REG_ADDR) ? CMPB_REG :
			(PADDR == LOAD_REG_ADDR) ? LOAD_REG :
			(PADDR == CLKDIV_REG_ADDR) ? CLKDIV_REG :
			(PADDR == CONTROL_REG_ADDR) ? CONTROL_REG :
			(PADDR == GENA_REG_ADDR) ? GENA_REG :
			(PADDR == GENB_REG_ADDR) ? GENB_REG :
			32'hDEADBEEF;


	assign PREADY = 1'b1;

endmodule