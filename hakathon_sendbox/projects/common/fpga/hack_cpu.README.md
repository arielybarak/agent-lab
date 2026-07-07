# hack_cpu + mem_arbiter — deferred (extract on demand)

The nand2tetris **Hack CPU** is large and only useful for a specific
"build/run a CPU" challenge, and it needs **generated ROM/RAM IP** (program ROM
from a `.mif`, data RAM), so a raw `.sv` here wouldn't run on its own. We've
built the reusable core — **`alu.sv`** (the Hack ALU, with a passing testbench).
The full CPU is documented for fast extraction if a matching challenge appears.

## If you need it, extract these from the `de10lite-board-and-build` skill

- **`hack_cpu.sv`** — skill section "Hack CPU": 16-bit CPU, dual-cycle
  (Fetch/Execute), registers A(16)/D(16)/PC(14). Wire it to `alu.sv`.
- **`mem_arbiter.sv`** — section "Memory Space Arbiter": address decode
  0x0000–3FFF RAM, 0x4000–5FFF text screen, 0x6000–0x6001 I/O.
- **`cpu_rom` / `cpu_ram`** — Quartus IP (1-port ROM with `.mif`, data RAM).
  Generate in the IP Catalog; add the `.qip` to the project `.qsf`.

Assemble your Hack program to a `.mif`, point `cpu_rom` at it, recompile. Full
integration steps are in the skill ("Hack CPU → Integration", "ALU Operations",
"MIF-Based ROM Programming").
