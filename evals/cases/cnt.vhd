library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity cnt is
  generic (WIDTH : positive := 8);
  port (
    clk   : in std_logic;
    rst_n : in std_logic;
    en    : in std_logic;
    q     : out std_logic_vector(WIDTH-1 downto 0)
  );
end entity;

architecture rtl of cnt is
  signal r : unsigned(WIDTH-1 downto 0) := (others => '0');
begin
  process(clk, rst_n)
  begin
    if rst_n = '0' then
      r <= (others => '0');
    elsif rising_edge(clk) then
      if en = '1' then
        r <= r + 1;
      end if;
    end if;
  end process;

  q <= std_logic_vector(r);
end architecture;
