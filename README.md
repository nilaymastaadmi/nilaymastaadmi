### Hi, I'm Nilay

ECE final year at BITS Goa.

**I like building.**

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/nilaymastaadmi/nilaymastaadmi/main/assets/snake-dark.svg?v=3">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/nilaymastaadmi/nilaymastaadmi/main/assets/snake-light.svg?v=3">
  <img alt="A snake game playing itself, looping continuously." src="https://raw.githubusercontent.com/nilaymastaadmi/nilaymastaadmi/main/assets/snake-light.svg?v=3" width="100%">
</picture>

---

## Silicon

**[axi-cdc-uvm](https://github.com/nilaymastaadmi/axi-cdc-uvm)** &nbsp;`SystemVerilog` `UVM` `SVA`
An AXI4-Lite slave whose writes cross into an unrelated 27 MHz domain through a gray-coded
FIFO. 100 seeds, 11,495 crossings, zero mismatches, 18/18 coverage. Runs clean on Cadence
Xcelium too.

**[rv32-dsp-soc](https://github.com/nilaymastaadmi/rv32-dsp-soc)** &nbsp;`Verilog` `RISC-V`
An RV32I core with a GPS correlator hung off the bus. The hardware search runs 5.63x faster
than the software one, and both return the same answer on the same noisy samples. Checked
instruction by instruction against a C++ simulator, not by staring at waveforms.

**[analog-pmic-sky130](https://github.com/nilaymastaadmi/analog-pmic-sky130)** &nbsp;`SKY130` `ngspice`
A two-stage OTA and the LDO built around it. 76 dB gain, 81 degrees phase margin, passing
across all 15 PVT corners plus a 300-sample Monte Carlo.

**[gmid-char-sky130](https://github.com/nilaymastaadmi/gmid-char-sky130)** &nbsp;`SKY130` `ngspice`
Sweeps the devices so transistor widths come out of a lookup instead of out of guessing.
This is where the sizing data above comes from.

**nebula-slacksmith** &nbsp;`private until 15 Sept`
RTL optimisation that changes pipeline latency and writes its own proof obligation. Most
tools will not touch latency, because proving equivalence across a timing change is the
hard part.

## Agents

**[market-query-agent](https://github.com/nilaymastaadmi/market-query-agent)** &nbsp;`Python`
Answers questions about Indian equity data by writing SQL. 93.8% over 48 questions. Three
failed. I labelled all three by hand, and the automatic classifier got all three wrong.

**[alpaca-hackathon](https://github.com/nilaymastaadmi/alpaca-hackathon)** &nbsp;`Python`
Sells option premium, but only when volatility is actually expensive. On its first live run
it refused: implied 12.81 against realised 13.28. Every call it makes is signed, so you can
check the log is the log.

**[jaw2026-trust-reliability](https://github.com/nilaymastaadmi/jaw2026-trust-reliability)** &nbsp;`Python`
333 questions over 687 documents, with no database supplied. It builds one, then answers
from it. 100.000 on the official set.

## Vision

**[pcb-drishti-pro](https://github.com/nilaymastaadmi/pcb-drishti-pro)** &nbsp;`Python` `YOLO`
Finds PCB defects and prices them, so the output is SCRAP or RELEASE instead of a box on an
image. 0.717 mAP on board designs it never trained on. Still served: one curl returns live
detections.

**heart-murmur-index** &nbsp;`private`
3,163 heart-sound spectrograms, indexed and manifested so the dataset rebuilds without
shipping the images around.

---

`SystemVerilog` &nbsp;`UVM` &nbsp;`SVA` &nbsp;`Verilog` &nbsp;`Yosys` &nbsp;`SKY130` &nbsp;`ngspice` &nbsp;`Python` &nbsp;`C++` &nbsp;`PyTorch` &nbsp;`Linux`
