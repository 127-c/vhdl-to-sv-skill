# Review Checklist

Use this checklist before returning converted SystemVerilog.

## Semantic Checks

- Every source clocked process is mapped to `always_ff` with the correct edge and reset behavior.
- Every combinational process is mapped to `always_comb` or `assign` without missing default assignments or incomplete branches that infer latches.
- Every VHDL `signal <=` / `variable :=` assignment was converted according to process semantics, not by raw token replacement.
- Every signed value remains signed in declaration or expression context.
- Every constrained VHDL integer/subtype used as RTL storage, array element, record/struct field, port, counter, or pipeline state has a derived fixed-width `logic` / `logic signed` type, or a specific Manual Review Item explaining why SV `int` was retained.
- Every synthesizable VHDL procedure is converted without SV `task` by default: use inline logic, `function automatic`, `function automatic void`, or a packed struct return.
- Every dynamic-width VHDL function uses the selected strategy deliberately: preferably `virtual class` + `static function automatic`, otherwise module-parameterized logic or fixed-width package specializations with a clear reason, covered width contract, and reuse limitation.
- Every resize, sign extension, zero extension, truncation, shift, comparison, and cast has controlled width behavior.
- Every use of `resize`, `ext`, or `sxt` is implemented as explicit zero/sign extension, truncation, or a documented `$signed` / `$unsigned` shorthand with target-width proof.
- Every VHDL `shift_left`, `shift_right`, `sll`, `srl`, `sla`, or `sra` conversion has reviewed logical/arithmetic behavior, fill bits, result width, shift amount width, and signedness.
- Every range-unconstrained VHDL array has an object-level range or parameterized bound in SV; no dynamic array is introduced for RTL.
- Every VHDL attribute conversion distinguishes packed vector width, unpacked array depth, element width, and index value.
- Every `downto` / `to` range is preserved or fully remapped across declarations, indexes, slices, attributes, and loops.
- Every array dimension is correctly represented as packed or unpacked based on element width vs array depth.
- Every record maps to `struct packed` only when all fields can legally be packed.

## Synthesizability Checks

- No dynamic arrays are introduced for RTL unconstrained arrays.
- No `file`, `access`, `protected`, `physical`, text I/O, or wait-based testbench behavior is silently converted.
- No ambiguous `buffer`, `linkage`, `inout`, multi-driver, tri-state, or resolved-type behavior is hidden.
- No clock/reset or declaration initialization assumption is presented as certain unless proven from context.
- Generate constructs use elaboration-time `generate`, `genvar`, and parameters rather than procedural runtime logic.
- No Xilinx UNISIM or other vendor-specific primitives (LUT*, SRL16E, FD*, MUXCY, XORCY, MULT_AND, CARRY*, DSP48*, BUFG, RAMB*, etc.) remain in generated SV unless the user explicitly requested vendor-specific output. Each removed primitive has a corresponding generic logic replacement with a `// VHDL2SV:` comment.

## Output Checks

- The SV code is syntactically coherent and uses `logic`, `always_ff`, `always_comb`, `assign`, `typedef`, `parameter`, and `localparam` consistently.
- Constrained integer-derived typedefs/declarations include local Chinese `// VHDL2SV:` comments with the original VHDL range/prototype.
- Non-trivial VHDL shift conversions include local Chinese `// VHDL2SV:` comments or explicit Manual Review Items.
- Module ports use explicit directions, types, and packed dimensions.
- Synthesizable module ports do not use explicit `var` port kinds (`input var`, `output var`, `inout var`).
- Instantiations use named parameter and port connections where possible.
- Manual review items are specific and actionable.
- Conversion notes explain non-trivial choices without burying the code.
- Strategy 2 conversions state that the function became module-local and name the parameters that define width.
- Strategy 3 conversions list all generated fixed-width package specializations and identify any missing call widths.
- Validation Results are present and clearly separate static conversion checks from unrun simulation or synthesis checks.
- Functional equivalence, Questa simulation, or Efinity synthesis success is not claimed unless those external checks were actually run.

## Code Style Checks

- Generated files follow `references/code-style.md` unless an existing target repository style clearly overrides it.
- Parameters are typed, derived constants are `localparam`, and width-sensitive literals are sized.
- Packed and unpacked dimensions are placed consistently and do not blur element width with array depth.
- Source names and ordering are preserved unless a rename or reorder is documented.
- Generated RTL is not cluttered with obvious comments; migration-sensitive assumptions are documented in notes.
- Every high-risk conversion that requires local context has a short Chinese `// VHDL2SV:` comment next to the generated RTL.

## Static Validation Checks

- `scripts/verify_conversion.py` was run when source VHDL and generated SV files were available, or the same L0/L1 checks were performed manually with a skipped-script reason.
- Eval `must_have` and `must_not_have` patterns were checked when the conversion corresponds to an eval case.
- Forbidden RTL/testbench constructs are absent unless the source was intentionally rejected or marked manual review.
- Suspicious `typedef int ... array`, `int` fields in structs that originate from constrained VHDL integer ranges, and unresolved VHDL shift function/operator conversions are either fixed or reported as warnings.
- L2-L4 tool checks are reported as not run in this conversion-only workflow unless the user separately requested them.
