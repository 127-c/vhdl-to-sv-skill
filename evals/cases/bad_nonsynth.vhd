library ieee;
use ieee.std_logic_1164.all;
use std.textio.all;

entity bad_nonsynth is
end entity;

architecture tb of bad_nonsynth is
  file f : text open read_mode is "stim.txt";
begin
  process
  begin
    wait for 10 ns;
  end process;
end architecture;
