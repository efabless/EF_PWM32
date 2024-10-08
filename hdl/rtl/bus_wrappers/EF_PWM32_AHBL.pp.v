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






























    






                                                
    



















module EF_PWM32_AHBL (




	input wire          HCLK,
                                        input wire          HRESETn,
                                        input wire          HWRITE,
                                        input wire [31:0]   HWDATA,
                                        input wire [31:0]   HADDR,
                                        input wire [1:0]    HTRANS,
                                        input wire          HSEL,
                                        input wire          HREADY,
                                        output wire         HREADYOUT,
                                        output wire [31:0]  HRDATA,
                                        output wire         IRQ
,
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
        .clk(HCLK),
        .clk_en(clk_gated_en),
        .clk_o(clk_g)
    );
    
	wire		clk = clk_g;
	wire		rst_n = HRESETn;


	reg  last_HSEL, last_HWRITE; reg [31:0] last_HADDR; reg [1:0] last_HTRANS;
                                        always@ (posedge HCLK or negedge HRESETn) begin
					   if(~HRESETn) begin
					       last_HSEL       <= 1'b0;
					       last_HADDR      <= 1'b0;
					       last_HWRITE     <= 1'b0;
					       last_HTRANS     <= 1'b0;
				            end else if(HREADY) begin
                                                last_HSEL       <= HSEL;
                                                last_HADDR      <= HADDR;
                                                last_HWRITE     <= HWRITE;
                                                last_HTRANS     <= HTRANS;
                                            end
                                        end
                                        wire    ahbl_valid	= last_HSEL & last_HTRANS[1];
	                                    wire	ahbl_we	= last_HWRITE & ahbl_valid;
	                                    wire	ahbl_re	= ~last_HWRITE & ahbl_valid;

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
	always @(posedge HCLK or negedge HRESETn) if(~HRESETn) CMPA_REG <= 0;
                                        else if(ahbl_we & (last_HADDR[16-1:0]==CMPA_REG_OFFSET))
                                            CMPA_REG <= HWDATA[32-1:0];

	reg [31:0]	CMPB_REG;
	assign	cmpB = CMPB_REG;
	always @(posedge HCLK or negedge HRESETn) if(~HRESETn) CMPB_REG <= 0;
                                        else if(ahbl_we & (last_HADDR[16-1:0]==CMPB_REG_OFFSET))
                                            CMPB_REG <= HWDATA[32-1:0];

	reg [31:0]	TOP_REG;
	assign	top = TOP_REG;
	always @(posedge HCLK or negedge HRESETn) if(~HRESETn) TOP_REG <= 0;
                                        else if(ahbl_we & (last_HADDR[16-1:0]==TOP_REG_OFFSET))
                                            TOP_REG <= HWDATA[32-1:0];

	reg [3:0]	CLKDIV_REG;
	assign	clkdiv = CLKDIV_REG;
	always @(posedge HCLK or negedge HRESETn) if(~HRESETn) CLKDIV_REG <= 0;
                                        else if(ahbl_we & (last_HADDR[16-1:0]==CLKDIV_REG_OFFSET))
                                            CLKDIV_REG <= HWDATA[4-1:0];

	reg [5:0]	CONTROL_REG;
	assign	en	=	CONTROL_REG[0 : 0];
	assign	enA	=	CONTROL_REG[1 : 1];
	assign	enB	=	CONTROL_REG[2 : 2];
	assign	invA	=	CONTROL_REG[3 : 3];
	assign	invB	=	CONTROL_REG[4 : 4];
	assign	cntr_mode	=	CONTROL_REG[5 : 5];
	always @(posedge HCLK or negedge HRESETn) if(~HRESETn) CONTROL_REG <= 0;
                                        else if(ahbl_we & (last_HADDR[16-1:0]==CONTROL_REG_OFFSET))
                                            CONTROL_REG <= HWDATA[6-1:0];

	reg [11:0]	GENA_REG;
	assign	pwmA_e0a	=	GENA_REG[1 : 0];
	assign	pwmA_e1a	=	GENA_REG[3 : 2];
	assign	pwmA_e2a	=	GENA_REG[5 : 4];
	assign	pwmA_e3a	=	GENA_REG[7 : 6];
	assign	pwmA_e4a	=	GENA_REG[9 : 8];
	assign	pwmA_e5a	=	GENA_REG[11 : 10];
	always @(posedge HCLK or negedge HRESETn) if(~HRESETn) GENA_REG <= 0;
                                        else if(ahbl_we & (last_HADDR[16-1:0]==GENA_REG_OFFSET))
                                            GENA_REG <= HWDATA[12-1:0];

	reg [11:0]	GENB_REG;
	assign	pwmB_e0a	=	GENB_REG[1 : 0];
	assign	pwmB_e1a	=	GENB_REG[3 : 2];
	assign	pwmB_e2a	=	GENB_REG[5 : 4];
	assign	pwmB_e3a	=	GENB_REG[7 : 6];
	assign	pwmB_e4a	=	GENB_REG[9 : 8];
	assign	pwmB_e5a	=	GENB_REG[11 : 10];
	always @(posedge HCLK or negedge HRESETn) if(~HRESETn) GENB_REG <= 0;
                                        else if(ahbl_we & (last_HADDR[16-1:0]==GENB_REG_OFFSET))
                                            GENB_REG <= HWDATA[12-1:0];

	localparam	GCLK_REG_OFFSET = 16'hFF10;
	always @(posedge HCLK or negedge HRESETn) if(~HRESETn) GCLK_REG <= 0;
                                        else if(ahbl_we & (last_HADDR[16-1:0]==GCLK_REG_OFFSET))
                                            GCLK_REG <= HWDATA[1-1:0];

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

	assign	HRDATA = 
			(last_HADDR[16-1:0] == CMPA_REG_OFFSET)	? CMPA_REG :
			(last_HADDR[16-1:0] == CMPB_REG_OFFSET)	? CMPB_REG :
			(last_HADDR[16-1:0] == TOP_REG_OFFSET)	? TOP_REG :
			(last_HADDR[16-1:0] == CLKDIV_REG_OFFSET)	? CLKDIV_REG :
			(last_HADDR[16-1:0] == CONTROL_REG_OFFSET)	? CONTROL_REG :
			(last_HADDR[16-1:0] == GENA_REG_OFFSET)	? GENA_REG :
			(last_HADDR[16-1:0] == GENB_REG_OFFSET)	? GENB_REG :
			(last_HADDR[16-1:0] == GCLK_REG_OFFSET)	? GCLK_REG :
			32'hDEADBEEF;

	assign	HREADYOUT = 1'b1;

endmodule
