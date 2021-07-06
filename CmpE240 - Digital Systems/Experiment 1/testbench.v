`timescale 1ns / 1ns

module testbench();

reg x0, x1, x2;
wire y;

source s(y, x0, x1, x2);

initial begin
	$dumpfile("Diagram.vcd");
	$dumpvars(0, y, x0, x1, x2);

	x0 = 0;
	x1 = 0; 
	x2 = 0;
	#20; // 20 ns delay
	x0 = 1;
	x1 = 0; 
	x2 = 0;
	#20; // 20 ns delay  
	x0 = 0; 
	x1 = 1; 
	x2 = 0;
	#20; // 20 ns delay  
	x0 = 1; 
	x1 = 1; 
	x2 = 0;
	#20; // 20 ns delay  
	x0 = 0;
	x1 = 0; 
	x2 = 1;
	#20; // 20 ns delay 
	x0 = 1; 
	x1 = 0; 
	x2 = 1;
	#20; // 20 ns delay 
	x0 = 0; 
	x1 = 1; 
	x2 = 1;
	#20; // 20 ns delay 
	x0 = 1; 
	x1 = 1; 
	x2 = 1;
	#20; // Puts 20 ns delay
	$finish;

end



endmodule