---
name: vhdl-to-sv
description: 灏嗗彲缁煎悎鐨?VHDL RTL 杞崲涓虹瓑浠风殑 SystemVerilog RTL锛屽苟楠岃瘉鐢熸垚鐨勮浆鎹㈢粨鏋溿€傚綋鐢ㄦ埛瑕佹眰鎶?VHDL 缈昏瘧銆佽縼绉汇€侀噸鍐欍€佸鏌ャ€侀噸鏋勩€侀獙璇佹垨妫€鏌ヤ负 SV/SystemVerilog 鏃朵娇鐢ㄦ skill锛屽挨鍏堕€傜敤浜?entity/architecture 妯″潡銆乸ackage銆乬eneric銆佺鍙ｃ€乸rocess銆乻ignal銆佹暟缁勩€乺ecord銆佸彈绾︽潫 integer range/subtype銆佹湁绗﹀彿/鏃犵鍙风畻鏈€乺esize/ext/sxt銆乻hift_left/shift_right 鍜屽叾浠栫Щ浣嶃€佸姩鎬佷綅瀹?function銆乵odule-local 鎴?package-specialized function 绛栫暐銆佹湭绾︽潫鏁扮粍銆乂HDL 灞炴€с€乬enerate 璇彞銆乂HDL 绱㈠紩璇箟銆佸彲缁煎悎鎬у鏌ユ垨杞崲璐ㄩ噺鎶ュ憡銆傛 skill 鍙潰鍚戝彲缁煎悎 RTL锛涢亣鍒?testbench-only銆佽涓虹骇銆乫ile I/O銆乤ccess/protected/physical 绫诲瀷銆佸惈绯婄殑涓夋€?buffer 琛屼负浠ュ強涓嶅彲缁煎悎缁撴瀯鏃讹紝搴旀爣璁伴闄╋紝鑰屼笉鏄洸鐩浆鎹€?---

# VHDL 鍒?SystemVerilog RTL 杞崲

## 鏍稿績鐩爣 / Purpose

灏嗗彲缁煎悎鐨?VHDL RTL 杞崲涓虹瓑浠风殑 SystemVerilog RTL锛屽悓鏃朵繚鐣欑‖浠惰涓恒€佷綅瀹姐€佺鍙峰睘鎬с€佺储寮曟柟鍚戙€佸浣嶈涓轰互鍙婄粍鍚?鏃跺簭璇箟銆?
鎶婃 skill 褰撲綔杩佺Щ鎸囧锛岃€屼笉鏄畝鍗曠殑鏂囨湰鏇挎崲鍣ㄣ€傚厛淇濈暀婧愪唬鐮佽涔夛紝鍐嶅簲鐢ㄩ」鐩殑 SystemVerilog 浠ｇ爜椋庢牸銆?
杞崲鍚庤楠岃瘉鐢熸垚鐨?SV 鐨勮娉曠粨鏋勩€佸彲缁煎悎椋庨櫓銆佽鍒欎竴鑷存€у拰鍙鏌ユ€с€傞櫎闈炲凡缁忓湪姝?skill 宸ヤ綔娴佷箣澶栫湡瀹炶繍琛岃繃浠跨湡鎴栧崗鍚屼豢鐪燂紝鍚﹀垯涓嶈澹扮О鍔熻兘绛変环銆?
## 閫傜敤鑼冨洿 / Scope

榛樿鍙浆鎹㈠彲缁煎悎 RTL銆?
澶勭悊锛?- `entity` / `architecture` 鍒?`module`
- `generic` / `constant` 鍒?`parameter` / `localparam`
- `port`銆乣signal`銆乣variable`銆乣subtype`銆乣type`銆乣enum`銆乣record` 鍜屾暟缁?- 骞跺彂璧嬪€笺€佺粍鍚?process銆佹椂閽?process銆乫unction銆乸rocedure銆乸ackage 鍜?generate block
- VHDL bit/vector 瀛楅潰閲忋€佹嫾鎺ャ€佺储寮曘€佸垏鐗囥€佸睘鎬с€佹湁绗﹀彿/鏃犵鍙风畻鏈€乣resize`銆乣ext` 鍜?`sxt`

鏍囪椋庨櫓锛岃€屼笉鏄洸鐩浆鎹細
- `access`銆乣file`銆乣protected`銆乣physical`銆佸ぇ澶氭暟 RTL 涓殑 `real`/`time` 鐢ㄦ硶銆佸姩鎬佸垎閰嶃€乼ext I/O銆佸熀浜?wait 鐨勮涓轰唬鐮佹垨 testbench-only 缁撴瀯
- 鍚硦鐨?`buffer`銆乣linkage`銆乣inout`銆佸椹卞姩銆乺esolved logic 琛屼负銆佸０鏄庡垵濮嬪寲鎴栨椂閽?澶嶄綅璇箟
- 娌℃湁瀵硅薄绾?range 鎴栧弬鏁板寲杈圭晫鐨?unconstrained array

## 浣跨敤妯″紡 / Usage Modes

鏍规嵁鐢ㄦ埛璇锋眰鍜岃緭鍏ラ€夋嫨鍚堥€傛ā寮忥細

- **VHDL 鍒?SV 杞崲**锛氳鍙?`.vhd` / `.vhdl` 婧愭枃浠舵垨鍐呰仈 VHDL锛屽苟鐢熸垚绛変环鐨?`.sv` 浠ｇ爜鎴栨枃浠躲€?- **SV 杩佺Щ瀹℃煡**锛氭牴鎹師濮?VHDL銆佹 skill 鐨勮浆鎹㈣鍒欏拰椤圭洰椋庢牸锛屽鏌ュ凡缁忚浆鎹㈣繃鐨?SystemVerilog銆?- **杞崲楠岃瘉**锛氭牴鎹師濮?VHDL銆侀潤鎬佽浆鎹㈣鍒欍€佸彲缁煎悎椋庨櫓瑙勫垯銆佹敞閲婄瓥鐣ュ拰蹇呴渶杈撳嚭鍖哄潡锛屾鏌ョ敓鎴愮殑 SV銆?- **瑙勫垯瑙ｉ噴**锛氳В閲婃煇涓?VHDL 缁撴瀯搴斿浣曟槧灏勫埌 SystemVerilog锛屽挨鍏舵槸浣嶅銆佺鍙枫€佹暟缁勩€乺ecord銆乫unction 鎴?process 琛屼负銆?- **鎵归噺杩佺Щ瑙勫垝**锛氭鏌ュ涓?VHDL 鏂囦欢锛岃瘑鍒?package 鍜?design-unit 渚濊禆鍏崇郴锛屾彁鍑虹紪璇戦『搴忥紝鐒跺悗鎸変緷璧栭『搴忚浆鎹€?
## 鎵ц娴佺▼ / Workflow

鎸変互涓?phase 椤哄簭鎵ц銆傚伐浣滆繃绋嬩腑鎸佺画璁板綍鍋囪銆佹湭鏀寔缁撴瀯鍜屼汉宸ュ鏌ラ」銆?
### Phase 0: 杈撳叆璇嗗埆 / Input Recognition

1. 鍏堝畾浣嶆簮鏂囦欢銆傜敤鎴风粰鍑鸿矾寰勬椂锛屼粠璇ユ枃浠舵垨鐩綍璇诲彇 `.vhd` 鍜?`.vhdl` 鏂囦欢銆傚伐浣滃尯宸叉湁鏂囦欢鍙鏃讹紝涓嶈姹傜敤鎴风矘璐翠唬鐮併€?2. 灏嗘瘡涓緭鍏ュ垎绫讳负 VHDL 婧愩€佸凡杞崲 SV 婧愩€乸ackage銆乸ackage body銆乪ntity銆乤rchitecture銆佺嫭绔?function/procedure 鎴栦粎瀹℃煡 artifact銆?3. 鍒ゆ柇鐢ㄦ埛闇€瑕佹枃浠惰緭鍑恒€佸唴鑱斾唬鐮併€佸鏌ヨ繕鏄В閲娿€?4. 杞崲鍓嶅厛鍐冲畾杈撳嚭璺緞銆傞粯璁ゅ皢姣忎釜宸茶浆鎹?design unit 鍐欐垚鍚岀洰褰曞悓 basename 鐨?`.sv` 鏂囦欢锛涘鏋滅敤鎴锋寚瀹氳緭鍑虹洰褰曪紝鍒欏啓鍏ヨ鐩綍銆傚浜?package锛屽鏋滄瘮婧愭枃浠跺悕鏇存竻妤氾紝浣跨敤 `<package_name>_pkg.sv`銆?
### Phase 1: 涓婁笅鏂囧垎鏋?/ Context Analysis

1. 寤虹珛鏂囦欢/design-unit 涓婁笅鏂囷細璇嗗埆 package銆乸ackage body銆乪ntity銆乤rchitecture銆乧omponent declaration銆佷緷璧栧叧绯汇€佹椂閽熴€佸浣嶃€乬eneric銆佺鍙ｃ€佸唴閮ㄥ０鏄庛€乸rocess銆佸疄渚嬪拰 generate block銆?2. 鍦ㄨ浆鎹㈣鍙ュ墠鍏堟彁鍙栧０鏄庯紝浣胯〃杈惧紡鑳戒娇鐢ㄦ纭殑 SV 绫诲瀷銆?3. 灏嗘瘡涓?process 鎴栧苟鍙戝尯鍩熷垎绫讳负缁撴瀯鍨嬨€佺粍鍚堥€昏緫銆佹椂搴忛€昏緫銆乸ackage/type declaration銆乫unction/procedure 鎴栦笉鏀寔/涓嶅彲缁煎悎缁撴瀯銆?4. 瀵规瘡涓?VHDL function锛屾鏌ュ叾鍙傛暟銆佽繑鍥炲€笺€佸眬閮ㄥ彉閲忋€佽祴鍊肩洰鏍囨垨灞炴€ф槸鍚︿緷璧栬皟鐢ㄧ偣浣嶅銆佹湭绾︽潫 vector銆乣a'length`銆乣a'range` 鎴栧璞＄壒瀹氳竟鐣屻€?5. 鍦ㄨ浆鎹?composite type 鍓嶈瘑鍒瘡涓彈绾︽潫鏍囬噺绫诲瀷銆傚挨鍏惰璁板綍鐢ㄤ簬鏁扮粍銆乺ecord銆佺鍙ｃ€乻ignal銆乿ariable 鎴栨祦姘寸姸鎬佷腑鐨?`integer range`銆乣natural range`銆乣positive range` 鍜?subtype 鐨勫師濮?VHDL 鍘熷瀷銆?
### Phase 2: 瑙勫垯鍖归厤 / 绛栫暐閫夋嫨

1. 杞崲澶嶆潅绫诲瀷銆佹暟缁勩€乺ecord銆佸睘鎬с€佺畻鏈綅瀹藉彉鍖栥€乸rocess銆乫unction銆乸ackage 鎴?generate 璇彞鍓嶏紝璇诲彇 `references/conversion-rules.md`銆?2. 鍐欏叆鐢熸垚鐨?SystemVerilog 鍓嶏紝璇诲彇 `references/code-style.md`锛岄櫎闈炵洰鏍囦粨搴撳凡鏈夋洿鏄庣‘鐨勬湰鍦?SV 椋庢牸銆傝嫢鏈湴椋庢牸涓庢 reference 鍐茬獊锛岄伒寰湰鍦伴鏍硷紝骞惰鏄庢湁鎰忎箟鐨勫亸绂汇€?3. 澶勭悊 dynamic-width function銆乣resize` / `ext` / `sxt`銆乽nconstrained array锛屾垨 `'length`銆乣'range`銆乣'left`銆乣'right` 绛?VHDL 灞炴€у墠锛岃鍙?`references/special-conversion-strategies.md`銆?4. 鍐冲畾杩佺Щ璇存槑搴斿啓鍏?RTL 娉ㄩ噴銆丆onversion Notes 杩樻槸 Manual Review Items 鍓嶏紝璇诲彇 `references/annotation-policy.md`銆?5. 鎸夎涓洪€夋嫨杞崲绛栫暐锛岃€屼笉鏄寜璇硶閫夋嫨銆傚厛淇濈暀婧愯涔夛紝鍐嶅仛椋庢牸鏀硅繘銆?6. 闇€瑕佸姩鎬佷綅瀹?function 瑙勫垯鏃讹紝浼樺厛浣跨敤鍙傛暟鍖?`virtual class` 鍔?`static function automatic` 绛栫暐锛涘彧鏈夊湪鏂囨。瑙勫畾鏉′欢婊¤冻鏃讹紝鎵嶄娇鐢?module-parameterized 鎴?fixed-width package-specialization 绛栫暐銆?7. 褰撹涔変緷璧栫洰鏍囧伐鍏锋敮鎸併€侀」鐩唬鐮侀鏍笺€佸浣嶇害瀹氥€乺esolved logic 琛屼负鎴栧惈绯?VHDL 缁撴瀯鏃讹紝杈撳嚭浜哄伐瀹℃煡椤癸紝涓嶈鐚滄祴銆?
### Phase 3: 缁撴灉鐢熸垚 / Result Generation

1. 鐢熸垚 SystemVerilog 鏃朵娇鐢ㄦ樉寮?typed ports銆佹樉寮?parameter 绫诲瀷銆佸彈鎺т綅瀹姐€佺ǔ瀹氬懡鍚嶃€乣logic`銆乣always_ff`銆乣always_comb`銆佸叿鍚?parameter override 鍜屽叿鍚嶇鍙ｈ繛鎺ャ€?2. 灏嗘椂閽熻Е鍙戠殑 `rising_edge` / `falling_edge` process 杞负 `always_ff`锛屽瘎瀛樺櫒浣跨敤闈為樆濉炶祴鍊笺€?3. 灏嗙粍鍚?process 杞负 `always_comb`锛屼娇鐢ㄩ樆濉炶祴鍊硷紝骞跺湪闇€瑕佹椂鎻愪緵鏄惧紡榛樿鍊间互閬垮厤 latch 鎺ㄦ柇銆?4. 绠€鍗曞苟鍙戣祴鍊煎湪杩炵画杩炵嚎璇箟鏇存竻妤氭椂杞负 `assign`銆?5. 濡傛灉澶氫釜鐢熸垚鏂囦欢鍏变韩 package 渚濊禆锛屼繚鐣欐垨璇存槑缂栬瘧椤哄簭銆?6. 瀵?`references/annotation-policy.md` 瀹氫箟鐨勯珮椋庨櫓杞崲锛屽湪鐢熸垚 RTL 闄勮繎娣诲姞蹇呴渶鐨?`// VHDL2SV:` 鐭敞閲娿€備繚鐣?`VHDL2SV:` 鍓嶇紑锛屽啋鍙峰悗鐨勮鏄庝娇鐢ㄤ腑鏂囥€傛敞閲婁繚鎸佸眬閮ㄣ€佺畝鐭紱鏇村娉涚殑娉ㄦ剰浜嬮」鏀惧埌 Conversion Notes 鎴?Manual Review Items銆?
### Phase 4: 缁撴灉澶嶆煡 / Final Review

1. 杩斿洖鏈€缁堜唬鐮佹垨杩佺Щ瀹℃煡鍓嶏紝璇诲彇 `references/review-checklist.md` 鍜?`references/verification-workflow.md`銆?2. 澶嶆煡浣嶅銆佺鍙枫€佺储寮曟柟鍚戙€佸浣嶈涓恒€佽祴鍊兼椂搴忋€佹暟缁勭淮搴︺€乫unction 浣嶅鍜屼笉鏀寔缁撴瀯銆?3. 楠岃瘉鐢熸垚浠ｇ爜閬靛惊 `references/code-style.md` 鎴栫洰鏍囦粨搴撳凡鏈夐鏍笺€?4. 鏂囦欢鍙敤鏃讹紝杩愯 `references/verification-workflow.md` 涓殑榛樿杞崲楠岃瘉绛夌骇锛歀0 鎶ュ憡/鏍煎紡妫€鏌ャ€丩1 闈欐€佽浆鎹㈡鏌ュ拰 L2 Questa `vlog -sv` 璇硶缂栬瘧妫€鏌ャ€傛宸ヤ綔娴佷腑涓嶈杩愯 Efinity 缁煎悎鎴?`vsim` 鍔熻兘浠跨湡銆?5. 褰撴簮 VHDL 鍜岀敓鎴?SV 鏂囦欢閮藉瓨鍦ㄦ椂锛屼娇鐢?`scripts/verify_conversion.py`銆傚鏋滆剼鏈棤娉曡繍琛岋紝鍒欐墜鍔ㄦ墽琛屽悓绛夐潤鎬佹鏌ュ苟璇存槑鍘熷洜銆?6. 褰撶敓鎴?SV 鏂囦欢瀛樺湪涓?`vlib`/`vlog` 鍙敤鏃讹紝杩愯 Questa 璇硶缂栬瘧妫€鏌ャ€傚敖閲忎娇鐢ㄤ緷璧栨劅鐭ョ殑缂栬瘧椤哄簭锛屽挨鍏舵槸 package 搴斿厛浜庝緷璧栧畠鐨?module 缂栬瘧銆傚鏋?Questa 涓嶅彲鐢ㄦ垨鏃犳硶杩愯缂栬瘧锛屽垯鍦?L2 涓爣璁?`SKIP` 骞惰鏄庡師鍥犮€?7. 鎸夎姹傜殑杈撳嚭鏍煎紡杩斿洖鐢熸垚鏂囦欢/浠ｇ爜銆佽浆鎹㈣鏄庛€佷汉宸ュ鏌ラ」銆佸彲缁煎悎鎬ф鏌ユ竻鍗曞拰楠岃瘉缁撴灉銆?
## 鏍稿績瑙勫垯 / Core Rules

浼樺厛鐢熸垚鑳戒繚鐣欒涓虹殑鏈€灏?SystemVerilog銆備笉瑕佷负浜嗚繃搴︾幇浠ｅ寲鑰屾敼鍙樼储寮曟垨纭欢缁撴瀯銆?
### 绫诲瀷 / Types

- 榛樿灏?`std_logic` 鍜?`std_logic_vector` 鏄犲皠涓哄洓鎬?`logic`銆?- 鍙湁褰撴簮浠ｇ爜鏄庣‘鏄簩鎬侀€昏緫锛屾垨鐢ㄦ埛瑕佹眰浜屾€侀鏍兼椂锛屾墠灏?VHDL `bit` / `bit_vector` 鏄犲皠涓?SV `bit`銆?- 浣跨敤 `logic signed [...]` 淇濈暀 `signed`锛涘皢 `unsigned` 鏄犲皠涓烘棤绗﹀彿 `logic [...]`锛岄櫎闈為渶瑕佹樉寮?signed cast銆?- 瀵?`integer range`銆乣natural`銆乣positive` 鍜?`subtype`锛屽彧鏈夊綋瀵硅薄鏄湡瀹炵‖浠?signal/counter/index 鏃舵墠鎺ㄥ鍥哄畾浣嶅銆傚惁鍒欎娇鐢?`int` / `int unsigned`锛屽苟璇存槑鍘熷 range 绾︽潫銆?- 瀵圭敤浜庡瓨鍌?RTL 鏁版嵁銆佹暟缁勫厓绱犮€乺ecord/struct 瀛楁銆佺鍙ｃ€佽鏁板櫒鎴栨祦姘寸姸鎬佺殑鍙楃害鏉?integer锛屼紭鍏堜娇鐢ㄦ樉寮?`logic` / `logic signed` 鍜屾帹瀵煎嚭鐨勫浐瀹氫綅瀹姐€傛坊鍔犲眬閮ㄤ腑鏂?`// VHDL2SV:` 娉ㄩ噴锛屽紩鐢ㄦ垨姒傛嫭鍘熷 VHDL range/鍘熷瀷銆?- 鍙湁褰?32-bit signed 璇箟鏄湁鎰忕殑銆佷笖涓嶄細鍙樻垚纭欢瀛樺偍鏃讹紝鎵嶆妸 SV `int` 鐢ㄤ簬缂栬瘧鏈熷弬鏁般€佸惊鐜彉閲忋€佷复鏃惰绠楁垨 API 椋庢牸鏍囬噺銆傝嫢鏃犳硶纭畾瀵硅薄鏄瓨鍌ㄨ繕鏄粎鐢ㄤ簬璁＄畻锛屽瀛樺偍瀵硅薄浣跨敤鏄惧紡 `logic`锛屽苟鍦?Manual Review Items 涓垪鍑轰笉纭畾鐐广€?
### 浣嶅涓庣储寮?/ Widths and Indexes

- 榛樿淇濈暀 `downto` / `to` 鏂瑰悜銆傚彧鏈夌敤鎴锋垨椤圭洰鏄庣‘瑕佹眰鏃舵墠褰掍竴鍖栦负 `[W-1:0]`锛屽苟涓斿繀椤婚噸鍐欐墍鏈夊彈褰卞搷鐨勭储寮曘€佸垏鐗囥€乺ange 鍜屽睘鎬с€?- 璋ㄦ厧澶勭悊 VHDL 灞炴€с€俙a'length` 鍙兘琛ㄧず vector bit width銆乤rray depth 鎴?element width锛屽彇鍐充簬 `a`锛涚浉搴旈€夋嫨 `$bits`銆乣$size` 鎴栨樉寮?parameter銆?- 缁濅笉瑕佹妸 `$signed`銆乣$unsigned` 鎴?cast 褰撴垚 `resize` 鐨勫畬鏁存浛浠ｏ紱鍙兘闇€瑕佹樉寮?extension/truncation銆?- 瀵逛綅瀹芥晱鎰熷父閲忎娇鐢ㄦ樉寮?sized literal銆?
### 绗﹀彿涓庣畻鏈?/ Signedness and Arithmetic

- 鍦ㄥ０鏄庡拰琛ㄨ揪寮忎笂涓嬫枃涓繚鐣?signedness銆?- 鏄庣‘鎺у埗 zero extension銆乻ign extension銆乼runcation銆乻hift銆乧omparison 鍜?cast 鐨勪綅瀹姐€?- 灏?`resize(unsigned(...), N)` 杞负鍙楁帶 zero-extension 鎴?truncation銆?- 灏?`resize(signed(...), N)` 杞负鍙楁帶 sign-extension 鎴?truncation銆?- 鎸夋搷浣滄暟璇箟杞崲 VHDL `shift_left` / `shift_right` / `sll` / `srl` / `sla` / `sra`锛屼笉瑕佸彧鎸夊嚱鏁板悕鏇挎崲銆係V 鏈夌Щ浣嶈繍绠楃 `<<`銆乣>>`銆乣<<<`銆乣>>>`锛屾病鏈夊唴寤虹殑 RTL `shift_left` function銆傞€昏緫宸︾Щ鐢?`<<`锛岄€昏緫鍙崇Щ鐢?`>>`锛涘綋 VHDL signed 璇箟瑕佹眰绠楁湳鍙崇Щ鏃讹紝浣跨敤甯︽樉寮?signed 鎿嶄綔鏁扮殑 `>>>`銆?- 褰撴棤娉曚粠澹版槑鍜屼笂涓嬫枃璇佹槑 VHDL 绉讳綅鎿嶄綔鏁扮鍙峰睘鎬с€佸～鍏呰涓恒€佺粨鏋滀綅瀹芥垨绉讳綅閲忎綅瀹芥椂锛屼繚鎸佺敓鎴?RTL 淇濆畧锛屽苟娣诲姞涓枃 `// VHDL2SV:` 娉ㄩ噴鍜?Manual Review Item銆?
### 鏁扮粍銆乺ecord 涓?package / Arrays, Records, and Packages

- 鍖哄垎 packed vector width 鍜?unpacked array depth銆?- 鍙湁褰撴墍鏈夊瓧娈甸兘鑳藉悎娉曟墦鍖呬负鍥哄畾浣嶅鍏冪礌锛屽苟涓旇 record 鐨勮涓虹被浼?packed bus 鏃讹紝鎵嶅皢 VHDL record 杞负 `struct packed`銆?- 鍙湁鎵惧埌瀵硅薄绾ц竟鐣屾垨鍙傛暟鍖栬竟鐣屽悗锛屾墠杞崲 unconstrained array銆?- 閫氬父灏?VHDL package declaration 鍜?package body 鍚堝苟鍒颁竴涓?SV package銆?
### 璇彞涓庤繘绋?/ Statements and Processes

- 灏?VHDL `&` 鎷兼帴杞负 SV `{...}`锛屼笉瑕佽浆涓烘寜浣?`&`銆?- 鍙湁鍦?boolean 鏉′欢涓紝鎵嶅皢 VHDL boolean `and/or/not` 杞负 `&&/||/!`锛泇ector logic 浣跨敤鎸変綅 `&/|/~`銆?- 鏍规嵁鐩爣绫诲瀷杞崲 `others =>`锛歱acked vector 閫氬父浣跨敤 `'0` / `'1`锛沘rray/struct 浣跨敤 `'{default:...}`銆?- 灏?`case` 璇彞涓殑 `when others` 杞负 `default:`銆?- 鏍规嵁 process 璇箟杞崲璧嬪€硷紝鑰屼笉鏄師濮?token 鏇挎崲銆?- 瀵规瘡涓珮椋庨櫓鐢熸垚缁撴瀯娣诲姞鐭腑鏂?`// VHDL2SV:` 娉ㄩ噴锛氬姩鎬佷綅瀹?function 绛栫暐銆佹湁鎰忔埅鏂€佹樉寮忕鍙?闆舵墿灞曘€佹柟鍚?绱㈠紩閲嶆槧灏勩€佹湭绾︽潫鏁扮粍杈圭晫閫夋嫨銆佸０鏄庡垵濮嬪寲鍋囪锛屾垨缁忚繃瀹℃煡鐨?`buffer`/`inout`/涓夋€佸鐞嗐€?- 瀵规瘡涓粠鍙楃害鏉?VHDL integer/subtype 杞垚鍥哄畾浣嶅 `logic` 鐨勪綅缃坊鍔犵煭涓枃 `// VHDL2SV:` 娉ㄩ噴锛屽寘鍚師濮?VHDL 鍘熷瀷鎴?range 姒傛嫭銆?- 瀵规瘡涓潪骞冲嚒 VHDL 绉讳綅 function/operator 杞崲娣诲姞鐭腑鏂?`// VHDL2SV:` 娉ㄩ噴锛屽挨鍏跺綋 signedness銆佸～鍏呰涓烘垨缁撴灉浣嶅浼氬奖鍝嶈涓烘椂銆?
procedure 瑙勫垯锛?- 榛樿涓嶈涓哄彲缁煎悎 RTL 鐢熸垚 SV `task`銆?- 褰?VHDL `procedure` 鏄函闆舵椂闂寸粍鍚堥€昏緫鏃讹紝杞负 `function automatic`銆傚崟涓€缁撴灉浣跨敤鏄惧紡杩斿洖绫诲瀷锛涘涓粨鏋滃湪姣?struct return 鏇存竻妤氭椂锛屼娇鐢?`function automatic void` 鍔?`output` / `inout` 鍙傛暟銆?- 褰?procedure 寰堢畝鍗曘€佸彧鍦ㄦ湰鍦颁竴涓?process 浣跨敤锛屾垨灏佽鎴?function 浼氭ā绯?signal 璧嬪€兼椂搴忔椂锛岀洿鎺ュ唴鑱斻€?- 鍦ㄦ椂閽?process 涓皟鐢ㄧ殑 procedure锛屽簲鍏堢敤闃诲璧嬪€兼垨 function result 璁＄畻 next value锛屽啀鍦ㄥ灞?`always_ff` 涓敤闈為樆濉炶祴鍊兼洿鏂板瘎瀛樺櫒銆?- 鍚?wait銆乨elay銆乫ile I/O銆乻hared variable銆侀殣钘忕姸鎬併€乻ignal 鏃跺簭渚濊禆鎴栧惈绯?`signal` 鍙傛暟鐨?procedure锛屼笉杞垚 `task`锛岃€屾槸鏍囪浜哄伐瀹℃煡銆?
楠岃瘉瑙勫垯锛?- 鍐欏叆鐢熸垚 SV 鍚庢墽琛岄獙璇併€傝嚦灏戞鏌ュ繀闇€杈撳嚭鍖哄潡銆佺鐢ㄧ粨鏋勩€乸rocess 鏄犲皠銆佷綅瀹?绗﹀彿璇存槑銆侀€傜敤鐨?eval 鏈熸湜锛屼互鍙婃枃浠跺拰宸ュ叿鍙敤鏃剁殑 Questa `vlog -sv` 璇硶缂栬瘧銆?- 榛樿杩愯 Questa `vlog -sv` 缂栬瘧浣滀负鐢熸垚 SV 鐨勫伐鍏疯娉曟鏌ャ€傝姝ラ涓嶆槸鍔熻兘浠跨湡锛屼笉鑳借鎶ュ憡涓哄姛鑳界瓑浠枫€?- 涓嶈嚜鍔ㄨ繍琛?Efinity 缁煎悎鎴?`vsim` 浠跨湡銆俀uesta 鍔熻兘浠跨湡鏄悗缁姛鑳介獙璇佸眰锛岄櫎闈炵敤鎴锋槑纭姹傚苟鎻愪緵 testbench/浠跨湡璁剧疆锛屽惁鍒欎笉灞炰簬姝よ浆鎹?only 宸ヤ綔娴併€?- 褰撴簮鏂囦欢鍜岀敓鎴愭枃浠跺彲鐢ㄦ椂锛屼娇鐢?`scripts/verify_conversion.py` 鎵ц鍙噸澶嶉潤鎬佽浆鎹㈡鏌ャ€?
## 鐗规畩鍦烘櫙 / Special Cases

- 瀵?dynamic 鎴?unconstrained vector-width VHDL function锛屼娇鐢?`references/conversion-rules.md` 涓殑椤圭洰绛栫暐锛氬弬鏁板寲 `virtual class` 鍔?`static function automatic`銆傚彧鏈夊綋鐢ㄦ埛鏄庣‘瑕佹眰銆侀」鐩?宸ュ叿椋庢牸绂佹鍙傛暟鍖?class锛屾垨璇?function 鍙瘉鏄庝笉鍙鐢ㄦ椂锛屾墠浣跨敤 module-parameterized 瀹炵幇鎴?package-level fixed-width specialization锛涘苟鍦ㄦ枃妗ｄ腑璇存槑渚嬪銆?- 瀵?module-local dynamic-width function锛屽彧鏈夊綋 function 涓庤 module 鐨?generic 鎴栬皟鐢ㄧ偣绱у瘑缁戝畾鏃讹紝鎵嶄娇鐢?module parameter 鎺у埗鎵€鏈変綅瀹斤紝骞跺皢瀹炵幇淇濈暀鍦?module 鍐呴儴銆?- 瀵瑰皯閲忕ǔ瀹氬浐瀹氫綅瀹介泦鍚堢殑鍏叡 dynamic-width function锛屽垱寤烘樉寮忓懡鍚嶇殑 fixed-width package specialization锛屽苟鍒楀嚭宸茶鐩栧拰鏈鐩栫殑 width pair銆?- 瀵瑰彲缁煎悎 RTL 涓殑 VHDL procedure锛屼紭鍏堜娇鐢?`function automatic`銆乣function automatic void` 鎴栧唴鑱斻€傞櫎闈炵敤鎴锋槑纭姹?task 椋庢牸骞剁‘璁ょ洰鏍囩患鍚堟祦绋嬫帴鍙楋紝鍚﹀垯涓嶈杈撳嚭 `task`銆?- 瀵?`buffer`銆乣linkage`銆乣inout`銆乼ri-state 琛屼负銆佸椹卞姩鎴?resolved type锛屽仠姝㈢寽娴嬪苟杈撳嚭浜哄伐瀹℃煡椤癸紝璇存槑鍙兘鐨勮縼绉婚€夐」銆?- 瀵?declaration initialization锛屼笉瑕佸亣璁惧畠绛変环浜庣‖浠跺浣嶏紝闄ら潪椤圭洰绾﹀畾鎴栨簮涓婁笅鏂囪兘璇佹槑銆?- 瀵?VHDL `open` association锛屽湪淇濈暀绌鸿繛鎺ユ垨 tie-off 鍓嶆鏌ョ鍙ｆ柟鍚戝拰 module contract銆?- 瀵逛緷璧?architecture/configuration 鐨勫疄渚嬪寲锛屼繚鐣欐垨璇存槑鎵€閫夋嫨鐨?architecture/configuration 渚濊禆銆?
## 缁濅笉鍋氱殑浜?/ Do Not

- 涓嶈闈欓粯杞崲涓嶆敮鎸併€佸惈绯娿€乼estbench-only 鎴栦笉鍙患鍚堢殑 VHDL銆?- 褰撳伐浣滃尯瀛樺湪鍙鏂囦欢鏃讹紝涓嶈瑕佹眰鐢ㄦ埛绮樿创浠ｇ爜銆?- 涓嶈褰掍竴鍖栫储寮曟柟鍚戯紝闄ら潪姣忎釜鍙楀奖鍝嶇殑澹版槑銆佺储寮曘€佸垏鐗囥€乺ange銆佸睘鎬у拰 loop 閮借閲嶆柊鏄犲皠銆?- 涓嶈鍙敤 `$signed`銆乣$unsigned` 鎴?unsized cast 鏇夸唬 `resize`銆乣ext` 鎴?`sxt`銆?- 涓嶈鎶婄敤浜庣‖浠跺瓨鍌ㄧ殑鍙楃害鏉?VHDL `integer range` 闈欓粯鏄犲皠鎴?SV `int`锛沗int` 鏄?32-bit signed锛屼笉鑳戒繚鐣?VHDL range 绾︽潫銆?- 涓嶈鍦ㄧ敓鎴愮殑 SV 涓繚鐣?VHDL `shift_left` / `shift_right` function call锛岄櫎闈炴湁鎰忕敓鎴愪簡鍏锋湁瀹屽叏鐩稿悓濂戠害鐨勯」鐩?SV helper function锛屽苟涓斿凡缁忔枃妗ｅ寲銆?- 涓嶈涓?RTL 杩佺Щ寮曞叆 SV dynamic array銆乹ueue銆佹湁鐘舵€?class銆乼iming control銆乫ile I/O 鎴栧叾浠栦笉鍙患鍚堢粨鏋勩€?- 榛樿涓嶈涓?RTL procedure 杞崲鐢熸垚 SV `task`銆?- 褰撳彲浠ヤ娇鐢ㄥ叿鍚?parameter 鎴栫鍙ｈ繛鎺ユ椂锛屼笉瑕佷娇鐢?positional association銆?- 涓嶈鐢ㄦ樉鑰屾槗瑙佺殑娉ㄩ噴姹℃煋鐢熸垚 RTL銆傚彧瀵归珮椋庨櫓杩佺Щ鍐崇瓥浣跨敤涓枃 `// VHDL2SV:` 娉ㄩ噴锛涙洿瀹芥硾鐨勫亣璁惧拰椋庨櫓鍐欏埌鍝嶅簲璇存槑涓€?- 涓嶈澹扮О Efinity 缁煎悎閫氳繃銆丵uesta 浠跨湡閫氳繃鎴栧姛鑳界瓑浠凤紝闄ら潪杩欎簺澶栭儴妫€鏌ョ‘瀹炵敱鐢ㄦ埛鎴栧崟鐙姹傜殑娴佺▼杩愯杩囥€俀uesta `vlog -sv` 璇硶缂栬瘧閫氳繃鍙兘鎶ュ憡涓虹紪璇?璇硶妫€鏌ラ€氳繃锛屼笉鑳芥姤鍛婁负浠跨湡閫氳繃銆?
## 杈撳嚭鏍煎紡 / Output Format

褰撶敤鎴疯姹傛枃浠惰浆鎹㈡椂锛屽皢杞崲鍚庣殑 `.sv` 鏂囦欢鍐欏叆纾佺洏锛屽苟杩斿洖锛?
````markdown
## Generated Files
- `<path/to/output.sv>`

## Conversion Notes
- <閲嶈璇箟鍐崇瓥銆佷綅瀹?绗﹀彿/绱㈠紩鍋囪銆侀鏍奸€夋嫨鍜岄潪骞冲嚒鏄犲皠>

## Manual Review Items
- <闇€瑕佷汉宸ョ‘璁ょ殑椤圭洰锛涙病鏈夊垯鍐?"None">

## Synthesizability Checklist
- <鍏充簬 process 绫诲瀷銆乴atch銆佸椹卞姩銆佷笉鏀寔缁撴瀯銆佷綅瀹?绗﹀彿鐨勭畝鐭€氳繃/澶辫触璇存槑>

## Validation Results
- <L0 鎶ュ憡/鏍煎紡妫€鏌ョ粨鏋?
- <L1 闈欐€佽浆鎹㈡鏌ョ粨鏋?
- <L2 Questa `vlog -sv` 璇硶缂栬瘧妫€鏌ョ粨鏋滐紱濡傛灉 Questa 涓嶅彲鐢ㄦ垨娌℃湁鐢熸垚 SV 鏂囦欢锛屽垯鍐?"SKIP" 骞惰鏄庡師鍥?
- <閫傜敤鏃剁殑 eval pattern 妫€鏌ョ粨鏋?
- <鍔熻兘浠跨湡鐘舵€侊紱闄ら潪鐪熷疄杩愯杩囦豢鐪?鍗忓悓浠跨湡锛屽惁鍒欏啓 "Not run">
````

濡傛灉鐢ㄦ埛瑕佹眰鍐呰仈杈撳嚭鑰屼笉鏄枃浠讹紝鍒欏湪鍝嶅簲涓繑鍥?SystemVerilog 浠ｇ爜銆傚惁鍒欎紭鍏堣緭鍑烘枃浠躲€?
## 璐ㄩ噺妫€鏌ユ竻鍗?/ Final Checklist

- 姣忎釜婧?clocked process 閮芥槧灏勫埌 `always_ff`锛屽苟淇濈暀姝ｇ‘ edge 鍜?reset 琛屼负銆?- 姣忎釜 combinational process 閮芥槧灏勫埌 `always_comb` 鎴?`assign`锛屾病鏈夌己澶遍粯璁ゅ€兼垨涓嶅畬鏁村垎鏀鑷?latch 鎺ㄦ柇銆?- 姣忎釜 signed 鍊煎湪澹版槑鎴栬〃杈惧紡涓婁笅鏂囦腑浠嶄繚鎸?signed銆?- 姣忎釜 resize銆乻ign extension銆亃ero extension銆乼runcation銆乻hift銆乧omparison 鍜?cast 閮芥湁鍙楁帶浣嶅琛屼负銆?- 姣忎釜鐢ㄤ簬 RTL 瀛樺偍鐨勫彈绾︽潫 VHDL integer/subtype 閮芥湁鏄惧紡 `logic`/`logic signed` 浣嶅锛屾垨鏈夊叿浣?Manual Review Item 瑙ｉ噴涓轰粈涔堜繚鐣?`int`銆?- 姣忎釜 VHDL `shift_left` / `shift_right` / shift operator 閮芥槧灏勪负姝ｇ‘鐨?SV operator 鎴?helper锛屽苟宸插鏌?signedness銆佸～鍏呰涓恒€佺粨鏋滀綅瀹藉拰绉讳綅閲忋€?- 姣忎釜 `downto` / `to` range 閮借淇濈暀锛屾垨宸插畬鏁撮噸鏄犲皠銆?- 姣忎釜 array dimension 閮芥牴鎹?element width 涓?array depth 姝ｇ‘琛ㄧず涓?packed 鎴?unpacked銆?- 姣忎釜 dynamic-width VHDL function 閮戒娇鐢ㄦ槑纭瓥鐣ワ紝骞惰褰曚换浣曚緥澶栥€?- 姣忎釜楂橀闄╃敓鎴愮粨鏋勯兘鏈夊眬閮ㄤ腑鏂?`// VHDL2SV:` 娉ㄩ噴锛屽苟鍦?Conversion Notes 鎴?Manual Review Items 涓湁瀵瑰簲璇存槑銆?- 姣忎釜浜哄伐瀹℃煡椤归兘鍏蜂綋涓斿彲鎵ц銆?- 鐢熸垚鐨?SystemVerilog 閬靛惊 `references/code-style.md` 鎴栫洰鏍囦粨搴撳凡鏈夐鏍笺€?- 鍖呭惈 Validation Results锛屽苟鍖哄垎宸查€氳繃妫€鏌ャ€佽鍛娿€佸け璐ュ拰璺宠繃鐨勫閮ㄦ鏌ャ€?- 褰撶敓鎴?SV 鏂囦欢鍙敤鏃讹紝Validation Results 涓寘鍚?L2 Questa `vlog -sv` 璇硶缂栬瘧缁撴灉锛涘鏋滆烦杩囷紝鍒欏師鍥犲繀椤绘槑纭€?- 闄ら潪鐪熷疄杩愯杩囦豢鐪熸垨鍗忓悓浠跨湡锛屽惁鍒欎笉澹扮О鍔熻兘绛変环銆?
## 宸ュ叿涓庤剼鏈鐣?/ Tools and Scripts

浣跨敤 `scripts/verify_conversion.py` 瀵圭敓鎴?SV 涓庢簮 VHDL 鍙婂彲閫?eval 鏈熸湜鎵ц鍙噸澶嶉潤鎬侀獙璇併€傝鑴氭湰涓嶈繍琛?Efinity銆丵uesta 鎴栦换浣曠患鍚?浠跨湡娴佺▼銆俀uesta `vlog -sv` 璇硶缂栬瘧鏄崟鐙殑 L2 楠岃瘉姝ラ锛屽叿浣撴祦绋嬭 `references/verification-workflow.md`銆?
褰撳墠璇勪及 prompt 鍜岀粨鏋勫寲鏈熸湜浣嶄簬 `evals/evals.json`锛屾牱渚?VHDL case 浣嶄簬 `evals/cases/`銆?
## 鍙傝€冭祫鏂?/ References

鍙傝€冩枃浠朵綅浜?`references/`锛?- 杞崲澶嶆潅绫诲瀷銆佹暟缁勩€乺ecord銆佸睘鎬с€佺畻鏈綅瀹藉彉鍖栥€乸rocess銆乫unction銆乸ackage 鎴?generate 璇彞鍓嶏紝璇诲彇 `references/conversion-rules.md`銆?- 鍐欏叆鎴栫紪杈戠敓鎴愮殑 SystemVerilog 鍓嶏紝璇诲彇 `references/code-style.md`锛岄櫎闈炵洰鏍囦粨搴撳凡鏈夋洿鏄庣‘鐨勬湰鍦?SV 椋庢牸銆傝嫢鏈湴椋庢牸涓庢 reference 鍐茬獊锛岄伒寰湰鍦伴鏍硷紝骞惰鏄庢湁鎰忎箟鐨勫亸绂汇€?- 澶勭悊椤圭洰鍙傝€冩枃妗ｆ€荤粨鍑虹殑鍥伴毦鍦烘櫙鍓嶏紝璇诲彇 `references/special-conversion-strategies.md`锛歞ynamic-width function 绛栫暐銆乣resize` / `ext` / `sxt`銆乽nconstrained array 鍜?VHDL 灞炴€с€?- 鍐冲畾鐢熸垚 RTL 涓啓鍝簺娉ㄩ噴銆佸搷搴?notes 涓啓鍝簺璇存槑鍓嶏紝璇诲彇 `references/annotation-policy.md`銆?- 楠岃瘉鐢熸垚 SV 鎴栨姤鍛婅浆鎹㈣川閲忓墠锛岃鍙?`references/verification-workflow.md`銆?- 杩斿洖鏈€缁堜唬鐮佹垨杩佺Щ瀹℃煡鍓嶏紝璇诲彇 `references/review-checklist.md`銆?