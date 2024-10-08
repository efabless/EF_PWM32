`timescale 1ns/1ps

module top();
wire pwmA;
wire pwmB;
wire PCLK;
wire PRESETn;
wire [31:0] PADDR;
wire PWRITE;
wire PSEL;
wire PENABLE;
wire [31:0] PWDATA;
wire [31:0] PRDATA;
wire PREADY;

EF_PWM32_apb uut(
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

`ifndef SKIP_WAVE_DUMP
initial begin
    $dumpfile("waves.vcd");
    $dumpvars(0, top);
end
`endif

always #10 PCLK = !PCLK;

endmodule