import pytest
import virtual_pins


# This should probably be a fixture, but I had trouble getting parameters passed to it.
def setup_gen(tmp_path, hdl, ext):

    hdl_path = tmp_path / ("test" + ext)
    tcl_path = tmp_path / "test.tcl"

    gen_config = {
        "parameters": {"input_file": str(hdl_path), "output_file": str(tcl_path)},
        "vlnv": "bogus:core:here",
        "files_root": tmp_path,
    }

    hdl_path.write_text(hdl)

    return (virtual_pins.VirtualPinGenerator(data=gen_config), tcl_path)


# HDL and expected results are included in the parameters as embedded strings.
# This can be tough to read, so perhaps they should be moved to external files
# or just module-level variables

@pytest.mark.parametrize(
    "bad_hdl,bad_hdl_ext",
    [
        (
            """
module syntax_error (
    input  a,
    input  b,
    output c
);
    // Oops I forgot my semicolon
    c <= a & b
endmodule
""",
            ".v",
        ),
        (
            """
library IEEE;
use ieee.std_logic_1164.all;

entity syntax_error is
    port (
        -- Oops my comma should be a semicolon
        a : in std_logic,
        b : in std_logic;
        c : out std_logic
    );
end entity syntax_error;

architecture test of syntax_error is
begin
    c <= a and b;
end architecture test;
""",
            ".vhd",
        ),
    ],
)
def test_syntax_err(tmp_path, bad_hdl, bad_hdl_ext):

    from hdlConvertor._hdlConvertor import ParseException

    uut, output = setup_gen(tmp_path, bad_hdl, bad_hdl_ext)

    with pytest.raises(ParseException):
        uut.run()


@pytest.mark.parametrize(
    "hdl,hdl_ext,expected",
    [
        (
            """
module acc #(
    parameter WIDTH = 13,
    parameter COUNT = 10
)(
    input                clock,
    input                reset,
    input                load,
    input  [WIDTH-1:0]   a,
    input  [WIDTH-1:0]   b,
    output [2*WIDTH-1:0] acc,
    output               valid
);

    always @(posedge clock, posedge reset)
    begin
        if (reset)
        begin
            acc   <= 2*WIDTH-1'b0;
            valid <= 1'b0;
        end else begin
            valid <= 1'b1;
            acc <= acc + a + b;
        end
    end

endmodule
""",
            ".v",
            """set ports {load a b acc valid}
foreach p $ports {
  set_instance_assignment -name VIRTUAL_PIN ON -to $p
}
""",
        ),
        (
            """
library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;

entity ACC is
    generic (
        WIDTH : positive := 13;
        COUNT : positive := 10
    );
    port (
        clock : in  std_logic;
        reset : in  std_logic;
        load  : in  std_logic;
        a     : in  std_logic_vector(WIDTH-1 downto 0);
        b     : in  std_logic_vector(WIDTH-1 downto 0);
        acc   : out std_logic_vector(2*WIDTH-1 downto 0);
        valid : out std_logic
    );
end entity ACC;

architecture test of ACC is

    signal acc_i : unsigned(2*WIDTH-1 downto 0);

begin

    acc <= std_logic_vector(acc_i);

    process (clock, reset)
    begin
        if reset = '1' then
            acc   <= (others => '0');
            valid <= '0';
        else
            if rising_edge(clock) then
	        valid <= '1';
		acc_i <= acc_i + unsigned(a) + unsigned(b);
            end if;
        end if;
    end process;
end architecture test;
""",
            ".vhd",
            """set ports {load a b acc valid}
foreach p $ports {
  set_instance_assignment -name VIRTUAL_PIN ON -to $p
}
""",
        ),
    ],
)
def test_basic_ports(tmp_path, hdl, hdl_ext, expected):

    uut, output = setup_gen(tmp_path, hdl, hdl_ext)

    uut.run()

    assert output.read_text() == expected
