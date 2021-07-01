`timescale 1ns / 1ns
module source(y, x0, x1, x2);

input x0, x1, x2;
output y;

wire w1, w2, w3;
wire nx0, nx1, nx2;

not(nx2, x2);
and A1(w1, nx2, x1);

not(nx0, x0);
and A2(w2, w1, nx0);

not(nx1, x1);
and A3(w3, nx1, x2);

or O(y, w2, w3);


endmodule