# Conversion Verification Workflow

Use this workflow after generating SystemVerilog from VHDL. The goal is to make AI-generated RTL reviewable and catch syntax-shape, synthesizability-risk, conversion-rule, and tool syntax-acceptance mistakes before any later Questa functional simulation or Efinity synthesis work.

## Verification Levels

- **L0 Report and format check**: Confirm the response includes Generated Files, Conversion Notes, Manual Review Items, Synthesizability Checklist, and Validation Results.
- **L1 Static conversion check**: Inspect generated SV for required constructs, forbidden constructs, suspicious width/signedness patterns, process mapping, and rule-specific expectations from `evals/evals.json`.
- **L2 Questa syntax compile check**: Compile generated SV with Questa `vlog -sv` in a temporary work library. This checks syntax, package/module ordering, and tool acceptance. It is not functional simulation.
- **L3 Functional/golden check**: Reserved for later Questa `vsim` or cosimulation work. Do not claim functional equivalence from L0-L2.
- **L4 Efinity synthesis**: Reserved for later manual or separately requested Efinity project flow.

Default execution is L0-L2 when generated SV files exist. Mark L2 as `SKIP` if Questa `vlib`/`vlog` is unavailable, generated files are unavailable, or compile order cannot be determined safely. Mark L3-L4 as `Not run` unless the user separately requests those workflows and provides the project/test setup.

## Required Validation Procedure

1. Gather source VHDL files, generated SV files, optional conversion notes, and optional eval case id.
2. Run `scripts/verify_conversion.py` when files exist:

```powershell
python scripts\verify_conversion.py `
  --vhdl evals\cases\arith.vhd `
  --sv path\to\arith.sv `
  --eval-config evals\evals.json `
  --eval-id 2
```

3. If the script cannot run, manually perform L0-L1 and state the skipped command and reason.
4. Run L2 Questa syntax compile for generated SV files when `vlib` and `vlog` are available. Use dependency-aware order where possible, especially packages before modules. Use a temporary work library outside the source tree or under the workspace's temporary output area:

```powershell
vlib "$env:TEMP\vhdl2sv_work"
vlog -sv -work "$env:TEMP\vhdl2sv_work" <generated-package-files-first> <generated-module-files>
```

5. If Questa compile cannot run, report `L2: SKIP` with the exact reason, such as `vlog not found`, `no generated SV files`, or `compile order unavailable`.
6. If Questa compile fails, report `L2: FAIL` and include the first actionable compiler errors. Do not continue to claim the generated SV is tool-clean.
7. Treat warnings as review items. Treat L0/L1 failures and L2 compile failures as conversion blockers unless the user explicitly accepts the risk.
8. Include the validation summary in the final response under `Validation Results`.

## What L1 Must Check

- Generated SV contains a `module`, `package`, or both as appropriate.
- Ports use explicit direction and type where modules are generated, and synthesizable ports do not use explicit `var` port kinds such as `input var`, `output var`, or `inout var`.
- Clocked VHDL processes map to `always_ff`; combinational VHDL processes map to `always_comb` or `assign`.
- `resize`, `ext`, `sxt`, signedness changes, truncation, dynamic-width function strategies, unconstrained arrays, and VHDL attributes are documented in notes or targeted RTL comments.
- Constrained VHDL integer/subtype storage does not silently become 32-bit SV `int`; generated fixed-width `logic` declarations must document the original VHDL range/prototype, and retained `int` usage must be justified.
- VHDL `shift_left`, `shift_right`, `sll`, `srl`, `sla`, and `sra` conversions use SV shift operators or documented helper functions, with logical/arithmetic behavior and result width reviewed.
- Forbidden RTL constructs are absent unless explicitly marked as unsupported/manual review: dynamic arrays, queues, stateful classes, `initial`, `#` delays, `wait`, file I/O, and unreviewed `inout`/tri-state.
- Eval `must_have` and `must_not_have` patterns pass when an eval case is used.

## What L2 Must Check

- Generated SV files can be compiled by Questa `vlog -sv` into a clean work library.
- Package files compile before modules that import or reference them.
- Compiler errors are treated as failures and summarized under `Validation Results`.
- Compiler warnings are summarized and, when relevant, mirrored in Conversion Notes or Manual Review Items.
- Do not run `vsim`, do not execute a testbench, and do not report functional equivalence from L2.

## Reporting Rules

Use these result labels:
- `PASS`: check ran and passed.
- `WARN`: potential issue that needs review but is not a direct conversion failure.
- `FAIL`: likely conversion bug or unsupported construct.
- `SKIP`: check was intentionally not run, with a reason.

Never claim functional equivalence from L0-L2 alone. Use wording such as "static conversion checks passed and Questa syntax compile passed" unless a real Questa simulation, golden simulation, or VHDL/SV cosimulation ran.
