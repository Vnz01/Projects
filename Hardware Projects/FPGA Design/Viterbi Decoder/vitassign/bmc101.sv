module bmc101			  
(
   input    [1:0] rx_pair,
   output   [1:0] path_0_bmc,
   output   [1:0] path_1_bmc);

logic tmp01 = rx_pair[0];
logic tmp00 = rx_pair[1];
logic tmp10;
logic tmp11;

assign tmp10 = !tmp00;
assign tmp11 = !tmp01;

assign path_0_bmc[1] = tmp00 & tmp01;
assign path_0_bmc[0] = tmp00 ^ tmp01;
assign path_1_bmc[1] = tmp10 & tmp11;
assign path_1_bmc[0] = tmp10 & tmp11;
endmodule

