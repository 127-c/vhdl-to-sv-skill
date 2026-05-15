library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity arith is
  port (
    a   : in std_logic_vector(7 downto 0);
    b   : in signed(7 downto 0);
    yu  : out unsigned(15 downto 0);
    ys  : out signed(15 downto 0);
    cat : out std_logic_vector(10 downto 0)
  );
end entity;

architecture rtl of arith is
begin
  yu  <= resize(unsigned(a), 16);
  ys  <= resize(signed(b), 16);
  cat <= "001" & a;
end architecture;
