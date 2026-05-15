library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

package constrained_shift_pkg is
  constant EXP_N : natural := 5;
  type scale_array_t is array (0 to 3) of integer range -2**EXP_N to 2**EXP_N-1;
end package;

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use work.constrained_shift_pkg.all;

entity constrained_shift is
  port (
    a      : in  signed(7 downto 0);
    shamt  : in  natural range 0 to 7;
    y_left : out signed(7 downto 0);
    y_ar   : out signed(7 downto 0)
  );
end entity;

architecture rtl of constrained_shift is
  signal scales : scale_array_t;
begin
  y_left <= shift_left(a, shamt);
  y_ar   <= shift_right(a, shamt);
end architecture;
