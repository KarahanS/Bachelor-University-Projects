`timescale 1ns / 1ns
module mul4x1(D0, I3, I2, I1, I0, S1, S0);

input I3, I2, I1, I0, S1, S0;
output D0;

reg D0;

always @(I3, I2, I1, I0, S1, S0)
begin
	if (S1==0 && S0==0)
	begin
		D0 <= I0;
	end
	else if (S1==0 && S0==1)
	begin
		D0 <= I1;
	end
	else if (S1==1 && S0==0)
	begin
		D0 <= I2;
	end
	else
	begin
		D0 <= I3;
	end
end

endmodule