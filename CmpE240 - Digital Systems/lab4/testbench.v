`timescale 1ns/1ns
module testbench();

wire [1:0] y;
reg a, b;
reg rst;
reg clk;
parameter inputa1 = 32'b11001010010001111111110111101010,
inputb1 = 32'b00011001011001001100101111100101,
inputa2 = 32'b10110100101101110011010111000001,
inputb2 = 32'b00100111111010001000001001010001,
inputa3 = 32'b00100011010101100000110100001111,
inputb3 = 32'b10101000101010001101111001001001,
inputa4 = 32'b11110010111010101000010101000001,
inputb4 = 32'b01011111011010111011111010111100,
inputa5 = 32'b00010010111101111001100001100111,
inputb5 = 32'b00110001011100010111101011110011;

integer i;

FSM fsm(y, a, b, clk, rst);

initial begin
    $dumpfile("TimingDiagram.vcd");
    $dumpvars(0, y, a, b, rst, clk, fsm);

    rst = 1;
    a = 0;
    b = 0;
    #30;
    rst = 0;
    
    for (i=31; i>=0; i--) begin
        a = inputa1[i];
        b = inputb1[i];
        #40;
    end
    for (i=31; i>=0; i--) begin
        a = inputa2[i];
        b = inputb2[i];
        #40;
    end
    for (i=31; i>=0; i--) begin
        a = inputa3[i];
        b = inputb3[i];
        #40;
    end
    for (i=31; i>=0; i--) begin
        a = inputa4[i];
        b = inputb4[i];
        #40;
    end
    for (i=31; i>=0; i--) begin
        a = inputa5[i];
        b = inputb5[i];
        #40;
    end
    
    $finish;
end

always begin    
    clk = 0;
    #20;
    clk = 1;
    #20;
end

endmodule
