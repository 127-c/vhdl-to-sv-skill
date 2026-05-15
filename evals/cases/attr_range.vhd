library ieee;
use ieee.std_logic_1164.all;

entity attr_range is
  port (
    a     : in  std_logic_vector(0 to 7);
    first : out std_logic;
    last  : out std_logic
  );
end entity;

architecture rtl of attr_range is
begin
  first <= a(a'left);
  last  <= a(a'right);
end architecture;
