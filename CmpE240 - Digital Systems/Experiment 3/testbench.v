`timescale 1ns/1ns
module testbench();

wire [1:0] y;
reg x;
reg rst;
reg clk;

source s(y, x, rst, clk);

parameter inputsequence0 = 32'b00110110111110011110001000110110,
inputsequence1 = 32'b11000001011000011110101001100111,
inputsequence2 = 32'b11011111001001111100111101110101,
inputsequence3 = 32'b10111110010101111010000101011000,
inputsequence4 = 32'b00111010111010000100101110000110;
integer i;



initial begin
    $dumpfile("TimingDiagram.vcd");
    $dumpvars(0, y, x, rst, clk);
    
    rst = 0;
    x = 0;
    #5
    rst = 1;
    x = 0;
    #30;
    rst = 0;
    
    for (i=31; i>=0; i--) begin
        x = inputsequence0[i];
        #40;
        
    end
    rst = 1;
    #30;
    rst = 0;
    for (i=31; i>=0; i--) begin
        x = inputsequence1[i];
        #40;
        
    end
    rst = 1;
    #30;
    rst = 0;
    for (i=31; i>=0; i--) begin
        x = inputsequence2[i];
        #40;
        
    end
    rst = 1;
    #30;
    rst = 0;
    for (i=31; i>=0; i--) begin
        x = inputsequence3[i];
        #40;
        
    end
    rst = 1;
    #30;
    rst = 0;
    for (i=31; i>=0; i--) begin
        x = inputsequence4[i];
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
