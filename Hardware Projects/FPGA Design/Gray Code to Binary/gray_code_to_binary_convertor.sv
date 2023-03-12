module gray_code_to_binary_convertor #(parameter N = 4)( 
  input logic clk, rstn, 
  input logic[N-1:0] gray_value,
  output logic[N-1:0] binary_value);
 
  always @(posedge clk or negedge rstn)
    begin
      binary_value[N-1] = gray_value[N-1];
	for (int i = N-2; i>=0; i--) begin
        binary_value[i] = gray_value[i] ^ binary_value[i+1];
	end
    end

endmodule: gray_code_to_binary_convertor
