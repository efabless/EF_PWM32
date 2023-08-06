/*
	Copyright 2023 Mohamed Shalan


*/


`timescale			1ns/1ns
`default_nettype	none

`define		AHB_BLOCK(name, init)	always @(posedge HCLK or negedge HRESETn) if(~HRESETn) name <= init;
`define		AHB_REG(name, init)		`AHB_BLOCK(name, init) else if(ahbl_we & (last_HADDR==``name``_ADDR)) name <= HWDATA;
`define		AHB_ICR(sz)				`AHB_BLOCK(ICR_REG, sz'b0) else if(ahbl_we & (last_HADDR==ICR_REG_ADDR)) ICR_REG <= HWDATA; else ICR_REG <= sz'd0;

module ef_sar_Adc8_ahbl (
	input	wire 		cmp,
	output	wire 		sample,
	output	wire 		eoc,
	output	wire 		ch_sel,
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
	output	wire 		HREADYOUT,
	output	wire 		irq
);
	localparam[15:0] TCTRL_REG_ADDR = 16'h0000;
	localparam[15:0] CHSEL_REG_ADDR = 16'h0004;
	localparam[15:0] CHSEL_REG_ADDR = 16'h0008;
	localparam[15:0] CTRL_REG_ADDR = 16'h000c;
	localparam[15:0] SOC_REG_ADDR = 16'h0010;
	localparam[15:0] SEQCTRL0_REG_ADDR = 16'h0014;
	localparam[15:0] SEQCTRL1_REG_ADDR = 16'h0018;
	localparam[15:0] DATA_REG_ADDR = 16'h001c;
	localparam[15:0] FIFOTHRESHOLD_REG_ADDR = 16'h0020;
	localparam[15:0] ICR_REG_ADDR = 16'h0f00;
	localparam[15:0] RIS_REG_ADDR = 16'h0f04;
	localparam[15:0] IM_REG_ADDR = 16'h0f08;
	localparam[15:0] MIS_REG_ADDR = 16'h0f0c;

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

	reg	[31:0]	TCTRL_REG;
	reg	[2:0]	CHSEL_REG;
	reg	[2:0]	CHSEL_REG;
	reg	[1:0]	CTRL_REG;
	reg			SOC_REG;
	reg	[31:0]	SEQCTRL0_REG;
	reg	[31:0]	SEQCTRL1_REG;
	reg	[3:0]	FIFOTHRESHOLD_REG;
	reg	[2:0]	RIS_REG;
	reg	[2:0]	ICR_REG;
	reg	[2:0]	IM_REG;

	wire[7:0]	clkdiv	= TCTRL_REG[7:0];
	wire[7:0]	sample_div	= TCTRL_REG[15:8];
	wire[3:0]	swidth	= TCTRL_REG[19:16];
	wire[2:0]	ch_sel_in	= CHSEL_REG[2:0];
	wire[2:0]	ch_sel_in	= CHSEL_REG[2:0];
	wire		en	= CTRL_REG[0:0];
	wire		seq_en	= CTRL_REG[1:1];
	wire		soc	= SOC_REG[0:0];
	wire[4:0]	seq0	= SEQCTRL0_REG[4:0];
	wire[4:0]	seq1	= SEQCTRL0_REG[12:8];
	wire[4:0]	seq2	= SEQCTRL0_REG[20:16];
	wire[4:0]	seq3	= SEQCTRL0_REG[28:24];
	wire[4:0]	seq4	= SEQCTRL1_REG[4:0];
	wire[4:0]	seq5	= SEQCTRL1_REG[12:8];
	wire[4:0]	seq6	= SEQCTRL1_REG[20:16];
	wire[4:0]	seq7	= SEQCTRL1_REG[28:24];
	wire[7:0]	data;
	wire[7:0]	DATA_REG	= data;
	wire[7:0]	fifo_threshold	= FIFOTHRESHOLD_REG[7:0];
	wire		fifo_full;
	wire		_FIFO_FULL_FLAG_	= fifo_full;
	wire		fifo_above;
	wire		_FIFO_LEVEL_FLAG_	= fifo_above;
	wire		eoc;
	wire		_EOC_FLAG_	= eoc;
	wire[2:0]	MIS_REG	= RIS_REG & IM_REG;
	wire		ch_sel_out	= ch_sel;
	wire		ahbl_valid	= last_HSEL & last_HTRANS[1];
	wire		ahbl_we	= last_HWRITE & ahbl_valid;
	wire		ahbl_re	= ~last_HWRITE & ahbl_valid;
	wire		_clk_	= HCLK;
	wire		_rst_	= ~HRESETn;

	ef_sar_Adc8 inst_to_wrap (
		.clk(_clk_),
		.rst_n(~_rst_),
		.swidth(swidth),
		.clkdiv(clkdiv),
		.sample_div(sample_div),
		.en(en),
		.cmp(cmp),
		.soc(soc),
		.sample(sample),
		.eoc(eoc),
		.data(data),
		.rd(rd),
		.ch_sel_out(ch_sel_out),
		.ch_sel_in(ch_sel_in),
		.seq0(seq0),
		.seq1(seq1),
		.seq2(seq2),
		.seq3(seq3),
		.seq4(seq4),
		.seq5(seq5),
		.seq6(seq6),
		.seq7(seq7),
		.seq_en(seq_en),
		.fifo_full(fifo_full),
		.fifo_threshold(fifo_threshold),
		.fifo_above(fifo_above)
	);

	wire		rd	= (ahbl_re & (last_HADDR==DATA_REG_ADDR));
	`AHB_REG(TCTRL_REG, 0)
	`AHB_REG(CHSEL_REG, 0)
	`AHB_REG(CHSEL_REG, 0)
	`AHB_REG(CTRL_REG, 0)
	`AHB_REG(SOC_REG, 0)
	`AHB_REG(SEQCTRL0_REG, 0)
	`AHB_REG(SEQCTRL1_REG, 0)
	`AHB_REG(FIFOTHRESHOLD_REG, 0)

	`AHB_ICR(3)

	always @(posedge HCLK or negedge HRESETn)
		if(~HRESETn) RIS_REG <= 32'd0;
		else begin
			if(_FIFO_FULL_FLAG_) RIS_REG[0] <= 1'b1; else if(ICR_REG[0]) RIS_REG[0] <= 1'b0;
			if(_FIFO_LEVEL_FLAG_) RIS_REG[1] <= 1'b1; else if(ICR_REG[1]) RIS_REG[1] <= 1'b0;
			if(_EOC_FLAG_) RIS_REG[2] <= 1'b1; else if(ICR_REG[2]) RIS_REG[2] <= 1'b0;

		end

	assign irq = |MIS_REG;

	assign	HRDATA = 
			(last_HADDR == TCTRL_REG_ADDR) ? TCTRL_REG :
			(last_HADDR == CHSEL_REG_ADDR) ? CHSEL_REG :
			(last_HADDR == CHSEL_REG_ADDR) ? CHSEL_REG :
			(last_HADDR == CTRL_REG_ADDR) ? CTRL_REG :
			(last_HADDR == SOC_REG_ADDR) ? SOC_REG :
			(last_HADDR == SEQCTRL0_REG_ADDR) ? SEQCTRL0_REG :
			(last_HADDR == SEQCTRL1_REG_ADDR) ? SEQCTRL1_REG :
			(last_HADDR == FIFOTHRESHOLD_REG_ADDR) ? FIFOTHRESHOLD_REG :
			(last_HADDR == RIS_REG_ADDR) ? RIS_REG :
			(last_HADDR == ICR_REG_ADDR) ? ICR_REG :
			(last_HADDR == IM_REG_ADDR) ? IM_REG :
			(last_HADDR == DATA_REG_ADDR) ? DATA_REG :
			(last_HADDR == MIS_REG_ADDR) ? MIS_REG :
			32'hDEADBEEF;


	assign HREADYOUT = 1'b1;

endmodule
