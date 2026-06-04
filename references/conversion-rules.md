# VHDL to SystemVerilog Conversion Rules

This reference summarizes the project rules for synthesizable VHDL-to-SystemVerilog migration. P0 rules are high-risk and should be checked for every conversion. P1 rules are common and important. P2 rules are basic lookup items.

## Type Mapping

| ID | Priority | VHDL | SystemVerilog | Rule |
| --- | --- | --- | --- | --- |
| T-001 | P1 | `std_logic`, `std_ulogic` | `logic` | Preserve 4-state semantics. Do not collapse to `bit` unless explicitly safe. |
| T-002 | P1 | `bit`, `bit_vector` | `bit`, `bit [...]` | Use only when the source is explicitly 2-state or the project requires 2-state logic. |
| T-003 | P0 | `std_logic_vector(M downto N)`, `(N to M)` | `logic [L:R]` | Read and preserve declared direction by default. Do not flip ranges unless all indexes/slices/attributes are remapped. |
| T-004 | P0 | `signed`, `unsigned` | `logic signed [...]`, `logic [...]` | Preserve signedness in declarations and expressions. Signedness affects comparison, right shift, resize, and extension. |
| T-005 | P0 | `integer`, `natural`, `positive`, `integer range` | `int`, `int unsigned`, or fixed-width `logic` | Determine usage. Hardware storage with a known range must use a derived fixed-width `logic`/`logic signed` type unless a documented manual-review reason keeps `int`. Generic/parameter values can remain typed parameters with constraints noted. |
| T-006 | P0 | `subtype idx_t is integer range 0 to 15` | `typedef logic [3:0] idx_t` | Preserve range information when the subtype represents hardware bits, counters, indexes, array elements, record fields, ports, or pipeline state. |
| T-009 | P0 | `integer range -2**N to 2**N-1` | `logic signed [N:0]` or named typedef | This is an exact two's-complement signed range using `N+1` bits. Do not map storage of this type to 32-bit `int` unless explicitly reviewed. Add a `VHDL2SV:` comment with the original range. |
| T-007 | P1 | VHDL enum | `typedef enum logic[...]` | Infer explicit enum width from state count. Avoid tool-dependent implicit enum sizes. |
| T-008 | P2 | `character`, `string` | `byte`, `string`, byte array, or fixed logic vector | Decide whether the string is text metadata, a fixed indexed array, or synthesizable data. |

## Declaration Mapping

| ID | Priority | VHDL | SystemVerilog | Rule |
| --- | --- | --- | --- | --- |
| D-001 | P1 | `signal`, `variable`, `constant` | module `logic`, local variable, `localparam` | Complete type mapping first, then choose declaration scope. |
| D-002 | P1 | `in`, `out`, `inout`, `buffer`, `linkage` | `input`, `output`, `inout`, reviewed special case | `buffer` often needs output plus internal mirror. `linkage` should not be auto-converted. `inout` requires tri-state review. Do not emit explicit `var` port kinds (`input var`, `output var`, `inout var`) for synthesizable RTL; use plain typed ports or flatten/wrap complex interfaces for portability. |
| D-003 | P1 | `generic` | `parameter` | Externally configurable VHDL generics become SV parameters. Derived internal constants become `localparam`. |
| D-004 | P1 | declaration initial value | declaration init, reset logic, or combinational default | VHDL initialization is not always equivalent to a hardware reset. Flag it for review unless project conventions are known. |

## Instantiation

| ID | Priority | VHDL | SystemVerilog | Rule |
| --- | --- | --- | --- | --- |
| I-001 | P1 | `component` / `entity work.mod(arch)` instantiation | module instance | Convert to module instance, preserve instance name, and review architecture/configuration dependency. |
| I-002 | P1 | `generic map`, `port map` | `#(...)`, `(...)` | Prefer named parameter and port associations. Do not degrade named association to positional association. |
| I-003 | P1 | `open` | `.port()` or tie-off | Only leave open when the port direction and module contract allow it. Inputs need explicit review. |

## Attributes, Widths, Indexes, and Literals

| ID | Priority | VHDL | SystemVerilog | Rule |
| --- | --- | --- | --- | --- |
| A-001 | P0 | `a'length` | `$bits(a)`, `$size(a)`, or explicit parameter | Determine whether `a` is a packed vector, unpacked array, or element type. |
| A-002 | P0 | `for i in a'range loop` | explicit bounds | Preserve loop direction if it affects behavior. Do not make reverse loop counters unsigned by accident. |
| A-003 | P0 | `a'left`, `a'right`, `a'high`, `a'low` | explicit index or SV query | These are index values, not data bits. Use explicit indexes when safer. |
| A-004 | P0 | `downto`, `to` | preserve or controlled normalization | Default is preservation. Direction normalization requires global index/slice rewrite and a risk note. |
| A-005 | P1 | `a(i)`, `a(7 downto 0)` | `a[i]`, `a[7:0]` | Check whether `a` is packed vector or unpacked array before replacing parentheses. |
| A-006 | P0 | `resize(unsigned(a), N)` | zero-extend or truncate | Compare source and target widths. `$unsigned(a)` alone may rely on LHS width and may be insufficient. |
| A-007 | P0 | `resize(signed(a), N)` | sign-extend or truncate | Wider target extends sign bit; narrower target truncates low bits and needs a risk note. |
| A-008 | P0 | `ext(a, N)` | zero-extension or low-bit truncation | Treat as unsigned extension. Prefer explicit concatenation when width is known. |
| A-009 | P0 | `sxt(a, N)` | sign-extension or low-bit truncation | Extend from the source sign bit even when source type is `std_logic_vector`. |
| A-010 | P0 | `signed(a)`, `unsigned(a)` | `$signed(a)`, `$unsigned(a)` | These change interpretation, not necessarily width. Control expression widths explicitly in arithmetic. |
| A-011 | P1 | `"001" & abc`, `a & b` | `{3'b001, abc}`, `{a, b}` | VHDL `&` is concatenation. Never map it to SV bitwise `&`. |
| A-012 | P1 | `2 ** N` | width-controlled `1 << N` | For powers of two, prefer a sized shift expression. Unsized `1` can create width bugs. |
| A-013 | P2 | `x"FF"`, `o"17"`, `b"1010"` | `8'hFF`, `6'o17`, `4'b1010` | Always write explicit width. Octal contributes 3 bits per digit. |
| A-014 | P1 | `'0'`, `'1'`, `'Z'`, `'X'`, `'U'`, `'W'`, `'L'`, `'H'`, `'-'` | `1'b0`, `1'b1`, `1'bz`, `1'bx`, review others | Only 0/1/Z/X map directly. Other resolved values require project policy or review. |

## Constrained Integer Widths

VHDL integer ranges carry semantic constraints that SV `int` does not preserve. SV `int` is a 32-bit signed 2-state type. Use it only for compile-time constants, loop variables, temporary arithmetic, or intentionally 32-bit scalar APIs. For hardware storage, derive a fixed-width `logic` type and keep the VHDL prototype visible to reviewers.

Rules:
- For nonnegative ranges `0 to MAX`, use the minimum unsigned width that can represent `MAX`, for example `0 to 15` -> `logic [3:0]`.
- For ranges `-2**N to 2**N-1`, use signed width `N+1`, for example `logic signed [N:0]`.
- For symbolic bounds, create a named `localparam int unsigned <NAME>_W` or a named typedef, then use `logic [<NAME>_W-1:0]` / `logic signed [<NAME>_W-1:0]`.
- When the exact width cannot be proven, choose a conservative explicit `logic` width based on the source range expression when possible, and add a Manual Review Item rather than silently using `int`.
- Add a Chinese `// VHDL2SV:` comment near the typedef/declaration. Include the original VHDL subtype or range summary.

Pattern:
```systemverilog
// VHDL2SV: intarray 鍏冪礌鏉ヨ嚜 integer range -2**exponent_high 鍒?2**exponent_high-1锛屼娇鐢?exponent_high+1 浣嶆湁绗﹀彿瀹氬琛ㄧず銆?localparam int unsigned TARGET_SCALE_W = exponent_high + 1;
typedef logic signed [TARGET_SCALE_W-1:0] target_scale_t;
typedef target_scale_t intarray [number_of_denormalizer_pipeline_stages:0];
```

## Arrays and Composite Types

| ID | Priority | VHDL | SystemVerilog | Rule |
| --- | --- | --- | --- | --- |
| ARR-001 | P1 | constrained array of vector | unpacked array with packed element | Keep element width and array dimension separate: `logic [7:0] arr [0:3]`. |
| ARR-002 | P0 | unconstrained array | object-level fixed array or parameterized bound | Do not translate RTL unconstrained arrays to SV dynamic arrays. Find actual bounds at use sites. |
| ARR-003 | P1 | generic-sized array | parameter plus fixed unpacked array | Preserve `DEPTH`/`WIDTH` parameters and consider adding validity checks. |
| ARR-004 | P1 | array port | unpacked array port or flattened bus | Choose based on project/tool interface rules. If flattening, provide pack/unpack mapping. |
| ARR-005 | P1 | multidimensional array | packed/unpacked dimensions by intent | Decide whether the object is memory-like storage or a packed bus/lane structure. |
| R-001 | P0 | `record` | `typedef struct packed` or `struct` | Use `packed` only when all fields are packed fixed-width elements and the record behaves like a packed bus. When a record becomes a struct used on a module port, keep the port declaration plain typed without `var`, or flatten/wrap the interface if synthesis or mixed-language tools require it. |
| R-002 | P1 | record containing array | struct with packed or unpacked array field | Packed structs cannot contain unpacked arrays. Choose by field semantics. |
| R-003 | P1 | array of record | `record_t arr [range]` | Preserve readability and hierarchy unless flattening is required. |
| R-004 | P0 | nested records/arrays/subtypes | layered typedefs | Convert leaf types first, then build composite typedefs. Avoid unreadable one-shot flattening. |

## Statements and Processes

| ID | Priority | VHDL | SystemVerilog | Rule |
| --- | --- | --- | --- | --- |
| S-001 | P0 | `variable :=`, `signal <=` | blocking `=`, nonblocking `<=`, or continuous assign | Determine process type before choosing assignment operator. |
| S-002 | P0 | combinational process | `always_comb` with blocking assignments | Add default assignments or complete branches to avoid latches. |
| S-003 | P0 | clocked process with `rising_edge` / `falling_edge` | `always_ff @(posedge/negedge clk)` | Use nonblocking assignments for registered state. Preserve reset behavior and polarity. |
| S-004 | P0 | process-local variable | local blocking variable or next-state refactor | Check if the variable carries state across cycles. If so, model it as a register. |
| S-005 | P1 | `(others => '0')` | `'0`, `'1`, or `'{default:...}` | Choose based on packed vector vs array/struct target. |
| S-006 | P2 | `if` / `elsif` / `else` | `if` / `else if` / `else` | Review branch completeness in combinational logic. |
| S-007 | P2 | `case`, `when others` | `case`, `default` | Preserve selector width and literal width. |
| S-008 | P1 | static `for` loop | `for` loop | Prefer static bounds for synthesizable RTL. Dynamic `while`/unbounded loops need review. |
| S-009 | P1 | simple concurrent assignment | `assign` | Use `assign` for simple continuous combinational wiring. Use `always_comb` for multi-branch logic. |

## Functions, Procedures, Packages, and Generate

| ID | Priority | VHDL | SystemVerilog | Rule |
| --- | --- | --- | --- | --- |
| F-001 | P1 | fixed-width function | `function automatic` | Make return width and argument widths explicit. |
| F-002 | P0 | function with unconstrained or dynamic-width vector args/returns | required by default: parameterized `virtual class` + `static function automatic` | Do not blindly convert to an unsized SV function, inline fixed-width logic, or specialize based only on current call sites. Width-dependent functions need the Strategy 1 class pattern unless a documented project/tool/user exception applies. |
| F-003 | P1 | procedure | default: `function automatic`, `function automatic void`, or inline logic | Do not generate `task` for synthesizable RTL by default. Use a zero-time function or inline logic; flag timing/stateful procedures for review. |
| F-004 | P1 | `constant`/`variable`/`signal` parameters | `input`, `output`, `inout`, `ref` | Infer direction from read/write behavior, not keyword replacement. |
| F-005 | P1 | `package` / `package body` | `package ... endpackage` | Usually merge declarations and bodies into one SV package. |
| F-006 | P2 | `library` / `use` | `import pkg::*` | Convert user packages. Standard IEEE imports usually disappear after type conversion. |
| G-001 | P1 | generic-derived constant | `localparam` | Use `$clog2` carefully and review edge cases like `DEPTH == 1`. |
| G-002 | P1 | `for generate` | `genvar` and `generate for` | This is elaboration-time structure, not procedural runtime looping. |
| G-003 | P1 | `if generate` | `generate if` | Preserve generate labels where useful. |

### Synthesizable Procedure Conversion

VHDL `procedure` is a subprogram without a return value, but RTL conversion should not mechanically map it to SV `task`. In this project, `task` is not the default RTL style because it can hide timing intent and is often associated with testbench/process behavior.

Preference order:

1. Inline the procedure body when it is short, called once, or tightly coupled to one process.
2. Convert to `function automatic` with a typed return value when the procedure computes one result.
3. Convert to `function automatic void` with explicit `output` / `inout` arguments when the procedure computes multiple combinational outputs and keeping a subprogram improves readability.
4. Use a packed struct return when multiple related outputs naturally form one packed result.
5. Emit a manual-review item when the procedure has waits, delays, file I/O, shared variables, hidden state, signal timing dependencies, or ambiguous `signal` parameters.

SV patterns:

```systemverilog
function automatic logic [W-1:0] calc_next(input logic [W-1:0] a);
  return a + {{(W-1){1'b0}}, 1'b1};
endfunction
```

```systemverilog
function automatic void decode(
  input  logic [1:0] sel,
  output logic       en,
  output logic [3:0] mask
);
  en = 1'b0;
  mask = '0;
  case (sel)
    2'd1: begin
      en = 1'b1;
      mask = 4'h1;
    end
    default: begin
    end
  endcase
endfunction
```

Rules:
- Keep converted procedures zero-time and combinational.
- Do not place nonblocking assignments inside a converted function. If the VHDL procedure is called in a clocked process, compute next values in locals/function outputs and assign registers with `<=` in the surrounding `always_ff`.
- Do not convert `signal` parameters by keyword alone. Infer whether the parameter is read, written, or both, and whether the original procedure relied on signal update timing.
- Add a `// VHDL2SV:` Chinese comment next to non-obvious procedure inlining or function conversion.
- Only use `task` when the user explicitly requests task-based output and confirms the synthesis/style requirement; otherwise list it as a rejected option in Conversion Notes.

### Dynamic-Width VHDL Function Strategies

Use these strategies when a VHDL function depends on argument width, return width, `a'length`, `a'range`, unconstrained vector parameters, or call-site-specific resize/extension behavior. This is a high-risk area because ordinary SV functions require explicit packed dimensions; a direct text conversion can accidentally freeze the width or depend on the wrong left-hand side width. Treat these functions as dynamic-width even when the body is simple or all current call sites are known.

Preference order:

1. Use Strategy 1 by default: `virtual class` with parameterized `static function automatic`.
2. Use Strategy 2 only when the user requests module-local conversion or the function is tightly coupled to one module instance and should follow module parameters. Document why Strategy 1 was not used and which module parameters now define the function width contract.
3. Use Strategy 3 only when project/tool style forbids parameterized classes, or when the function is public but the call graph uses a small stable set of fixed widths. Document every generated specialization and any uncovered-call risk.

#### Strategy 1: Parameterized virtual class + static function automatic

Use this for reusable dynamic-width VHDL functions and for local functions with unconstrained vector arguments or returns unless an explicit exception applies. The class parameters carry call-site widths, and the static function keeps the call style compact without creating an object. Mark the class `virtual` to make clear it is a namespace/utility container, not hardware state.

VHDL:
```vhdl
function zext(a : std_logic_vector; n : natural) return std_logic_vector is
  variable r : std_logic_vector(n-1 downto 0);
begin
  r := (others => '0');
  r(a'length-1 downto 0) := a;
  return r;
end function;
```

SV pattern:
```systemverilog
virtual class zext_fn #(parameter int IN_W = 1, parameter int OUT_W = IN_W);
  static function automatic logic [OUT_W-1:0] call(input logic [IN_W-1:0] a);
    logic [OUT_W-1:0] r;
    r = '0;
    r[IN_W-1:0] = a;
    return r;
  endfunction
endclass

assign y = zext_fn#(.IN_W($bits(a)), .OUT_W($bits(y)))::call(a);
```

Rules:
- Pass every dynamic width as a class parameter such as `IN_W`, `OUT_W`, `ELEM_W`, or `DEPTH`.
- Use `$bits(signal)` at call sites when it cleanly represents the source or destination width.
- Preserve signedness explicitly in class parameters and return declarations. For sign extension, use `logic signed` where the returned value must be signed, and document the sign-bit source.
- Keep the function pure combinational. Do not put state, timing controls, or non-synthesizable behavior inside the class function.
- Add a conversion note that this is a parameterized static utility replacing a VHDL dynamic-width function.
- Do not replace this strategy with direct inline assignments just because the function body is simple. Inlining removes the reusable width contract that the VHDL unconstrained function expresses.

#### Strategy 2: Move function logic into a parameterized module

Use this when the VHDL function is only meaningful inside one module, depends on that module's generics, or produces hardware that is clearer as explicit combinational logic. This avoids a global utility class and lets module parameters control widths.

Use this strategy for:
- A function declared in an architecture and used only inside that architecture.
- A group of local functions that share the same module parameters such as `IN_W`, `OUT_W`, `FRAC_W`, `EXP_W`, or `LANES`.
- A conversion target whose synthesis style avoids parameterized classes but allows ordinary module parameters and local functions.
- A function whose inputs are runtime signals but whose widths are elaboration-time constants.

Do not use this strategy for:
- A VHDL package function called by multiple unrelated modules with different width contracts.
- A function that should remain importable from a package.
- A case where moving the logic into one module would force duplicated code in several modules; prefer Strategy 1 or Strategy 3.

SV pattern:
```systemverilog
module example #(parameter int IN_W = 8, parameter int OUT_W = 16) (...);
  function automatic logic [OUT_W-1:0] zext_local(input logic [IN_W-1:0] a);
    logic [OUT_W-1:0] r;

    r = '0;
    r[IN_W-1:0] = a;
    return r;
  endfunction

  assign y = zext_local(a);
endmodule
```

Rules:
- Promote every width that was dynamic in VHDL into a module `parameter` or `localparam`; do not leave the function return or argument dimensions implicit.
- Keep the local function pure combinational and `automatic`.
- If the function has one simple call site, either keep it as a local function or expand it into `always_comb` / `assign` logic, whichever is clearer for review.
- If several local functions share the same width parameters, define those parameters once in the module and use them consistently in every local function signature.
- Use assertions, parameter checks, or manual-review notes for illegal parameter combinations such as `OUT_W < IN_W` when truncation was not intended.
- Add a conversion note that the VHDL dynamic-width function was intentionally made module-local, and state that the function is no longer visible outside the module.
- Add a manual-review item if another module or package previously called the VHDL function, because external reuse would require Strategy 1 or Strategy 3.

#### Strategy 3: Rewrite multiple fixed-width package functions

Use this when only a small known set of widths is needed, or when tools/project style do not allow parameterized class utilities in RTL packages. This is more verbose but easy for conservative synthesis flows to understand.

Use this strategy for:
- A VHDL package function that is public and should remain a package utility.
- A project/tool flow that avoids parameterized classes in synthesizable RTL.
- A call graph where source and target widths are few, known, and stable.
- A review style that prefers explicit fixed-width RTL over generic width metaprogramming.

Do not use this strategy for:
- Open-ended or frequently changing width combinations.
- A package function whose callers derive widths from many independent generics.
- A function whose behavior depends on array depth, element width, signedness, and output width in many combinations; prefer Strategy 1 unless the project forbids it.

SV pattern:
```systemverilog
package conv_pkg;
  function automatic logic [15:0] zext8_to16(input logic [7:0] a);
    return {8'b0, a};
  endfunction

  function automatic logic [31:0] zext16_to32(input logic [15:0] a);
    return {16'b0, a};
  endfunction
endpackage
```

Rules:
- Name each specialization with source/target width or another unambiguous convention.
- Use this only when the width set is stable and small; otherwise Strategy 1 is preferred.
- Preserve the original package API intent by grouping specializations in the generated package and importing that package at call sites.
- Build the specialization list from real call sites, not from guesswork. Record each covered `(input width, output width, signedness)` tuple.
- Use explicit extension/truncation logic inside each specialization. Do not rely on unsized constants or left-hand-side inference.
- Keep names deterministic, for example `zext8_to16`, `sxt12_to18`, or `resize_s8_to16`.
- Update every call site to call the matching specialization; do not leave an overloaded or dynamic call unresolved.
- Add a manual-review item if the original VHDL function could be called with widths not covered by the generated fixed-width functions.
- Add a conversion note that Strategy 3 trades reuse flexibility for conservative synthesis compatibility and explicit reviewability.

### Hard-Case Strategy Reference

See `special-conversion-strategies.md` for the decision workflow and expanded patterns for:
- Strategy 2 module-local dynamic-width functions.
- Strategy 3 fixed-width package specializations.
- H-002 `resize` / `ext` / `sxt` conversion.
- H-003 range-unconstrained arrays.
- H-004 `'length`, `'range`, `'left`, and `'right` attributes.

## Operators and Casts

| ID | Priority | VHDL | SystemVerilog | Rule |
| --- | --- | --- | --- | --- |
| OP-001 | P2 | `/=` | `!=` | Use `!==` only if X/Z comparison semantics are intentionally required. |
| OP-002 | P1 | `and`, `or`, `not`, `xor`, `xnor` | bitwise or logical operators | Use operand types to choose bitwise vs logical operators. |
| OP-003 | P1 | `sll`, `srl`, `sla`, `sra`, `shl`, `shr` | `<<`, `>>`, `<<<`, `>>>` | Arithmetic right shift needs signed operand or `$signed(...) >>>`. Document any non-trivial signedness/fill/result-width decision. |
| OP-006 | P0 | `shift_left(a, n)`, `shift_right(a, n)` | `a << n`, `a >> n`, or `$signed(a) >>> n` | These are VHDL standard/package functions, not SV built-ins. Choose logical vs arithmetic behavior from the operand type and package semantics. If unclear, emit a `VHDL2SV:` comment and Manual Review Item. |
| OP-004 | P1 | `to_integer(unsigned(a))` | `int'($unsigned(a))` | Review target width. `int` is fixed-width and may truncate large vectors. |
| OP-005 | P1 | `to_unsigned(i,N)`, `to_signed(i,N)` | sized cast | Preserve target width `N` explicitly. |

## Vendor/UNISIM Primitive Substitution

When the target is a non-Xilinx platform, or the user requests generic synthesizable output, every Xilinx UNISIM primitive must be replaced with an equivalent generic SystemVerilog implementation. Each substitution must include a `// VHDL2SV:` Chinese comment identifying the original primitive.

### Combinational Primitives

| ID | Priority | VHDL Primitive | Generic SV Equivalent |
| --- | --- | --- | --- |
| VP-001 | P0 | `LUT1` (2-entry LUT) | `always_comb case({i0}) ...` or `assign o = lut_val[{i0}];` |
| VP-002 | P0 | `LUT2` (4-entry LUT) | `always_comb case({i1,i0}) ...` or `assign o = lut_val[{i1,i0}];` |
| VP-003 | P0 | `LUT3` (8-entry LUT) | `always_comb case({i2,i1,i0}) ...` or `assign o = lut_val[{i2,i1,i0}];` |
| VP-004 | P0 | `LUT4` (16-entry LUT) | `always_comb case({i3,i2,i1,i0}) ...` or `assign o = lut_val[{i3,i2,i1,i0}];` |
| VP-005 | P0 | `LUT5`/`LUT6` | Same pattern as LUT4, extended to 5 or 6 inputs |
| VP-006 | P0 | `MUXCY` (carry mux) | `assign o = s ? ci : di;` |
| VP-007 | P0 | `XORCY` (carry xor) | `assign o = ci ^ li;` |
| VP-008 | P0 | `MULT_AND` | `assign lo = a & b;` |
| VP-009 | P0 | `MUXF5`/`MUXF6`/`MUXF7`/`MUXF8` | `assign o = s ? i1 : i0;` |

### Sequential Primitives

| ID | Priority | VHDL Primitive | Generic SV Equivalent |
| --- | --- | --- | --- |
| VP-010 | P0 | `FD` (D flip-flop) | `always_ff @(posedge C) Q <= D;` |
| VP-011 | P0 | `FDE` (D flip-flop w/ CE) | `always_ff @(posedge C) if(CE) Q <= D;` |
| VP-012 | P0 | `FDRE` (D flip-flop w/ sync reset) | `always_ff @(posedge C) if(R) Q <= 0; else if(CE) Q <= D;` (check reset polarity from generic) |
| VP-013 | P0 | `FDSE` (D flip-flop w/ sync set) | `always_ff @(posedge C) if(S) Q <= 1; else if(CE) Q <= D;` |
| VP-014 | P0 | `FDRSE` (D flip-flop w/ reset+set) | `always_ff @(posedge C) if(R) Q <= 0; else if(S) Q <= 1; else if(CE) Q <= D;` |
| VP-015 | P0 | `FDCP`/`FDCPE` (async clear/preset) | `always_ff @(posedge C or posedge CLR or posedge PRE) ...` — flag for review: async control behavior must match original |
| VP-016 | P0 | `SRL16E` (16-bit shift register) | `always_ff @(posedge CLK) begin sr <= {sr[14:0], D}; end` + `assign Q = CE ? sr[A] : Q;` (check CE polarity from generic) |
| VP-017 | P0 | `SRLC32E`/`SRLC16E` | Same pattern as SRL16E extended to required depth |

### Carry Chain and Arithmetic Primitives

| ID | Priority | VHDL Primitive | Generic SV Equivalent |
| --- | --- | --- | --- |
| VP-020 | P0 | `CARRY4` | Behavioral: `assign {CO[3:0], O[3:0]} = {4'b0, S[3:0]} + {CYINIT, DI[2:0], CI};` — or manually expand the carry chain per-bit |
| VP-021 | P0 | `DSP48E1` | Parameterized behavioral: `P <= (A*B + C) or behavioral model with pipeline stages` — detailed DSP48 conversion is complex; when the full DSP48 feature set (pre-adder, cascade, pattern detect) is used, flag as Manual Review Item |
| VP-022 | P0 | `DSP48E2` | Same as DSP48E1 with wider buses |

### Clock and I/O Primitives

| ID | Priority | VHDL Primitive | Generic SV Equivalent |
| --- | --- | --- | --- |
| VP-030 | P0 | `BUFG` (global clock buffer) | `assign O = I;` — passthrough; clock routing is handled by the synthesis tool |
| VP-031 | P0 | `BUFH`/`BUFR`/`BUFIO` | `assign O = I;` — same passthrough |
| VP-032 | P0 | `IBUF`/`OBUF` | `assign O = I;` — passthrough |
| VP-033 | P0 | `IOBUF` (tri-state I/O) | `assign O = T ? 1'bz : I; assign IO = T ? 1'bz : I;` — flag for review, I/O buffer behavior depends on target technology |
| VP-034 | P0 | `MMCME2_ADV`/`PLLE2_ADV` | Flag as Manual Review Item — clock management tiles are inherently vendor-specific and cannot be trivially replaced |

### Block RAM Primitives

| ID | Priority | VHDL Primitive | Generic SV Equivalent |
| --- | --- | --- | --- |
| VP-040 | P0 | `RAMB18E1`/`RAMB36E1` (simple read/write) | Infer as generic RAM: `logic [W-1:0] mem [0:DEPTH-1]; always_ff @(posedge CLK) if(WE) mem[ADDR] <= DI; assign DO = mem[ADDR];` — but flag complex configurations (ECC, FIFO mode, cascade) as Manual Review Item |
| VP-041 | P0 | `RAMB18E1`/`RAMB36E1` (complex config) | Flag as Manual Review Item with the specific mode and port configuration |

### Substitution Rules

- **P0 rules**: Apply unconditionally for generic/non-Xilinx target. Do not instantiate the original primitive.
- **P1 rules**: Apply by default; only keep the original primitive if the user explicitly requests Xilinx-specific output.
- Every substitution must add a `// VHDL2SV:` comment next to the converted code: `// VHDL2SV: 原 Xilinx <primitive_name> 原语替换为通用逻辑`
- For LUTs with init values, embed the init value as a localparam and use it in the case statement or indexed select.
- For SRL16E, port `A[3:0]` selects which tap of the 16-element shift register is output; model this as a shift register with an addressable output.
- For DSP48 and complex BRAM, prefer behavioral descriptions (`a*b + c` for simple multiply-add) over trying to replicate every pipeline register exactly. Flag complex usage for manual review.
- Clock buffer (BUFG/BUFH/BUFR) passthrough: these are routing hints for the synthesis tool; a simple wire assignment is functionally correct for simulation and most synthesis tools will re-infer the appropriate clock resources.
- Do NOT emit `library UNISIM;` or `import unisim::*;` in generated SV.

## Final Conversion Checks

| ID | Priority | Check | Rule |
| --- | --- | --- | --- |
| C-001 | P0 | width and signedness | Recheck every assignment, arithmetic expression, comparison, shift, resize/ext/sxt, and cast. |
| C-002 | P0 | synthesizability | No dynamic arrays, unbounded loops, wait/file/access/protected constructs, accidental latches, or multiple drivers unless intentionally reviewed. Also: no vendor-specific primitives (UNISIM, ALTPRIM, etc.) unless the user explicitly requested vendor-specific output. |
| C-003 | P0 | response format | Return converted SV, key mapping notes, risks/manual confirmations, and a synthesizability checklist. |
| C-004 | P0 | vendor primitives | All Xilinx UNISIM (LUT*, SRL16E, FD*, MUXCY, XORCY, MULT_AND, CARRY*, DSP48*, BUFG, RAMB*, etc.) have been replaced with generic synthesizable equivalents. |
