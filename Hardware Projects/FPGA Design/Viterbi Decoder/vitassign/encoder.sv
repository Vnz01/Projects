// figure out what this encoder does -- differs a bit from Homework 7
module encoder                    // use this one
(  input             clk,
   input             rst,
   input             enable_i,
   input             d_in,
   output logic      valid_o,
   output      [1:0] d_out);
   
   logic         [2:0] cstate;
   logic         [2:0] nstate;
   
   logic         [1:0] d_out_reg;

   assign   d_out    =  (enable_i)? d_out_reg:2'b00;

   always_comb begin
      valid_o  =   enable_i;
      case (cstate)
// fill in the guts
		3'b000 : begin
				 nstate = (d_in)? 3'b100:3'b000;
				 d_out_reg = (d_in)? 2'b11:2'b00;
				 end
		3'b001 : begin
				 nstate = (d_in)? 3'b000:3'b100;
				 d_out_reg = (d_in)? 2'b11:2'b00;
				 end
		3'b010 : begin
				 nstate = (d_in)? 3'b001:3'b101;
				 d_out_reg = (d_in)? 2'b01:2'b10;
				 end
		3'b011 : begin
				 nstate = (d_in)? 3'b101:3'b001;
				 d_out_reg = (d_in)? 2'b01:2'b10;
				 end
		3'b100 : begin
				 nstate = (d_in)? 3'b110:3'b010;
				 d_out_reg = (d_in)? 2'b01:2'b10;
				 end
		3'b101 : begin
				 nstate = (d_in)? 3'b010:3'b110;
				 d_out_reg = (d_in)? 2'b01:2'b10;
				 end
		3'b110 : begin
				 nstate = (d_in)? 3'b011:3'b111;
				 d_out_reg = (d_in)? 2'b11:2'b00;
				 end
		3'b111 : begin
				 nstate = (d_in)? 3'b111:3'b011;
				 d_out_reg = (d_in)? 2'b11:2'b00;
				 end
      endcase
   end								   

   always @ (posedge clk,negedge rst)   begin
//      $display("data in=%d state=%b%b%b data out=%b%b",d_in,reg_1,reg_2,reg_3,d_out_reg[1],d_out_reg[0]);
      if(!rst)
         cstate   <= 3'b000;
      else if(!enable_i)
         cstate   <= 3'b000;
      else
         cstate   <= nstate;
   end

endmodule
