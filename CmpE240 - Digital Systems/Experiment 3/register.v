`timescale 1ns/1ns
module register(s2, s1, s0, n2, n1, n0, reset, clock);

	input reset, clock, n2, n1, n0;
	output reg s2, s1, s0;


    // When it is reset, states will be updated.
	always @(posedge clock)
		if(reset)
			begin
				s2 = 0;
				s1 = 0;
				s0 = 0;
			end
		else 
			begin 
				s2 = n2;
				s1 = n1;
				s0 = n0;
			end


endmodule