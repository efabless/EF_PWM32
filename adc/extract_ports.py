"""
    input  wire [2:0]                channel,
    input  wire [3:0]                swidth,
    input  wire [CLKDIV_WIDTH-1:0]   clkdiv, 
    input  wire [CLKDIV_WIDTH-1:0]   sample_div, 
    input  wire                      en,
    input  wire                      cmp,
    input  wire                      soc, 
    output wire                     sample,
    output wire                     eoc, 
    output wire [7:0]               data,
    input  wire                     rd,
    output wire [2:0]               ch_sel_out,
    input  wire [2:0]               ch_sel_in,
    input  wire [4:0]               seq0,
    input  wire [4:0]               seq1,
    input  wire [4:0]               seq2,
    input  wire [4:0]               seq3,
    input  wire [4:0]               seq4,
    input  wire [4:0]               seq5,
    input  wire [4:0]               seq6,
    input  wire [4:0]               seq7,
    input  wire                     seq_en,
    output wire                     fifo_full,
    input  wire [3:0]               fifo_threshold,
    output wire                     fifo_above
"""
# Using readlines()
#{"name": "pwmA", "size": "1", "dir":"output"},

file1 = open('ef_sar_adc8.v', 'r')
Lines = file1.readlines()
    
count = 0
flag = False
for line in Lines:
    count += 1
    #print("Line{}: {}".format(count, line.strip()))
    if "module" in line:
        if flag == False: 
            #print(line)
            if "ef_sar_adc8" in line:
                flag = True
                #print("found")
    elif "endmodule" in line:
        flag = False
    elif flag==True:
        size = 1
        tokens = line.split()
        if "[" in line:
            size = 0
        if "input" in line or "output" in line:
            #print(tokens)
            print("{" + f"'name': '{tokens[-1]}', 'size': '{size}', 'dir' : '{tokens[0]}'" + "},")


    
