library ieee;
use ieee.std_logic_1164.all;

package p is
  type state_t is (IDLE, RUN, DONE);
  type lane_t is record
    valid : std_logic;
    data  : std_logic_vector(7 downto 0);
  end record;
  type lane_arr_t is array(0 to 3) of lane_t;
end package;

use work.p.all;

entity comb is
  port (
    sel : in state_t;
    a   : in lane_arr_t;
    y   : out std_logic_vector(7 downto 0)
  );
end;

architecture rtl of comb is
begin
  process(sel, a)
  begin
    y <= (others => '0');
    case sel is
      when IDLE   => y <= a(0).data;
      when RUN    => y <= a(1).data;
      when others => y <= x"FF";
    end case;
  end process;
end;
