# SystemVerilog Code Style

Use this style when generated SystemVerilog is not being inserted into a repository with an existing, stronger local style. Preserve local project conventions when they are clear.

## Formatting

- Use two spaces for indentation and no tabs.
- Keep one declaration per line when dimensions, signedness, or initialization are present.
- Preserve VHDL entity port order and generic order unless the user requests cleanup.
- Use ANSI-style module headers with explicit direction, type, and packed dimensions on every port.
- Do not write explicit `var` port kinds (`input var`, `output var`, `inout var`) for synthesizable RTL. Although legal SystemVerilog, this is not portable enough for the target synthesis/mixed-language flow; use plain typed ports or flatten/wrap complex record-like interfaces.
- Use blank lines between parameter blocks, port declarations, internal declarations, continuous assignments, and procedural blocks.
- Prefer named end labels for packages, modules, classes, generate blocks, and longer functions when they improve readability.

## Naming

- Preserve source identifiers by default to keep waveform and review correlation simple.
- Rename only for SV legality, project conventions, or clear conflict avoidance; document non-trivial renames.
- Use `_pkg` suffix for generated package filenames and package names only when it avoids ambiguity.
- Use `_q` and `_d` suffixes only when introducing an explicit register/next-state split.

## Types and Declarations

- Use `logic` for 4-state RTL signals and ports; use `bit` only for explicitly 2-state VHDL or user-requested 2-state style.
- Type parameters explicitly, for example `parameter int unsigned WIDTH = 8`.
- Use `localparam` for derived constants and include explicit widths when the value becomes hardware.
- For constrained VHDL integers/subtypes that become RTL storage, array elements, record/struct fields, ports, counters, or pipeline state, use explicit fixed-width `logic` / `logic signed` typedefs instead of SV `int`. Keep `int` for parameters, loop variables, and temporary calculations where 32-bit semantics are intentional.
- Put packed dimensions next to the type and unpacked dimensions next to the identifier: `logic [7:0] mem [0:DEPTH-1];`.
- Do not introduce SV dynamic arrays, queues, classes with state, or unsynthesizable constructs for RTL migration.
- Do not add global compiler directives such as ``default_nettype none`` unless the target project already uses them or the user requests them.

## Expressions

- Use sized literals for fixed values: `8'hFF`, `3'b001`, `1'b0`.
- Use `'0` and `'1` for all-zero/all-one assignments only when the target type and width are already explicit.
- Avoid unsized arithmetic constants in width-sensitive logic. Prefer sized literals, typed parameters, or casts with explicit dimensions.
- Use `$bits`, `$size`, or explicit parameters for VHDL attributes only after determining whether the object is a packed vector, unpacked array, or element type.
- Treat `$signed`, `$unsigned`, and casts as interpretation controls, not as resize replacements.
- Convert VHDL shift functions/operators to SV shift operators with explicit signedness when needed. Use `<<` / `>>` for logical shifts and `$signed(x) >>> n` or a signed expression for arithmetic right shifts. Document non-trivial shift conversions with a local Chinese `// VHDL2SV:` comment.

## Procedural RTL

- Use `always_ff` for clocked registers and nonblocking assignments for registered state.
- Use `always_comb` for combinational processes and blocking assignments for local combinational values.
- Initialize combinational outputs and next-state variables at the top of `always_comb` blocks when branch coverage is not otherwise complete.
- Preserve reset polarity, reset synchronicity, and reset value exactly. Do not convert declaration initialization into reset behavior unless the source or project convention proves that intent.
- Use plain `case` by default. Use `unique case`, `priority case`, or synthesis pragmas only when source semantics and project style justify them.

## Packages, Functions, and Classes

- Place typedefs and parameters before functions that depend on them.
- Merge VHDL package declarations and package bodies into one SV package when that is clearer.
- Keep functions `automatic` unless a specific tool or project convention requires otherwise.
- Do not generate SV `task` for synthesizable RTL by default. Convert VHDL procedures to `function automatic`, `function automatic void`, packed struct returns, or inline logic.
- For dynamic-width VHDL functions, prefer the parameterized `virtual class` plus `static function automatic` strategy from `conversion-rules.md`.
- Keep utility classes stateless and pure combinational; use them as namespaces, not as hardware objects.

## Instantiation and Integration

- Use named parameter overrides and named port connections.
- Preserve instance names when legal.
- Convert VHDL `open` associations only after checking port direction and module contract.
- Emit package imports close to the scope that needs them, following local style if available.

## Comments and Notes

- Keep generated RTL comments sparse. Use Chinese `// VHDL2SV:` comments for migration-sensitive code required by `annotation-policy.md`, not for obvious translations.
- Include original VHDL prototypes/ranges in local comments for constrained integer typedefs or declarations that were narrowed to fixed-width `logic`.
- Put semantic risks, tool assumptions, and project-style exceptions in the response's Conversion Notes or Manual Review Items.
- When style and source semantics conflict, preserve source semantics first and document the style exception.
- Follow `annotation-policy.md` for required notes and targeted RTL comments.
