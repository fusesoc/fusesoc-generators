module test_add;

  localparam period = 10;

  reg  clock;
  reg  [15:0] a, b;
  reg  [16:0] expected;

  wire [16:0] c;

  integer errors = 0, cycle_count = 0, total_cycles = 100;

  my_add dut (.clk (clock), .a (a), .b (b), .c (c));

  initial
  begin
    clock = 0;
    forever #(period/2) clock = ~clock;
  end

  // Stimulus
  always @(posedge clock)
  begin
    #1
    a = $urandom;
    b = $urandom;
    cycle_count = cycle_count + 1;
  end

  // Model
  always @(posedge clock)
  begin
    expected = a + b;
  end

  // Check results on the falling edge of the clock
  always @(negedge clock)
  begin

    if (cycle_count == total_cycles)
    begin
      $display("Finished simulation. Ran %d tests with %d errors.", cycle_count, errors);
      $finish;
    end

    if (c !== expected)
    begin
      errors = errors + 1;
      $display("Error! Got %d + %d = %d but expected %d", a, b, c, expected);
    end

  end

endmodule
