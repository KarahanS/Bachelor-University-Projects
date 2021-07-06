`timescale 1ns / 1ns

module FSM(y, a, b, clk, rst);

output reg [1:0] y;   // y = y1y0
input wire a, b;
input wire rst;
input wire clk;

parameter S0 = 2'b00,
	S1 = 2'b01,
	S2 = 2'b10,
	S3 = 2'b11;
	
reg [1:0] stateReg;
reg [1:0] nextStateReg;

initial begin
	stateReg <= S0;
end

always@(a, b, stateReg) begin
	case(stateReg)
		S0: begin
			if(a == 0 && b == 0)
			begin
				nextStateReg <= S0;
				y = 2'b00;
			end
			else if(a == 0 && b == 1)
			begin 
				nextStateReg <= S1;
				y = 2'b01;
			end 
			else if(a == 1 && b == 0)
			begin 
				nextStateReg <= S2;
				y = 2'b10;
			end 
			else
			begin 
				nextStateReg <= S3;
				y = 2'b10;
			end 
		end
		S1: begin
			if(a == 0 && b== 0)
			begin 
				nextStateReg <= S0;
				y = 2'b00;
			end 
			else if(a == 0 && b == 1)
			begin 
				nextStateReg <= S0;
				y = 2'b01;
			end
			else 
			begin
				nextStateReg <= S2;
				y = 2'b10;
			end 
		end
		S2: begin
			if(a == 0 && b == 0)
			begin 
				nextStateReg <= S0;
				y = 2'b00;
			end 
			else if(a == 0 && b == 1)
			begin 
				nextStateReg <= S1;
				y = 2'b01;
			end 
			else if(a == 1 && b == 0)
			begin 
				nextStateReg <= S2;
				y = 2'b10;
			end 
			else
			begin 
				nextStateReg <= S1;
				y = 2'b01;
			end 
		end
		S3: begin
			nextStateReg <= S1;
			y = 2'b01;
		end
	endcase
end

always@(posedge clk) begin
	if(rst) begin
		stateReg <= S0;
	end
	else begin
		stateReg <= nextStateReg;
	end
end

endmodule
	