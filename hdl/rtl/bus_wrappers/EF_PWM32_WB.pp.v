/*
	Copyright 2023 Efabless Corp.

	Author: Mohamed Shalan (mshalan@efabless.com)

	Licensed under the Apache License, Version 2.0 (the "License");
	you may not use this file except in compliance with the License.
	You may obtain a copy of the License at

	    http://www.apache.org/licenses/LICENSE-2.0

	Unless required by applicable law or agreed to in writing, software
	distributed under the License is distributed on an "AS IS" BASIS,
	WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
	See the License for the specific language governing permissions and
	limitations under the License.

*/

/* THIS FILE IS GENERATED, DO NOT EDIT */

`timescale			1ns/1ps
`default_nettype	none



/*
	Copyright 2020 AUCOHL

    Author: Mohamed Shalan (mshalan@aucegypt.edu)
	
	Licensed under the Apache License, Version 2.0 (the "License"); 
	you may not use this file except in compliance with the License. 
	You may obtain a copy of the License at:

	http://www.apache.org/licenses/LICENSE-2.0

	Unless required by applicable law or agreed to in writing, software 
	distributed under the License is distributed on an "AS IS" BASIS, 
	WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
	See the License for the specific language governing permissions and 
	limitations under the License.
*/
































                                        


module EF_PWM32_WB (




	input   wire            ext_clk,
                                        input   wire            clk_i,
                                        input   wire            rst_i,
                                        input   wire [31:0]     adr_i,
                                        input   wire [31:0]     dat_i,
                                        output  wire [31:0]     dat_o,
                                        input   wire [3:0]      sel_i,
                                        input   wire            cyc_i,
                                        input   wire            stb_i,
                                        output  reg             ack_o,
                                        input   wire            we_i,
                                        output  wire            IRQ,
	output	wire	[1-1:0]	pwmA,
	output	wire	[1-1:0]	pwmB
);

	localparam	CMPA_REG_OFFSET = 16'h0000;
	localparam	CMPB_REG_OFFSET = 16'h0004;
	localparam	TOP_REG_OFFSET = 16'h0008;
	localparam	CLKDIV_REG_OFFSET = 16'h000C;
	localparam	CONTROL_REG_OFFSET = 16'h0010;
	localparam	GENA_REG_OFFSET = 16'h0014;
	localparam	GENB_REG_OFFSET = 16'h0018;

    reg [0:0] GCLK_REG;
    wire clk_g;
    wire clk_gated_en = GCLK_REG[0];
    ef_gating_cell clk_gate_cell(
        


 // USE_POWER_PINS
        .clk(clk_i),
        .clk_en(clk_gated_en),
        .clk_o(clk_g)
    );
    
	wire		clk = clk_g;
	wire		rst_n = (~rst_i);


	wire            wb_valid    = cyc_i & stb_i;
                                        wire            wb_we       = we_i & wb_valid;
                                        wire            wb_re       = ~we_i & wb_valid;
                                        wire[3:0]       wb_byte_sel = sel_i & {4{wb_we}};

	wire [32-1:0]	cmpA;
	wire [32-1:0]	cmpB;
	wire [32-1:0]	top;
	wire [4-1:0]	clkdiv;
	wire [1-1:0]	cntr_mode;
	wire [1-1:0]	enA;
	wire [1-1:0]	enB;
	wire [1-1:0]	en;
	wire [1-1:0]	invA;
	wire [1-1:0]	invB;
	wire [2-1:0]	pwmA_e0a;
	wire [2-1:0]	pwmA_e1a;
	wire [2-1:0]	pwmA_e2a;
	wire [2-1:0]	pwmA_e3a;
	wire [2-1:0]	pwmA_e4a;
	wire [2-1:0]	pwmA_e5a;
	wire [2-1:0]	pwmB_e0a;
	wire [2-1:0]	pwmB_e1a;
	wire [2-1:0]	pwmB_e2a;
	wire [2-1:0]	pwmB_e3a;
	wire [2-1:0]	pwmB_e4a;
	wire [2-1:0]	pwmB_e5a;

	// Register Definitions
	reg [31:0]	CMPA_REG;
	assign	cmpA = CMPA_REG;
	always @(posedge clk_i or posedge rst_i) if(rst_i) CMPA_REG <= 0; else if(wb_we & (adr_i[16-1:0]==CMPA_REG_OFFSET)) CMPA_REG <= dat_i[32-1:0];

	reg [31:0]	CMPB_REG;
	assign	cmpB = CMPB_REG;
	always @(posedge clk_i or posedge rst_i) if(rst_i) CMPB_REG <= 0; else if(wb_we & (adr_i[16-1:0]==CMPB_REG_OFFSET)) CMPB_REG <= dat_i[32-1:0];

	reg [31:0]	TOP_REG;
	assign	top = TOP_REG;
	always @(posedge clk_i or posedge rst_i) if(rst_i) TOP_REG <= 0; else if(wb_we & (adr_i[16-1:0]==TOP_REG_OFFSET)) TOP_REG <= dat_i[32-1:0];

	reg [3:0]	CLKDIV_REG;
	assign	clkdiv = CLKDIV_REG;
	always @(posedge clk_i or posedge rst_i) if(rst_i) CLKDIV_REG <= 0; else if(wb_we & (adr_i[16-1:0]==CLKDIV_REG_OFFSET)) CLKDIV_REG <= dat_i[4-1:0];

	reg [5:0]	CONTROL_REG;
	assign	en	=	CONTROL_REG[0 : 0];
	assign	enA	=	CONTROL_REG[1 : 1];
	assign	enB	=	CONTROL_REG[2 : 2];
	assign	invA	=	CONTROL_REG[3 : 3];
	assign	invB	=	CONTROL_REG[4 : 4];
	assign	cntr_mode	=	CONTROL_REG[5 : 5];
	always @(posedge clk_i or posedge rst_i) if(rst_i) CONTROL_REG <= 0; else if(wb_we & (adr_i[16-1:0]==CONTROL_REG_OFFSET)) CONTROL_REG <= dat_i[6-1:0];

	reg [11:0]	GENA_REG;
	assign	pwmA_e0a	=	GENA_REG[1 : 0];
	assign	pwmA_e1a	=	GENA_REG[3 : 2];
	assign	pwmA_e2a	=	GENA_REG[5 : 4];
	assign	pwmA_e3a	=	GENA_REG[7 : 6];
	assign	pwmA_e4a	=	GENA_REG[9 : 8];
	assign	pwmA_e5a	=	GENA_REG[11 : 10];
	always @(posedge clk_i or posedge rst_i) if(rst_i) GENA_REG <= 0; else if(wb_we & (adr_i[16-1:0]==GENA_REG_OFFSET)) GENA_REG <= dat_i[12-1:0];

	reg [11:0]	GENB_REG;
	assign	pwmB_e0a	=	GENB_REG[1 : 0];
	assign	pwmB_e1a	=	GENB_REG[3 : 2];
	assign	pwmB_e2a	=	GENB_REG[5 : 4];
	assign	pwmB_e3a	=	GENB_REG[7 : 6];
	assign	pwmB_e4a	=	GENB_REG[9 : 8];
	assign	pwmB_e5a	=	GENB_REG[11 : 10];
	always @(posedge clk_i or posedge rst_i) if(rst_i) GENB_REG <= 0; else if(wb_we & (adr_i[16-1:0]==GENB_REG_OFFSET)) GENB_REG <= dat_i[12-1:0];

	localparam	GCLK_REG_OFFSET = 16'hFF10;
	always @(posedge clk_i or posedge rst_i) if(rst_i) GCLK_REG <= 0; else if(wb_we & (adr_i[16-1:0]==GCLK_REG_OFFSET)) GCLK_REG <= dat_i[1-1:0];

	EF_PWM32 instance_to_wrap (
		.clk(clk),
		.rst_n(rst_n),
		.cmpA(cmpA),
		.cmpB(cmpB),
		.top(top),
		.clkdiv(clkdiv),
		.cntr_mode(cntr_mode),
		.enA(enA),
		.enB(enB),
		.en(en),
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
		.pwmB_e5a(pwmB_e5a),
		.pwmA(pwmA),
		.pwmB(pwmB)
	);

	assign	dat_o = 
			(adr_i[16-1:0] == CMPA_REG_OFFSET)	? CMPA_REG :
			(adr_i[16-1:0] == CMPB_REG_OFFSET)	? CMPB_REG :
			(adr_i[16-1:0] == TOP_REG_OFFSET)	? TOP_REG :
			(adr_i[16-1:0] == CLKDIV_REG_OFFSET)	? CLKDIV_REG :
			(adr_i[16-1:0] == CONTROL_REG_OFFSET)	? CONTROL_REG :
			(adr_i[16-1:0] == GENA_REG_OFFSET)	? GENA_REG :
			(adr_i[16-1:0] == GENB_REG_OFFSET)	? GENB_REG :
			32'hDEADBEEF;

	always @ (posedge clk_i or posedge rst_i)
		if(rst_i)
			ack_o <= 1'b0;
		else if(wb_valid & ~ack_o)
			ack_o <= 1'b1;
		else
			ack_o <= 1'b0;
endmodule
