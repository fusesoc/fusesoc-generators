USE work.constants_pkg.ALL;

ENTITY constants_test IS
END ENTITY;

ARCHITECTURE test OF constants_test IS
BEGIN

  sim : PROCESS
  BEGIN
    REPORT "WORD_SIZE: "  & INTEGER'IMAGE(word_size) & LF;
    REPORT "ITERATIONS: " & INTEGER'IMAGE(iterations) & LF;
    REPORT "LOW_AREA: "   & BOOLEAN'IMAGE(low_area) & LF;
    REPORT "IMPL: "       & impl & LF;

    std.env.finish(0);
    WAIT;
  END PROCESS;

END test ; --constants_test
