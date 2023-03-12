// programmable rate 1/2 convolutional encoder
// bitwise row of AND gates makes feedback pattern programmable
// N = 1 + constraint length
module conv_enc #(parameter N = 6)(// N = shift reg. length
  input                clk,
                       data_in,
				           reset,
  input        [  1:0] load_mask, // 1: load mask0 pattern; 2: load mask1 
  input        [N-1:0] mask,      // mask pattern to be loaded; prepend with 1  
  output logic [  1:0] data_out); // encoded data out
  
  logic [N-1:0] state_reg, 
					 mask_reg0, 
					 mask_reg1;
  
  always @(posedge clk, negedge reset) begin
		if (!reset)
			state_reg <= {N{1'b0}};
		else if (load_mask == 0) begin
			state_reg <= {data_in, state_reg[N-1:1]};			
		end
			
  end
  
  always @(posedge clk) begin
	if (load_mask[0])
		mask_reg0 <= mask;
	
	if (load_mask[1])
		mask_reg1 <= mask;
		
  end

  assign	data_out[0] = ^(state_reg & mask_reg0);
  assign data_out[1] = ^(state_reg & mask_reg1);
  
endmodule