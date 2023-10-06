/*
        Copyright 2023 efabless

        Author: Mohamed Shalan (mshalan@aucegypt.edu)

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

`timescale			    1ns/1ns
`default_nettype        none

module EF_PWM32_apb_tb;

    wire 		pwmA;
    wire 		pwmB;
    reg 		PCLK;
    reg 		PRESETn;
    reg [31:0]	PADDR;
    reg 		PWRITE;
    reg 		PSEL;
    reg 		PENABLE;
    reg [31:0]	PWDATA;
    wire [31:0]	PRDATA;
    wire 		PREADY;


    localparam[15:0] CMPA_REG_ADDR = 16'h0000;
	localparam[15:0] CMPB_REG_ADDR = 16'h0004;
	localparam[15:0] TOP_REG_ADDR = 16'h0008;
	localparam[15:0] CLKDIV_REG_ADDR = 16'h000c;
	localparam[15:0] CONTROL_REG_ADDR = 16'h0010;
	localparam[15:0] GENA_REG_ADDR = 16'h0014;
	localparam[15:0] GENB_REG_ADDR = 16'h0018;

    initial PCLK = 0;
    always #10 PCLK <= !PCLK;

    initial begin
        $dumpfile("EF_PWM32_apb_tb.vcd");
        $dumpvars(0, DUV);
    end

    EF_PWM32_apb DUV (
	    .pwmA(pwmA),
	    .pwmB(pwmB),
	    .PCLK(PCLK),
	    .PRESETn(PRESETn),
	    .PADDR(PADDR),
	    .PWRITE(PWRITE),
	    .PSEL(PSEL),
	    .PENABLE(PENABLE),
	    .PWDATA(PWDATA),
	    .PRDATA(PRDATA),
	    .PREADY(PREADY)
    );

    task apb_w_wr (input [31:0] address, input [31:0] data );
    begin
        @(posedge PCLK);
        PSEL = 1;
        PWRITE = 1;
        PWDATA = data;
        PENABLE = 0;
        PADDR = address;
        @(posedge PCLK);
        PENABLE = 1;
        @(posedge PCLK);
        PSEL = 0;
        PWRITE = 0;
        PENABLE = 0;
    end
    endtask
		
    task apb_w_rd(input [31:0] address, output [31:0] data );
    begin
        @(posedge PCLK);
        PSEL = 1;
        PWRITE = 0;
        PENABLE = 0;
        PADDR = address;
        @(posedge PCLK);
        PENABLE = 1;
        //@(posedge PREADY);
        wait(PREADY == 1)
        @(posedge PCLK) data = PRDATA;
        PSEL = 0;
        PWRITE = 0;
        PENABLE = 0;
    end
    endtask 
    
    initial begin
        PRESETn = 0;
        PADDR = 0;
        PWRITE = 0;
        PSEL = 0;
        PENABLE = 0;
        PWDATA = 0;
        #133;
        @(posedge PCLK) PRESETn = 1;
        apb_w_wr(CLKDIV_REG_ADDR, 4'b0010);
        apb_w_wr(TOP_REG_ADDR, 32'd12);
        apb_w_wr(CMPA_REG_ADDR, 32'd5);
        apb_w_wr(CMPB_REG_ADDR, 32'd5);
        apb_w_wr(GENA_REG_ADDR, 32'h009);
        apb_w_wr(GENB_REG_ADDR, 32'h009);
        apb_w_wr(CONTROL_REG_ADDR, 32'd7);
        #10_000;
        $finish;
    end

endmodule