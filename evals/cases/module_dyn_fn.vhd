library ieee;
use ieee.std_logic_1164.all;

entity module_dyn_fn is
  generic (
    IN_W  : positive := 8;
    OUT_W : positive := 16
  );
  port (
    a : in  std_logic_vector(IN_W-1 downto 0);
    y : out std_logic_vector(OUT_W-1 downto 0)
  );
end entity;

architecture rtl of module_dyn_fn is
  function zext_local(a_in : std_logic_vector) return std_logic_vector is
    variable r : std_logic_vector(OUT_W-1 downto 0);
  begin
    r := (others => '0');
    r(a_in'length-1 downto 0) := a_in;
    return r;
  end function;
begin
  y <= zext_local(a);
end architecture;
