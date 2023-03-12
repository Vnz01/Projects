module clock_divide_by_3( 
  input  logic clkin, reset,
  output logic clkout);

 logic cnt = 1;
 logic [1:0] ctr, rctr;

 always_ff@(posedge clkin) begin
  if (reset) begin
  	ctr <= 0;
  end
  else if(ctr == 2) begin
  	ctr <= 0;
  end
  else begin
	if(!cnt) begin
  	ctr <= ctr + 1;
  	end else begin
	ctr <= 2;
	cnt <= 0;
	end
  end
  end

 always_ff@(negedge clkin) begin
  if (reset) begin
  	rctr <= 0;
  end
  else if(rctr == 2) begin
  	rctr <= 0;
  end  
  else begin
  	rctr <= rctr + 1;
  end
  end

  assign clkout = ((ctr == 2)|(rctr == 2));

endmodule: clock_divide_by_3
