`timescale 1ns / 1ns
module testbench();

reg x3, x2, x1, x0;
wire y;

source s(y, x3, x2, x1, x0);

initial begin
	$dumpfile("Diagram.vcd");
	$dumpvars(0, y, x3, x2, x1, x0);

	x3 = 0; x2 = 0; x1 = 0; x0 = 0;
	#20; // 20 ns delay
	x3 = 0; x2 = 0; x1 = 0; x0 = 1;
	#20; // 20 ns delay  
	x3 = 0; x2 = 0; x1 = 1; x0 = 0;
	#20; // 20 ns delay  
	x3 = 0; x2 = 0; x1 = 1; x0 = 1;
	#20; // 20 ns delay  
	x3 = 0; x2 = 1; x1 = 0; x0 = 0;
	#20; // 20 ns delay 
	x3 = 0; x2 = 1; x1 = 0; x0 = 1;
	#20; // 20 ns delay 
	x3 = 0; x2 = 1; x1 = 1; x0 = 0;
	#20; // 20 ns delay 
	x3 = 0; x2 = 1; x1 = 1; x0 = 1;
	#20; // Puts 20 ns delay
	x3 = 1; x2 = 0; x1 = 0; x0 = 0;
	#20; // 20 ns delay
	x3 = 1; x2 = 0; x1 = 0; x0 = 1;
	#20; // 20 ns delay  
	x3 = 1; x2 = 0; x1 = 1; x0 = 0;
	#20; // 20 ns delay  
	x3 = 1; x2 = 0; x1 = 1; x0 = 1;
	#20; // 20 ns delay  
	x3 = 1; x2 = 1; x1 = 0; x0 = 0;
	#20; // 20 ns delay 
	x3 = 1; x2 = 1; x1 = 0; x0 = 1;
	#20; // 20 ns delay 
	x3 = 1; x2 = 1; x1 = 1; x0 = 0;
	#20; // 20 ns delay 
	x3 = 1; x2 = 1; x1 = 1; x0 = 1;
	#20; // Puts 20 ns delay
	$finish;

end



endmodule