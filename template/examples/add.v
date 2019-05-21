module add #(
  parameter WIDTH = 16)
(
  input                  clk,
  input      [WIDTH-1:0] a, b,
  output reg [WIDTH:0]   c
);

  always @(posedge clk)
    c <= a + b;

endmodule
