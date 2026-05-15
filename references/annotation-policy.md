# Annotation Policy

Use this policy to decide where conversion explanations belong. Generated RTL should stay readable; notes should carry most migration context.

## Required Notes

Document these in Conversion Notes or Manual Review Items:
- `resize`, `ext`, or `sxt` conversion, including whether zero-extension, sign-extension, or truncation was used.
- Any width truncation, sign reinterpretation, or cast that can change numeric value.
- Any signed/unsigned decision that affects comparison, shift, resize, or arithmetic.
- Any `downto` / `to` direction normalization or attribute replacement.
- Dynamic-width function strategy selection: Strategy 1 virtual class, Strategy 2 module-local parameterized function, or Strategy 3 fixed-width package specializations.
- VHDL procedure conversion strategy: inline logic, `function automatic`, `function automatic void`, or packed struct return. Note why SV `task` was not used when the source looked task-like.
- Constrained VHDL integer/subtype conversion, especially when the original type is used as hardware storage, array element, record/struct field, port, counter, or pipeline state. Include the original range/prototype and the derived SV width.
- VHDL shift function/operator conversion, including `shift_left`, `shift_right`, `sll`, `srl`, `sla`, and `sra`, when signedness, fill behavior, result width, or shift amount width matters.
- Unconstrained array conversion and the concrete object-level or parameterized bound used.
- Declaration initialization when it may or may not correspond to hardware reset.
- `buffer`, `inout`, `open`, tri-state, multi-driver, resolved type, or architecture/configuration assumptions.

## Required RTL Comments

Add a short `// VHDL2SV:` comment next to local migration decisions that a future reader must see next to the code. Keep the `VHDL2SV:` prefix exactly as written for searchability, and write the explanation after the prefix in Chinese. This is mandatory for:
- Intentional truncation.
- Explicit zero extension or sign extension for `resize`, `ext`, or `sxt`.
- Any signedness reinterpretation that affects arithmetic, comparison, or shift behavior.
- Any constrained VHDL integer/subtype converted to fixed-width `logic` / `logic signed` for RTL storage. Quote or summarize the original VHDL range/prototype.
- Any VHDL `shift_left` / `shift_right` or non-trivial shift operator conversion where logical vs arithmetic shift, result width, or fill bits could affect behavior.
- Direction normalization or index remapping.
- VHDL attribute replacement when the chosen SV code uses explicit indexes, `$bits`, `$size`, or localparams.
- A module-local replacement of a VHDL dynamic-width function.
- A fixed-width specialization that covers only specific widths.
- Non-obvious VHDL procedure conversion to inline logic or a zero-time function.
- Unconstrained array conversion where the SV object uses a concrete object-level or parameterized bound.
- `buffer`, `inout`, tri-state, `open`, or multi-driver handling that is preserved or intentionally changed.

Preferred comment format:

```systemverilog
// VHDL2SV: 对 resize(signed(b), 16) 做符号扩展，符号位来自 b[7]。
assign ys = {{8{b[7]}}, b};

// VHDL2SV: target_scale_t 来自 VHDL integer range -2**exponent_high 到 2**exponent_high-1，使用 exponent_high+1 位有符号定宽。
typedef logic signed [TARGET_SCALE_W-1:0] target_scale_t;

// VHDL2SV: VHDL shift_right(signed(a), n) 需要算术右移，SV 使用显式 signed 操作数。
assign y = $signed(a) >>> n;
```

Keep the comment local and factual. Use Chinese for the explanation text. Do not use long paragraphs in generated RTL; put detailed reasoning in Conversion Notes.

Do not comment obvious syntax mappings such as:
- `std_logic` to `logic`.
- `rising_edge(clk)` to `posedge clk`.
- `&` to `{...}` when the concatenation is straightforward and already noted.
- `when others` to `default`.

## Manual Review Items

Create a Manual Review Item when:
- The conversion depends on target synthesis-tool support.
- The source contains unsupported or ambiguous VHDL.
- A generated function specialization does not cover all possible original call widths.
- A constrained integer range cannot be converted to a proven fixed width, or the generated code intentionally keeps SV `int` for a value that might become hardware storage.
- A VHDL shift function/operator cannot be proven logical vs arithmetic, or the result width/fill behavior depends on package overload resolution that was not fully resolved.
- A reset, initialization, or port default cannot be proven equivalent.
- Simulation, cosimulation, or synthesis has not been run but the user asks about functional or tool pass/fail status.
