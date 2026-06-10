---
name: vhdl-to-sv
description: Convert synthesizable VHDL RTL into equivalent SystemVerilog RTL and validate the generated conversion. Use this skill whenever the user asks to translate, migrate, rewrite, review, refactor, verify, or check VHDL into SV/SystemVerilog, especially for entity/architecture modules, packages, generics, ports, processes, signals, arrays, records, constrained integer ranges/subtypes, signed/unsigned arithmetic, resize/ext/sxt, shift_left/shift_right and other shifts, dynamic-width functions, module-local or package-specialized function strategies, unconstrained arrays, VHDL attributes, generate statements, VHDL indexing semantics, synthesizability review, or conversion quality reports. This skill is only for synthesizable RTL; it should flag testbench-only, behavioral, file I/O, access/protected/physical types, ambiguous tri-state/buffer behavior, and non-synthesizable constructs instead of blindly converting them.
---

# VHDL to SystemVerilog RTL Conversion

## 鏍稿績鐩爣 / Purpose

Convert synthesizable VHDL RTL into equivalent SystemVerilog RTL while preserving hardware behavior, bit widths, signedness, index directions, reset behavior, and combinational/sequential semantics.

Use this skill as a migration guide, not as a blind text rewriter. Preserve source semantics first, then apply project SystemVerilog style.

After conversion, validate the generated SV for syntax shape, synthesizability risk, rule consistency, reviewability, and Questa `vlog -sv` syntax compile when generated files and the tool are available. Questa `vlog` compile is a syntax/tool-acceptance check, not functional simulation. Do not claim functional equivalence unless a real simulation or cosimulation has been run outside this skill workflow.

## 閫傜敤鑼冨洿 / Scope

Convert synthesizable RTL by default.

Handle:
- `entity` / `architecture` to `module`
- `generic` / `constant` to `parameter` / `localparam`
- `port`, `signal`, `variable`, `subtype`, `type`, `enum`, `record`, and arrays
- concurrent assignments, combinational processes, clocked processes, functions, procedures, packages, and generate blocks
- VHDL bit/vector literals, concatenation, indexing, slices, attributes, signed/unsigned arithmetic, `resize`, `ext`, and `sxt`
- **Vendor/UNISIM primitive substitution**: Convert Xilinx UNISIM primitives (LUT1-6, SRL16E, FD/FDE/FDRE/FDSE, MUXCY, XORCY, MULT_AND, CARRY4, DSP48E1/E2, BUFG, RAMB*, etc.) into generic synthesizable SystemVerilog equivalents. Do NOT instantiate vendor primitives in generated SV output unless the user explicitly requests Xilinx-specific output.

Flag rather than blindly convert:
- `access`, `file`, `protected`, `physical`, most `real`/`time` RTL usages, dynamic allocation, text I/O, wait-based behavioral code, or testbench-only constructs
- ambiguous `buffer`, `linkage`, `inout`, multiple drivers, resolved logic behavior, declaration initialization, or clock/reset semantics
- unconstrained arrays without an object-level range or parameterized bound

## 浣跨敤妯″紡 / Usage Modes

Use the appropriate mode based on the user request and inputs:

- **VHDL to SV conversion**: Read `.vhd` / `.vhdl` source files or inline VHDL and generate equivalent `.sv` code or files.
- **SV migration review**: Review already converted SystemVerilog against the original VHDL, this skill's conversion rules, and the project style.
- **Conversion validation**: Check generated SV against the original VHDL, static conversion rules, synthesizability risk rules, annotation policy, and required output sections.
- **Rule explanation**: Explain how a specific VHDL construct should map to SystemVerilog, especially width, signedness, array, record, function, or process behavior.
- **Batch migration planning**: Inspect multiple VHDL files, identify packages and design-unit dependencies, propose compile order, then convert in dependency-aware order.

## 鎵ц娴佺▼ / Workflow

Follow these phases in order. Keep notes about assumptions, unsupported constructs, and manual-review items while working.

### Phase 0: 杈撳叆璇嗗埆 / Input Recognition

1. Locate source files first. When the user gives a path, read `.vhd` and `.vhdl` files from that file or directory. Do not ask the user to paste code when files are available in the workspace.
2. Classify each input as VHDL source, converted SV source, package, package body, entity, architecture, standalone function/procedure, or review-only artifact.
3. Identify whether the user wants file output, inline code, a review, or an explanation.
4. Decide output paths before conversion. By default, write each converted design unit to a sibling `.sv` file with the same base name, or to a user-specified output directory if provided. For packages, use `<package_name>_pkg.sv` when that is clearer than the source filename.
5. **检测供应商原语**: 扫描源文件中的 `library unisim;`、`library UNISIM;`、`use unisim.vcomponents.all;` 和供应商专用组件实例化（LUT*、SRL16E、FD*、MUXCY、XORCY、MULT_AND、CARRY*、DSP48*、BUFG、RAMB* 等）。标记这些需要进行通用逻辑转换。如果用户的目标平台不是 Xilinx，所有供应商原语必须替换为通用可综合等价实现。

### Phase 1: 涓婁笅鏂囧垎鏋?/ Context Analysis

1. Build file/design-unit context: identify packages, package bodies, entities, architectures, component declarations, dependencies, clocks, resets, generics, ports, internal declarations, processes, instances, and generate blocks.
2. Extract declarations before converting statements so expressions can use the correct SV types.
3. Classify each process or concurrent region as structural, combinational, sequential, package/type declaration, function/procedure, or unsupported/non-synthesizable.
4. For every VHDL function, check whether any argument, return value, local variable, assignment target, or attribute depends on call-site width, an unconstrained vector, `a'length`, `a'range`, or object-specific bounds.
5. Identify every constrained scalar type before converting composite types. In particular, record the original prototype for `integer range`, `natural range`, `positive range`, and subtypes used inside arrays, records, ports, signals, variables, or stored pipeline state.

### Phase 2: 瑙勫垯鍖归厤 / 绛栫暐閫夋嫨

1. Read `references/conversion-rules.md` before converting non-trivial types, arrays, records, attributes, arithmetic width changes, processes, functions, packages, or generate statements.
2. Read `references/code-style.md` before writing generated SystemVerilog unless the target repository already has a clearer local SV style. Follow the local style when it conflicts with this reference, and mention meaningful deviations.
3. Read `references/special-conversion-strategies.md` before handling dynamic-width functions, `resize` / `ext` / `sxt`, unconstrained arrays, or VHDL attributes such as `'length`, `'range`, `'left`, and `'right`.
4. Read `references/annotation-policy.md` before deciding whether a migration decision belongs in an RTL comment, Conversion Notes, or Manual Review Items.
5. Choose conversion strategies by behavior, not by syntax. Preserve source semantics before making style improvements.
6. Apply the dynamic-width function rule when required: prefer the parameterized `virtual class` plus `static function automatic` strategy; use module-parameterized or fixed-width package-specialization strategies only under the documented conditions.
7. Emit a manual-review item instead of guessing when semantics depend on target tool support, project coding style, reset convention, resolved logic behavior, or ambiguous VHDL constructs.
8. **Apply vendor primitive substitution**: When converting VHDL that instantiates Xilinx UNISIM or other vendor-specific primitives, replace each primitive with its generic synthesizable SystemVerilog equivalent per `references/conversion-rules.md` section "Vendor/UNISIM Primitive Substitution". Add a `// VHDL2SV:` comment marking the substitution. If a primitive cannot be cleanly replaced, flag it as a Manual Review Item.

### Phase 3: 缁撴灉鐢熸垚 / Result Generation

1. Generate SystemVerilog with explicit typed ports, explicit parameter types, controlled widths, stable naming, `logic`, `always_ff`, `always_comb`, named parameter overrides, and named port connections.
2. Convert clocked `rising_edge` / `falling_edge` processes to `always_ff` with nonblocking assignments for registers.
3. Convert combinational processes to `always_comb` with blocking assignments and explicit defaults when needed to avoid inferred latches.
4. Convert simple concurrent assignments to `assign` when continuous wiring is clearer.
5. Preserve or document compile order when multiple generated files share package dependencies.
6. Add required `// VHDL2SV:` comments next to high-risk converted RTL as defined by `references/annotation-policy.md`. Keep the `VHDL2SV:` prefix and write the explanation after it in Chinese. Keep each comment short and local; put broader caveats in Conversion Notes or Manual Review Items.

### Phase 4: 缁撴灉澶嶆煡 / Final Review

1. Read `references/review-checklist.md` and `references/verification-workflow.md` before returning final code or a migration review.
2. Recheck width, signedness, indexing direction, reset behavior, assignment timing, array dimensions, function widths, and unsupported constructs.
3. Verify that generated code follows `references/code-style.md` or the target repository's established style.
4. Run the default conversion-validation levels from `references/verification-workflow.md` when files are available: L0 report/format check, L1 static conversion check, and L2 Questa `vlog -sv` syntax compile. Do not run Efinity synthesis or `vsim` functional simulation in this workflow.
5. Use `scripts/verify_conversion.py` when source VHDL and generated SV files exist. If the script cannot run, perform the same static checks manually and state why the script was not run.
6. Run Questa syntax compile when generated SV files exist and `vlog`/`vlib` are available. Use dependency-aware file order where possible, especially packages before modules. If Questa is unavailable or compile cannot be run, mark L2 as `SKIP` with the reason.
7. Return generated files/code, conversion notes, manual-review items, synthesizability checklist, and validation results in the required output format.

## 鏍稿績瑙勫垯 / Core Rules

Prefer the smallest SystemVerilog that preserves behavior. Do not over-modernize the design if doing so changes indexing or hardware structure.

### 绫诲瀷 / Types

- Map `std_logic` and `std_logic_vector` to 4-state `logic` by default.
- Map VHDL `bit` / `bit_vector` to SV `bit` only when the source is explicitly 2-state or the user requests 2-state logic.
- Preserve `signed` using `logic signed [...]`; map `unsigned` to unsigned `logic [...]` unless an explicit signed cast is needed.
- For `integer range`, `natural`, `positive`, and `subtype`, infer a fixed width only when the object is a real hardware signal/counter/index. Otherwise use `int` / `int unsigned` with notes about original range constraints.
- For constrained integers used as stored RTL data, array elements, record/struct fields, ports, counters, or pipeline state, prefer explicit `logic` / `logic signed` with a derived fixed width. Add a local Chinese `// VHDL2SV:` comment that quotes or summarizes the original VHDL range/prototype.
- Use SV `int` only for compile-time parameters, loop variables, temporary calculations, or API-style scalar values where 32-bit signed semantics are intentional and do not become hardware storage. If uncertain whether the object is storage or calculation-only, use explicit `logic` for the stored object and list the uncertainty under Manual Review Items.

### 浣嶅涓庣储寮?/ Widths and Indexes

- Preserve `downto` / `to` directions by default. Only normalize to `[W-1:0]` if the user or project explicitly asks for it, and then rewrite every affected index, slice, range, and attribute.
- Treat VHDL attributes carefully. `a'length` may mean vector bit width, array depth, or element width depending on `a`; choose `$bits`, `$size`, or an explicit parameter accordingly.
- Never treat `$signed`, `$unsigned`, or a cast as a complete replacement for `resize`; explicit extension/truncation may be required.
- Use explicit sized literals for width-sensitive constants.

### 绗﹀彿涓庣畻鏈?/ Signedness and Arithmetic

- Preserve signedness in declarations and expression context.
- Make zero extension, sign extension, truncation, shift, comparison, and cast widths explicit.
- Convert `resize(unsigned(...), N)` to controlled zero-extension or truncation.
- Convert `resize(signed(...), N)` to controlled sign-extension or truncation.
- Convert VHDL `shift_left` / `shift_right` / `sll` / `srl` / `sla` / `sra` by operand semantics, not by function name alone. SV has shift operators (`<<`, `>>`, `<<<`, `>>>`), not a built-in RTL `shift_left` function. Use `<<` for logical left shift, `>>` for logical right shift, and `>>>` for arithmetic right shift with an explicitly signed operand when VHDL signed semantics require it.
- When the VHDL shift operand signedness, shift-fill behavior, result width, or shift amount width cannot be proven from declarations and context, keep the generated RTL conservative and add a Chinese `// VHDL2SV:` comment plus a Manual Review Item.

### 鏁扮粍銆乺ecord 涓?package / Arrays, Records, and Packages

- Keep packed vector width and unpacked array depth separate.
- Convert VHDL records to `struct packed` only when all fields can legally be packed fixed-width elements and the record behaves like a packed bus.
- Convert unconstrained arrays only after finding object-level bounds or parameterized bounds.
- Usually merge VHDL package declarations and package bodies into one SV package.

### 璇彞涓庤繘绋?/ Statements and Processes

- Convert VHDL `&` concatenation to SV `{...}`, not bitwise `&`.
- Convert VHDL boolean `and/or/not` to `&&/||/!` only for boolean conditions; use bitwise `&/|/~` for vector logic.
- Convert `others =>` based on the target type: packed vectors usually use `'0` / `'1`; arrays/structs use `'{default:...}`.
- Use `default:` for `when others` in `case` statements.
- Convert assignments according to process semantics, not by raw token replacement.
- Add a short Chinese `// VHDL2SV:` comment next to every high-risk generated construct: dynamic-width function strategy, intentional truncation, explicit sign/zero extension, direction/index remapping, unconstrained-array bound selection, declaration-initialization assumption, or reviewed `buffer`/`inout`/tri-state handling.
- Add a short Chinese `// VHDL2SV:` comment next to every constrained VHDL integer/subtype converted to a fixed-width `logic` type, including the original VHDL prototype or range summary.
- Add a short Chinese `// VHDL2SV:` comment next to every non-trivial VHDL shift-function/operator conversion when signedness, fill behavior, or result width matters.

### 渚涘簲鍟嗗師璇浆鎹?/ Vendor Primitive Substitution

When the target is a non-Xilinx platform or the user requests generic synthesizable output, every Xilinx UNISIM primitive instantiation must be replaced with a **functionally equivalent, timing-identical** generic SystemVerilog implementation. See `references/conversion-rules.md` section "Vendor/UNISIM Primitive Substitution" for detailed rules.

核心要求：
- **功能等价**：相同输入产生相同输出（bit-exact），相同周期精确时序（cycle-accurate latency）
- **逻辑时序相同**：保留原始复位/使能行为、流水线级数、数据路径宽度
- 每个替换必须添加 `// VHDL2SV:` 中文注释标明原始原语名称
- 不得在输出中保留 `library UNISIM;` 或供应商原语实例化
- 无法确认功能等价时标志为 Manual Review Item，不得猜测替换
- **供应商原语替换是本 skill "严禁行为级简化转换"P0 规则的例外**：允许在保证功能等价和时序相同的前提下生成结构级通用逻辑，不要求逐门复制原始原语内部 netlist

Procedure rules:
- Do not generate SV `task` for synthesizable RTL by default.
- Convert synthesizable VHDL `procedure` to `function automatic` when it is pure zero-time combinational logic. Use an explicit return type for one result, or `function automatic void` with `output` / `inout` arguments for multiple results when that is clearer than a struct return.
- Inline a VHDL `procedure` when it is simple, local to one process, or when signal assignment timing would be obscured by wrapping it in a function.
- For procedures called inside clocked processes, compute next values with blocking assignments or a function result, then update registers with nonblocking assignments in the surrounding `always_ff`.
- Flag procedures with waits, delays, file I/O, shared variables, hidden state, signal timing dependencies, or ambiguous `signal` parameters for manual review instead of converting them to `task`.

Validation rules:
- Perform validation after writing generated SV. At minimum, check required output sections, forbidden constructs, process mapping, width/signedness documentation, eval-specific expectations when an eval case applies, and Questa `vlog -sv` syntax compile when files and tools are available.
- Run Questa `vlog -sv` compile as the default tool syntax check for generated SV. This is not functional simulation and must not be reported as functional equivalence.
- Do not run Efinity synthesis or `vsim` simulation automatically. Questa functional simulation is a later functional-verification layer and is out of scope for this conversion-only workflow unless the user explicitly requests it and provides the test setup.
- Use `scripts/verify_conversion.py` for repeatable static conversion checks when source and generated files are available.

## 鐗规畩鍦烘櫙 / Special Cases

- For dynamic or unconstrained vector-width VHDL functions, use the project strategy in `references/conversion-rules.md`: parameterized `virtual class` plus `static function automatic`. Only use module-parameterized implementation or package-level fixed-width specializations when the user explicitly requests it, the project/tool style forbids parameterized classes, or the function is demonstrably not reusable; document that exception.
- For module-local dynamic-width functions, use module parameters to control all widths and keep the implementation inside the module only when the function is tightly coupled to that module's generics or call sites.
- For public dynamic-width functions with a small stable width set, create explicitly named fixed-width package specializations and list covered and uncovered width pairs.
- For VHDL procedures in synthesizable RTL, prefer `function automatic`, `function automatic void`, or inlining. Do not emit `task` unless the user explicitly requests a task-based style and confirms the target synthesis flow accepts it.
- For `buffer`, `linkage`, `inout`, tri-state behavior, multiple drivers, or resolved types, stop and emit a manual-review item with likely migration options.
- For declaration initialization, do not assume it is equivalent to hardware reset unless project convention or source context proves it.
- For VHDL `open` associations, check port direction and module contract before leaving the connection open or adding a tie-off.
- For architecture/configuration-specific instantiation, preserve or document the selected architecture/configuration dependency.

## 缁濅笉鍋氱殑浜?/ Do Not

- Do not silently convert unsupported, ambiguous, testbench-only, or non-synthesizable VHDL.
- Do not ask the user to paste code when readable files are available in the workspace.
- Do not normalize index directions unless every affected declaration, index, slice, range, attribute, and loop is remapped.
- Do not replace `resize`, `ext`, or `sxt` with only `$signed`, `$unsigned`, or an unsized cast.
- Do not silently map a constrained VHDL `integer range` used as hardware storage to SV `int`; `int` is 32-bit signed and does not preserve the VHDL range constraint.
- Do not leave VHDL `shift_left` / `shift_right` as function calls in generated SV unless a project-defined SV helper function with that exact contract is intentionally generated and documented.
- Do not introduce SV dynamic arrays, queues, stateful classes, timing controls, file I/O, or other unsynthesizable constructs for RTL migration.
- Do not generate SV `task` for RTL procedure conversion by default.
- Do not instantiate Xilinx UNISIM, Altera ALTPRIM, Lattice, or any vendor-specific primitives in generated SV output unless the user explicitly requests vendor-specific output. Replace them with generic synthesizable logic.
- Do not use positional associations when named parameter or port connections are possible.
- Do not emit `input var`, `output var`, or `inout var` on synthesizable module ports. Treat simulator warnings about defaulting user-defined typed inputs to `var` as a compatibility note, not as permission to add `var`; prefer plain typed ports or explicit flattening/wrappers.
- Do not clutter generated RTL with obvious comments. Use Chinese `// VHDL2SV:` comments only for high-risk migration decisions; put broader assumptions and risks in the response notes.
- **严禁行为级简化转换（STRICTLY FORBIDDEN — P0 最高优先级）**: 禁止将 VHDL 结构型 RTL 转换为行为级 SystemVerilog。每一个 VHDL process/generate/instance/signal 必须精确映射到对应的 SV 结构。具体而言：禁止用一行 `assign` 或 `$clog2` 替代多级进位链/MUX树；禁止用行为级 `<<`/`>>` 替代参数化 barrel shifter 的逐级 MUX 展开；禁止省略流水线寄存器或将多周期流水线压缩为组合逻辑；禁止将 `REGISTERS`/`flt_pt_reg_type` 参数化的可配置流水线简化为固定延迟。转换结果必须保持原始 VHDL 的：① 周期精确时序（cycle-accurate latency）② 结构等价（structural equivalence）③ 综合结果可比（comparable synthesis result）。转换后的 SV 模块必须能直接替换原始 VHDL 实例，不需要修改任何上层模块的例化代码。**例外**：供应商原语替换（Vendor Primitive Substitution）允许在保证功能等价和时序相同的前提下生成通用逻辑，详见 `references/conversion-rules.md`。This is a P0 mandatory rule — violations invalidate the conversion regardless of simulation pass/fail.
- Do not claim Efinity synthesis success, Questa simulation success, or functional equivalence unless those external checks were actually run by the user or in a separate requested workflow. Questa `vlog -sv` syntax compile success may only be reported as compile/syntax success, not simulation success.

## 杈撳嚭鏍煎紡 / Output Format

When the user asks for a file conversion, write the converted `.sv` files to disk and return:

````markdown
## Generated Files
- `<path/to/output.sv>`

## Conversion Notes
- <important semantic decisions, width/signedness/index assumptions, style choices, and non-trivial mappings>

## Manual Review Items
- <items that need human confirmation; write "None" if there are none>

## Synthesizability Checklist
- <brief pass/fail notes for process types, latches, multiple drivers, unsupported constructs, widths/signedness>

## Validation Results
- <L0 report/format check result>
- <L1 static conversion check result>
- <L2 Questa `vlog -sv` syntax compile result; write "SKIP" with the reason if Questa is unavailable or generated files are not available>
- <eval pattern check result when applicable>
- <functional simulation status; write "Not run" unless a real simulation/cosimulation was run>
````

If the user asks for inline output rather than files, return the SystemVerilog code in the response. Otherwise, prefer file output.

## 璐ㄩ噺妫€鏌ユ竻鍗?/ Final Checklist

- Every source clocked process is mapped to `always_ff` with the correct edge and reset behavior.
- Every combinational process is mapped to `always_comb` or `assign` without missing defaults or incomplete branches that infer latches.
- Every signed value remains signed in declaration or expression context.
- Every resize, sign extension, zero extension, truncation, shift, comparison, and cast has controlled width behavior.
- Every constrained VHDL integer/subtype used as RTL storage has an explicit `logic`/`logic signed` width or a specific Manual Review Item explaining why `int` was retained.
- Every VHDL `shift_left` / `shift_right` / shift operator maps to the correct SV operator or helper, with signedness, fill behavior, result width, and shift amount reviewed.
- Every `downto` / `to` range is preserved or fully remapped.
- Every array dimension is correctly represented as packed or unpacked based on element width vs array depth.
- Every dynamic-width VHDL function uses a deliberate strategy and documents any exception.
- Every high-risk generated construct has a local Chinese `// VHDL2SV:` comment and a matching Conversion Notes or Manual Review Items entry.
- Every manual-review item is specific and actionable.
- Generated SystemVerilog follows `references/code-style.md` or the target repository's established style.
- Validation Results are included and distinguish passed checks, warnings, failures, and skipped external checks.
- Questa `vlog -sv` syntax compile result is included as L2 whenever generated SV files are available; if skipped, the reason is explicit.
- Functional equivalence is not claimed unless a real simulation or cosimulation was actually run.

## 宸ュ叿涓庤剼鏈鐣?/ Tools and Scripts

Use `scripts/verify_conversion.py` for repeatable static validation of generated SV against source VHDL and optional eval expectations. The script does not run Efinity, Questa, or any synthesis/simulation flow. Questa `vlog -sv` syntax compile is a separate L2 validation step described in `references/verification-workflow.md`.

The current evaluation prompts and structured expectations live in `evals/evals.json`, with sample VHDL cases under `evals/cases/`.

## 鍙傝€冭祫鏂?/ References

The reference files are in `references/`:
- Read `references/conversion-rules.md` before doing a conversion that involves non-trivial types, arrays, records, attributes, arithmetic width changes, processes, functions, packages, or generate statements.
- Read `references/code-style.md` before writing or editing generated SystemVerilog unless the target repository already has a clearer local SV style. Follow the local style when it conflicts with this reference, and mention meaningful deviations.
- Read `references/special-conversion-strategies.md` before handling the hard cases summarized from the project reference documents: dynamic-width function strategies, `resize` / `ext` / `sxt`, unconstrained arrays, and VHDL attributes.
- Read `references/annotation-policy.md` before deciding what to comment in generated RTL and what to put in response notes.
- Read `references/verification-workflow.md` before validating generated SV or reporting conversion quality.
- Read `references/review-checklist.md` before returning final code or a migration review.
