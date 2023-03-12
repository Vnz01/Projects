// Barrel Shifter RTL Model
module barrel_shifter (
  input logic select,  // select=0 shift operation, select=1 rotate operation
  input logic direction, // direction=0 right move, direction=1 left move
  input logic[1:0] shift_value, // number of bits to be shifted (0, 1, 2 or 3)
  input logic[3:0] din,
  output logic[3:0] dout
);

  logic [3:0] inv_din;
  logic [3:0] inv_dout;
logic [3:0] r_dout;
  logic mmux31, mmux21, mmux71, mux0mux4, mux1mux5, mux2mux6, mux3mux7;

  always_comb begin
	if(direction == 1) begin
       inv_din[0] <= din[3];
       inv_din[1] <= din[2];  
       inv_din[2] <= din[1];
       inv_din[3] <= din[0];
  end else begin
       inv_din[0] <= din[0];
       inv_din[1] <= din[1];  
       inv_din[2] <= din[2];
       inv_din[3] <= din[3];
  end
end

always_comb begin
if (select == 0) begin
mmux21 <= 0;
mmux31 <= 0;
mmux71 <= 0;
end else begin
mmux21 <= inv_din[0];
mmux31 <= inv_din[1];
mmux71 <= mux0mux4;
end
end


always_comb begin
if(direction == 1) begin
	dout[0] <= inv_dout[0];
	dout[1] <= inv_dout[1];  
	dout[2] <= inv_dout[2];
	dout[3] <= inv_dout[3];
end else begin
	dout[0] <= inv_dout[3];
	dout[1] <= inv_dout[2];  
	dout[2] <= inv_dout[1];
	dout[3] <= inv_dout[0];
end
end

mux_2x1 m0 (.in0(inv_din[0]),.in1(inv_din[2]),.sel(shift_value[1]),.out(mux0mux4));
mux_2x1 m1 (.in0(inv_din[1]),.in1(inv_din[3]),.sel(shift_value[1]),.out(mux1mux5));
mux_2x1 m2 (.in0(inv_din[2]),.in1(mmux21),.sel(shift_value[1]),.out(mux2mux6));
mux_2x1 m3 (.in0(inv_din[3]),.in1(mmux31),.sel(shift_value[1]),.out(mux3mux7));
mux_2x1 m4 (.in0(mux0mux4),.in1(mux1mux5),.sel(shift_value[0]),.out(inv_dout[3]));
mux_2x1 m5 (.in0(mux1mux5),.in1(mux2mux6),.sel(shift_value[0]),.out(inv_dout[2]));
mux_2x1 m6 (.in0(mux2mux6),.in1(mux3mux7),.sel(shift_value[0]),.out(inv_dout[1]));
mux_2x1 m7 (.in0(mux3mux7),.in1(mmux71),.sel(shift_value[0]),.out(inv_dout[0]));

endmodule: barrel_shifter
