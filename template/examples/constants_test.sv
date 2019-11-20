import constants_pkg::*;

module constants_test;

  initial
  begin
    $display("WORD_SIZE: %d",  word_size);
    $display("ITERATIONS: %d", iterations);
    $display("LOW_AREA: %d",   low_area);
    $display("IMPL: %s",       impl);
    $finish;
  end

endmodule

