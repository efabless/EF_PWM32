/*
	Copyright 2023 Mohamed Shalan


*/


`timescale			1ns/1ns
`default_nettype	none

`define		AHB_BLOCK(name, init)	always @(posedge HCLK or negedge HRESETn) if(~HRESETn) name <= init;
`define		AHB_REG(name, init)		`AHB_BLOCK(name, init) else if(ahbl_we & (last_HADDR==``name``_ADDR)) name <= HWDATA;
`define		AHB_ICR(sz)				`AHB_BLOCK(ICR_REG, sz'b0) else if(ahbl_we & (last_HADDR==ICR_REG_ADDR)) ICR_REG <= HWDATA; else ICR_REG <= sz'd0;

module EF_PWM32_ahbl (
	output	wire 		pwmA,
	output	wire 		pwmB,
	input	wire 		HCLK,
	input	wire 		HRESETn,
	input	wire [31:0]	HADDR,
	input	wire 		HWRITE,
	input	wire [1:0]	HTRANS,
	input	wire 		HREADY,
	input	wire 		HSEL,
	input	wire [2:0]	HSIZE,
	input	wire [31:0]	HWDATA,
	output	wire [31:0]	HRDATA,
	output	wire 		HREADYOUT
);
	localparam[15:0] CMPA_REG_ADDR = 16'h0000;
	localparam[15:0] CMPB_REG_ADDR = 16'h0004;
	localparam[15:0] LOAD_REG_ADDR = 16'h0008;
	localparam[15:0] CLKDIV_REG_ADDR = 16'h000c;
	localparam[15:0] CONTROL_REG_ADDR = 16'h0010;
	localparam[15:0] GENA_REG_ADDR = 16'h0014;
	localparam[15:0] GENB_REG_ADDR = 16'h0018;

	reg             last_HSEL;
	reg [31:0]      last_HADDR;
	reg             last_HWRITE;
	reg [1:0]       last_HTRANS;

	always@ (posedge HCLK) begin
		if(HREADY) begin
			last_HSEL       <= HSEL;
			last_HADDR      <= HADDR;
			last_HWRITE     <= HWRITE;
			last_HTRANS     <= HTRANS;
		end
	end

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
	wire		ahbl_valid	= last_HSEL & last_HTRANS[1];
	wire		ahbl_we	= last_HWRITE & ahbl_valid;
	wire		ahbl_re	= ~last_HWRITE & ahbl_valid;
	wire		_clk_	= HCLK;
	wire		_rst_	= ~HRESETn;

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

	`AHB_REG(CMPA_REG, 0)
	`AHB_REG(CMPB_REG, 0)
	`AHB_REG(LOAD_REG, 0)
	`AHB_REG(CLKDIV_REG, 0)
	`AHB_REG(CONTROL_REG, 0)
	`AHB_REG(GENA_REG, 0)
	`AHB_REG(GENB_REG, 0)
	assign	HRDATA = 
			(last_HADDR == CMPA_REG_ADDR) ? CMPA_REG :
			(last_HADDR == CMPB_REG_ADDR) ? CMPB_REG :
			(last_HADDR == LOAD_REG_ADDR) ? LOAD_REG :
			(last_HADDR == CLKDIV_REG_ADDR) ? CLKDIV_REG :
			(last_HADDR == CONTROL_REG_ADDR) ? CONTROL_REG :
			(last_HADDR == GENA_REG_ADDR) ? GENA_REG :
			(last_HADDR == GENB_REG_ADDR) ? GENB_REG :
			32'hDEADBEEF;


	assign HREADYOUT = 1'b1;

endmodule