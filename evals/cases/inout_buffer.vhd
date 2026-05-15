library ieee;
use ieee.std_logic_1164.all;

entity inout_buffer is
  port (
    en : in std_logic;
    io : inout std_logic;
    q  : buffer std_logic
  );
end entity;

architecture rtl of inout_buffer is
begin
  io <= q when en = '1' else 'Z';
  q  <= io;
end architecture;
