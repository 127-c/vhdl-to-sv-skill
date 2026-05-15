library ieee;
use ieee.std_logic_1164.all;

package conv_pkg is
  function zext(a : std_logic_vector; n : natural) return std_logic_vector;
end package;

package body conv_pkg is
  function zext(a : std_logic_vector; n : natural) return std_logic_vector is
    variable r : std_logic_vector(n-1 downto 0);
  begin
    r := (others => '0');
    r(a'length-1 downto 0) := a;
    return r;
  end function;
end package body;
