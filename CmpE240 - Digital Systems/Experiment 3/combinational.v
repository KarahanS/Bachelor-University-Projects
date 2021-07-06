`timescale 1ns/1ns
module combinational(n2, n1, n0, y, s2, s1, s0, x);

  input s2, s1, s0, x;
  output n2, n1, n0;
  output [1:0]y;

  wire not0, not1, not2, notx;
  not(not0, s0);
  not(not1, s1);
  not(not2, s2);
  not(notx, x);

  // and wires
  wire a, b, c, d, e, f, g, h, i, j, k, l;

  // n2
  and(a, s1, not2, notx);
  and(b, s1, s0, not2);
  and(c, s2, not1, not0);
  or(n2, a, b, c);

  // n1 
  and(d, not1, s0, x);
  and(e, s1, s2, x);
  and(f, not0, s1, x);
  or(n1, a, d, e, f);

  // n0
  and(g, not0, notx);
  and(h, s2, notx);
  and(i, not1, notx);
  and(j, not2, s1, not0);
  or(n0, h, h, i, j);

  // y1
  and(k, s2, s1, not0);
  and(l, s2, not1, s0);
  or(y[1], k, l);
  
  // y0
  and(y[0], s2, s0);


endmodule