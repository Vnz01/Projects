module ACS		                        // add-compare-select
(
   input       path_0_valid,
   input       path_1_valid,
   input [1:0] path_0_bmc,	            // branch metric computation
   input [1:0] path_1_bmc,				
   input [7:0] path_0_pmc,				// path metric computation
   input [7:0] path_1_pmc,

   output logic        selection,
   output logic        valid_o,
   output logic      [7:0] path_cost);  

   wire  [7:0] path_cost_0;			   // branch metric + path metric
   wire  [7:0] path_cost_1;

/* Fill in the guts per ACS instructions
*/

	assign path_cost_0 = path_0_pmc + path_0_bmc;
	assign path_cost_1 = path_1_pmc + path_1_bmc;

	always_comb begin
		if (valid_o) begin
			if (selection)
				path_cost[7:0] = path_cost_1[7:0];
			else 
				path_cost[7:0] = path_cost_0[7:0];
		end
		else
			path_cost[7:0] = 7'd0;
	end
	
	always_comb begin
		if (!path_0_valid) begin
			if (!path_1_valid)
				selection = 0;
			else
				selection = 1;
		end
		else begin
			if (!path_1_valid)
				selection = 0;
			else
				selection = (path_cost_0 > path_cost_1);
		end
	end
	assign valid_o = (path_0_valid==0 && path_1_valid==0) ? 0 : 1;
endmodule
