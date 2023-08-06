module ef_pwm32(
    input wire  clk,
    input wire  rst_n,
    output wire pwmA,
    output wire pwmB,
    input wire [31:0] cmpA,
    input wire [31:0] cmpB,
    input wire [31:0] load,
    input wire [ 3:0] clkdiv,
    input wire cntr_mode,
    input wire enA,
    input wire enB,
    input wire invA,
    input wire invB,
    input wire en,
    input wire [1:0] pwmA_e0a,
    input wire [1:0] pwmA_e1a,
    input wire [1:0] pwmA_e2a,
    input wire [1:0] pwmA_e3a,
    input wire [1:0] pwmA_e4a,
    input wire [1:0] pwmA_e5a,
    input wire [1:0] pwmB_e0a,
    input wire [1:0] pwmB_e1a,
    input wire [1:0] pwmB_e2a,
    input wire [1:0] pwmB_e3a,
    input wire [1:0] pwmB_e4a,
    input wire [1:0] pwmB_e5a
);
    reg [31:0] cntr;
    reg [ 3:0] clkdiv_ctr;
    always @(posedge clk or negedge rst_n)
        if(!rst_n)
            clkdiv_ctr <= 4'b0;
        else 
            clkdiv_ctr <= clkdiv_ctr + 4'b1;
    wire clkdiv2 = clkdiv[0];
    wire clkdiv4 = clkdiv[1] & (clkdiv_ctr[0] == 1'b1);
    wire clkdiv8 = clkdiv[2] & (clkdiv_ctr[1:0] == 2'b11);
    wire clkdiv16 = clkdiv[3] & (clkdiv_ctr[2:0] == 3'b111);
    reg clken;
    always @(posedge clk or negedge rst_n)
        if(!rst_n)
            clken <= 1'b0;
        else
            if(clken) 
                clken <= 1'b0;
            else 
                if(en) 
                    if(clkdiv2 | clkdiv4 | clkdiv8 | clkdiv16)
                        clken <= 1'b1;
    
    // the counter
    reg dir;
    wire cmp_load   = (cntr == load);
    wire cmp_zero   = (cntr == 32'd0);
    wire cmp_a      = (cntr == cmpA);
    wire cmp_b      = (cntr == cmpB);
    wire cmp_au     = cmp_a & ~dir;
    wire cmp_ad     = cmp_a & dir;
    wire cmp_bu     = cmp_b & ~dir;
    wire cmp_bd     = cmp_b & dir;
    
    always @(posedge clk or negedge rst_n)
        if(!rst_n) dir <= 1'b0;
        else if(cmp_zero) dir <= 1'b0;
        else if(cmp_load) dir <= 1'b1;
    
    always @(posedge clk or negedge rst_n)
        if(!rst_n) cntr <= 32'b0;
        else 
            if (clken) 
                if(cntr_mode) cntr <= dir ? cntr - 32'b1 : cntr + 32'b1;
                else 
                    if(cmp_load) cntr <= 32'd0; 
                    else cntr <= cntr + 32'b1;
    
    // PWM generation logic
    reg pwm_a, pwm_b;
    
    always @(posedge clk or negedge rst_n)
        if(!rst_n) pwm_a <= 1'b0;
        else if(clken) begin
            if(cmp_zero)
                case (pwmA_e0a)
                    2'b01: pwm_a <= 1'b1;
                    2'b10: pwm_a <= 1'b0;
                    2'b11: pwm_a <= ~pwm_a; 
                endcase
            else if(cmp_au)
                case (pwmA_e1a)
                    2'b01: pwm_a <= 1'b1;
                    2'b10: pwm_a <= 1'b0;
                    2'b11: pwm_a <= ~pwm_a; 
                endcase
            else if(cmp_bu)
                case (pwmA_e2a)
                    2'b01: pwm_a <= 1'b1;
                    2'b10: pwm_a <= 1'b0;
                    2'b11: pwm_a <= ~pwm_a; 
                endcase
            else if(cmp_load)
                case (pwmA_e3a)
                    2'b01: pwm_a <= 1'b1;
                    2'b10: pwm_a <= 1'b0;
                    2'b11: pwm_a <= ~pwm_a; 
                endcase
            else if(cmp_bd)
                case (pwmA_e4a)
                    2'b01: pwm_a <= 1'b1;
                    2'b10: pwm_a <= 1'b0;
                    2'b11: pwm_a <= ~pwm_a; 
                endcase
            else if(cmp_ad)
                case (pwmA_e5a)
                    2'b01: pwm_a <= 1'b1;
                    2'b10: pwm_a <= 1'b0;
                    2'b11: pwm_a <= ~pwm_a; 
                endcase
        end

    always @(posedge clk or negedge rst_n)
        if(!rst_n) pwm_b <= 1'b0;
        else if(clken) begin
            if(cmp_zero)
                case (pwmB_e0a)
                    2'b01: pwm_b <= 1'b1;
                    2'b10: pwm_b <= 1'b0;
                    2'b11: pwm_b <= ~pwm_a; 
                endcase
            else if(cmp_au)
                case (pwmB_e1a)
                    2'b01: pwm_b <= 1'b1;
                    2'b10: pwm_b <= 1'b0;
                    2'b11: pwm_b <= ~pwm_a; 
                endcase
            else if(cmp_bu)
                case (pwmB_e2a)
                    2'b01: pwm_b <= 1'b1;
                    2'b10: pwm_b <= 1'b0;
                    2'b11: pwm_b <= ~pwm_a; 
                endcase
            else if(cmp_load)
                case (pwmB_e3a)
                    2'b01: pwm_b <= 1'b1;
                    2'b10: pwm_b <= 1'b0;
                    2'b11: pwm_b <= ~pwm_a; 
                endcase
            else if(cmp_bd)
                case (pwmB_e4a)
                    2'b01: pwm_b <= 1'b1;
                    2'b10: pwm_b <= 1'b0;
                    2'b11: pwm_b <= ~pwm_a; 
                endcase
            else if(cmp_ad)
                case (pwmB_e5a)
                    2'b01: pwm_b <= 1'b1;
                    2'b10: pwm_b <= 1'b0;
                    2'b11: pwm_b <= ~pwm_a; 
                endcase
        end

        assign pwmA = invA ? ~pwm_a : pwm_a;
        assign pwmB = invB ? ~pwm_b : pwm_b;
        
endmodule

