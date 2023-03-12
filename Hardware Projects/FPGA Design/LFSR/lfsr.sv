//RTL Model for Linear Feedback Shift Register
module lfsr
#(parameter N = 4) // Number of bits for LFSR
(
  input logic clk, reset_n, load_seed,
  input logic[N-1:0] seed_data,
  output logic lfsr_done,
  output logic[N-1:0] lfsr_data
);
	
logic XOR_out;

always_comb 
begin
	XOR_out = 0;
	case(N)
	 2 : XOR_out = lfsr_data[1] ^ lfsr_data[0];
	 3 : XOR_out = lfsr_data[2] ^ lfsr_data[1];
	 4 : XOR_out = lfsr_data[3] ^ lfsr_data[2];
	 5 : XOR_out = lfsr_data[4] ^ lfsr_data[2];
	 6 : XOR_out = lfsr_data[5] ^ lfsr_data[4];
	 7 : XOR_out = lfsr_data[6] ^ lfsr_data[5];
	 8 : XOR_out = lfsr_data[7] ^ lfsr_data[5] ^ lfsr_data[4] ^ lfsr_data[3];
	 default : XOR_out = 0;
	endcase
end

always_ff@ (posedge clk or negedge reset_n) 
begin
	if(!reset_n)
	 lfsr_data <= 'h0;
	else
	begin
	 if(load_seed)
	 lfsr_data = seed_data;
	 else begin
	lfsr_data[N-1:0] = {lfsr_data[N-2:0], XOR_out};
	end	
end
end

assign lfsr_done = (lfsr_data == seed_data);

endmodule: lfsr
