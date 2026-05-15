# Special Conversion Strategies

Use this reference for hard VHDL constructs that cannot be translated by syntax replacement. These rules summarize the project reference documents and expand the second and third dynamic-width function methods.

## H-001 Dynamic-Width Functions

Treat a VHDL function as dynamic-width when any argument, return value, local object, assignment target, or attribute depends on call-site width, an unconstrained vector, `a'length`, `a'range`, object bounds, or a width parameter.

Default preference:
1. Parameterized `virtual class` + `static function automatic`.
2. Module-local parameterized function or logic.
3. Fixed-width package specializations.

Remember the semantic distinction:
- VHDL `constant` values inside a function are elaboration-time or locally computed values.
- VHDL `signal` inputs to a function are runtime hardware values; the SV function call becomes either compile-time computation or runtime combinational hardware depending on its inputs.

### Method 2: Module-Local Parameterized Function

Use this when the function is only used inside one module, or when a group of functions share the same module format parameters.

Best fit:
- The function is declared inside one VHDL architecture.
- The function depends on module generics such as width, lane count, exponent width, mantissa width, or pipeline format.
- External modules do not need to import or call the function.
- The target tool/style allows parameterized modules but avoids parameterized classes.

Conversion workflow:
1. Identify every dynamic width used by the VHDL function.
2. Promote those widths to module `parameter` or `localparam`.
3. Rewrite the function as a local `function automatic` with explicit argument and return dimensions.
4. Keep runtime logic pure combinational; use `always_comb` or `assign` at call sites.
5. If a function body is clearer as explicit logic and has only one call site, inline it into `always_comb` with explicit defaults.
6. Add a conversion note that the function is now module-local and no longer reusable outside the module.

Pattern:
```systemverilog
module calc #(
  parameter int unsigned IN_W = 8,
  parameter int unsigned OUT_W = 16
) (
  input  logic [IN_W-1:0]  a,
  output logic [OUT_W-1:0] y
);
  function automatic logic [OUT_W-1:0] zext_local(input logic [IN_W-1:0] value);
    logic [OUT_W-1:0] r;

    r = '0;
    r[IN_W-1:0] = value;
    return r;
  endfunction

  assign y = zext_local(a);
endmodule
```

Rules:
- Do not refer to package-level width constants when the width actually belongs to a module instance.
- Do not keep the function in a package if the replacement depends on instance-specific parameters.
- Guard invalid combinations such as `OUT_W < IN_W` with a note, assertion, or explicit truncation rule.
- Use this method for local reuse within a module; choose Method 3 if the function must remain a public package utility.

Manual review items:
- List any previous external callers that can no longer call the function.
- State whether truncation is intentional when output width is smaller than input width.
- State whether the target tool supports local `function automatic` with parameterized packed dimensions.

### Method 3: Fixed-Width Package Specializations

Use this when the function belongs in a package, the target style avoids parameterized classes, and actual call widths are few and stable.

Best fit:
- The VHDL function is a shared package function.
- The call graph uses fixed and known width pairs.
- Conservative synthesis compatibility matters more than generic reuse.
- Reviewers prefer explicit width-specific functions.

Conversion workflow:
1. Build a call-site inventory: function name, input widths, output width, signedness, and array depth if relevant.
2. Group calls by identical width/signature tuple.
3. Generate one `function automatic` per tuple in the SV package.
4. Name each specialization deterministically, using source and target widths.
5. Rewrite every call site to the matching specialization.
6. Add a manual-review item for any possible VHDL call width that has no generated specialization.

Pattern:
```systemverilog
package conv_pkg;
  function automatic logic [15:0] zext8_to16(input logic [7:0] value);
    return {8'b0, value};
  endfunction

  function automatic logic [31:0] zext16_to32(input logic [15:0] value);
    return {16'b0, value};
  endfunction

  function automatic logic signed [15:0] sxt8_to16(input logic [7:0] value);
    return {{8{value[7]}}, value};
  endfunction
endpackage
```

Rules:
- Do not pretend the specialized package still supports arbitrary widths.
- Do not create a large open-ended matrix of functions unless the user asks for it.
- Do not use overloaded-looking names that hide width changes. Encode width and signedness in names when needed.
- Keep extension/truncation explicit inside each specialization.
- Import the generated package at call sites and update calls by name.

Manual review items:
- List covered specializations, for example `zext8_to16`, `zext16_to32`.
- List uncovered or inferred width combinations.
- Note that future new widths require adding another function.

## H-002 `resize`, `ext`, and `sxt`

Prefer direct explicit zero/sign extension or truncation. Use `$signed` / `$unsigned` only when the target width is proven and the shorthand remains readable.

Rules:
- Convert `resize(unsigned(a), N)` and `ext(a, N)` as zero-extension when `N` is wider than the source.
- Convert `resize(signed(a), N)` and `sxt(a, N)` as sign-extension when `N` is wider than the source.
- Convert to low-bit truncation when `N` is narrower than the source, and add a risk note.
- Treat `$signed` and `$unsigned` as interpretation controls, not complete resize operations.

Patterns:
```systemverilog
assign yu = {{(OUT_W-IN_W){1'b0}}, a};
assign ys = {{(OUT_W-IN_W){b[IN_W-1]}}, b};
assign yt = a[OUT_W-1:0];
```

Use direct concatenation when the extension amount is known or parameterized cleanly. Use `$signed(a)` / `$unsigned(a)` only when the left-hand side width exactly supplies the target width and the expression is simple.

## H-003 Range-Unconstrained Arrays

Do not map RTL unconstrained arrays to SV dynamic arrays. Preserve the VHDL type idea with `typedef`, then apply concrete bounds at each object declaration.

VHDL pattern:
```vhdl
type byte_arr_t is array(natural range <>) of std_logic_vector(7 downto 0);
signal data : byte_arr_t(0 to DEPTH-1);
```

SV pattern:
```systemverilog
typedef logic [7:0] byte_t;
byte_t data [0:DEPTH-1];
```

Rules:
- Preserve the category/name of the VHDL type when it improves readability.
- Define the element type separately when the array bound is object-specific.
- Use module parameters for bounds derived from generics.
- Add a manual-review item when no object-level range or parameterized bound can be found.
- For array ports, choose unpacked array ports or flattened buses based on project/tool interface rules.

## H-004 VHDL Attributes

Do not mechanically replace VHDL attributes. First identify whether the target object is a packed vector, unpacked array, element type, or index range.

Rules:
- Map packed vector bit width to `$bits(a)` or a named parameter.
- Map unpacked array depth to `$size(a)` or a named parameter.
- Map element width to `$bits(a[index])` or an element-width parameter.
- Map `'left`, `'right`, `'high`, and `'low` to explicit index constants or SV query functions only when the declaration direction is preserved.
- Map `'range` loops to explicit loop bounds, preserving direction when it affects behavior.

Prefer explicit `localparam` names when the width or index is central to the converted RTL:
```systemverilog
localparam int unsigned DATA_W = $bits(data);
localparam int unsigned DEPTH = $size(mem);
```

Manual review items:
- State when a VHDL direction was normalized.
- State when an attribute was replaced by an explicit constant.
- State when an attribute refers to an array depth rather than a vector width.
