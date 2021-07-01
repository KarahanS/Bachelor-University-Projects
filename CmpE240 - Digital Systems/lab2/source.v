`timescale 1ns / 1ns
module source(y, x3, x2, x1, x0);

input x3, x2, x1, x0;
output y;

wire w1, w2;

and A(w1, x1, x0);

xor X(w2, x1, x0);

mul4x1 mul(y, w2, x1, x0, w1, x3, x2);



endmodule