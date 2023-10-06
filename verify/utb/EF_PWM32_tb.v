
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

module EF_PWM32_tb;
    reg  clk;
    reg  rst_n;
    wire pwmA;
    wire pwmB;
    reg [31:0] cmpA;
    reg [31:0] cmpB;
    reg [31:0] top;
    reg [ 3:0] clkdiv;
    reg cntr_mode;
    reg enA;
    reg enB;
    reg invA;
    reg invB;
    reg en;
    reg [1:0] pwmA_e0a;
    reg [1:0] pwmA_e1a;
    reg [1:0] pwmA_e2a;
    reg [1:0] pwmA_e3a;
    reg [1:0] pwmA_e4a;
    reg [1:0] pwmA_e5a;
    reg [1:0] pwmB_e0a;
    reg [1:0] pwmB_e1a;
    reg [1:0] pwmB_e2a;
    reg [1:0] pwmB_e3a;
    reg [1:0] pwmB_e4a;
    reg [1:0] pwmB_e5a;

    initial clk = 0;
    always #10 clk <= !clk;

    initial begin
        $dumpfile("pwm.vcd");
        $dumpvars;
    end

    
    initial begin
        rst_n = 0;
        clkdiv = 4'b0010;
        en = 0;
        top = 32'd12;
        cmpA = 32'd5;
        cmpB = 32'd9;
        cntr_mode = 0;
        enA = 1;
        enB = 0;
        invA = 0;
        invB = 0;
        pwmA_e0a = 2'd1;
        pwmA_e1a = 2'd2;
        pwmA_e2a = 2'd0;
        pwmA_e3a = 2'd0;

        pwmA_e4a = 2'd0;
        pwmA_e5a = 2'd0;

        pwmB_e0a = 2'd2;
        pwmB_e1a = 2'd0;
        pwmB_e2a = 2'd1;
        pwmB_e3a = 2'd0;

        pwmB_e4a = 2'd0;
        pwmB_e5a = 2'd0;
        #99;
        @(posedge clk) rst_n = 1;
        #999;
        @(posedge clk) en = 1;
        #999;
        @(posedge clk) clkdiv = 4'b0100;
        #999;
        @(posedge clk) clkdiv = 4'b1000;
        @(posedge clk) enB = 1'b1;
        #999;
        @(posedge clk) clkdiv = 4'b0001;
        cntr_mode = 1;
        pwmA_e0a = 2'd0;
        pwmA_e1a = 2'd1;
        pwmA_e2a = 2'd0;
        pwmA_e3a = 2'd0;

        pwmA_e4a = 2'd0;
        pwmA_e5a = 2'd2;

        pwmB_e0a = 2'd0;
        pwmB_e1a = 2'd0;
        pwmB_e2a = 2'd2;
        pwmB_e3a = 2'd0;

        pwmB_e4a = 2'd1;
        pwmB_e5a = 2'd0;
        
        #4000;
        @(posedge clk) clkdiv = 4'b0001;
        pwmA_e0a = 2'd0;
        pwmA_e1a = 2'd1;
        pwmA_e2a = 2'd2;
        pwmA_e3a = 2'd1;
        pwmA_e4a = 2'd2;
        pwmA_e5a = 2'd3;
        pwmB_e0a = 2'd0;
        pwmB_e1a = 2'd1;
        pwmB_e2a = 2'd2;
        pwmB_e3a = 2'd1;
        pwmB_e4a = 2'd2;
        pwmB_e5a = 2'd3;
        #3000;
        @(posedge clk) enA = 0;
        @(posedge clk) enB = 0;
        @(posedge clk) en = 0;
        #1000;
        $finish;
    end

    EF_PWM32 duv (
        .clk(clk),
        .rst_n(rst_n),
        .pwmA(pwmA),
        .pwmB(pwmB),
        .cmpA(cmpA),
        .cmpB(cmpB),
        .top(top),
        .clkdiv(clkdiv),
        .cntr_mode(cntr_mode),
        .enA(enA),
        .enB(enB),
        .invA(invA),
        .invB(invB),
        .en(en),
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

endmodule