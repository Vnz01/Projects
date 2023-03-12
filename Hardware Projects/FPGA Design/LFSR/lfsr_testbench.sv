`timescale 1ns/1ns
//LFSR Testbench Code
module lfsr_testbench;
  parameter N = 4;
  logic clock;
  logic [N-1:0] lfsr_data, seed_data;
  logic lfsr_done;
  logic reset_n, load_seed;
   
  lfsr #(.N(N)) design_inst(
   .clk(clock),
   .reset_n(reset_n),
   .load_seed(load_seed),
   .seed_data(seed_data),
   .lfsr_data(lfsr_data),
   .lfsr_done(lfsr_done)
  );
  
  initial begin
   // Initialize Inputs
   reset_n = 0;
   load_seed = 0;
   clock = 0;
   seed_data = {N{1'b0}};

   // Wait 10 ns for global reset_n to finish and start counter
   #15;
   reset_n = 1;

   #10;
   load_seed = 1;
   seed_data = {N{1'b1}}; //Change value to change seed
   // seed_data = {N{1'b0}};

   #20;
   load_seed = 0;

	for (int i=0 ; i <2**(N-2) ; i++)
	begin
		#160;
	end
   // terminate simulation
   $stop();
  end

  // Clock generator logic
  always@(clock) begin
    #10ns clock <= !clock;
  end

  // Print input and output signals
  always@(posedge clock or reset_n or load_seed) begin
   $display(" time=%0t,  reset_n=%b  clk=%b  load_seed=%b  count=%d  lfsr_done=%b", $time, reset_n, clock, load_seed, lfsr_data, lfsr_done);
  end

endmodule