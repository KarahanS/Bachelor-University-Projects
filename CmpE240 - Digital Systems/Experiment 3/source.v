`timescale 1ns/1ns

module source(y, x, reset, clock);

  output [1:0]y;
  input x, clock, reset;

  wire n2,n1,n0,s2,s1,s0;

  combinational comb(n2, n1, n0, y, s2, s1, s0, x);
  register register(s2, s1, s0, n2, n1, n0, reset, clock);

endmodule