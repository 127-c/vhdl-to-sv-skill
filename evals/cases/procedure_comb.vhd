library ieee;
use ieee.std_logic_1164.all;

entity procedure_comb is
  port (
    sel  : in  std_logic_vector(1 downto 0);
    y_en : out std_logic;
    y    : out std_logic_vector(3 downto 0)
  );
end entity;

architecture rtl of procedure_comb is
  procedure decode(
    signal sel_i : in  std_logic_vector(1 downto 0);
    signal en_o  : out std_logic;
    signal y_o   : out std_logic_vector(3 downto 0)
  ) is
  begin
    en_o <= '0';
    y_o  <= (others => '0');
    case sel_i is
      when "01" =>
        en_o <= '1';
        y_o  <= "0001";
      when "10" =>
        en_o <= '1';
        y_o  <= "0010";
      when others =>
        null;
    end case;
  end procedure;
begin
  process(sel)
  begin
    decode(sel, y_en, y);
  end process;
end architecture;
