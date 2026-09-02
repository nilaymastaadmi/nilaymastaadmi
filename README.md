### hi, i'm Nilay

**i like building.** ECE final year at BITS Goa. Most of what is below started as a
question I could not answer by reading, so I built the thing and measured it instead.

Every project here states a number and hands you a way to check it yourself.

<!--SNAKE:START-->
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/nilaymastaadmi/nilaymastaadmi/main/assets/snake-dark.svg?v=1">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/nilaymastaadmi/nilaymastaadmi/main/assets/snake-light.svg?v=1">
  <img alt="A shared snake game board, 21 by 11. Score 0, high score 0, 1 moves played." src="https://raw.githubusercontent.com/nilaymastaadmi/nilaymastaadmi/main/assets/snake-light.svg?v=1" width="100%">
</picture>

<div align="center">

|  |  |  |
|:--:|:--:|:--:|
|  | [**&uarr; up**](https://github.com/nilaymastaadmi/nilaymastaadmi/issues/new?title=snake:up&body=Submit+this+issue+and+the+bot+moves+the+shared+snake+one+square%2C+then+closes+the+issue.+Nothing+else+happens.+You+can+edit+the+title+to+up/down/left/right+before+submitting.) |  |
| [**&larr; left**](https://github.com/nilaymastaadmi/nilaymastaadmi/issues/new?title=snake:left&body=Submit+this+issue+and+the+bot+moves+the+shared+snake+one+square%2C+then+closes+the+issue.+Nothing+else+happens.+You+can+edit+the+title+to+up/down/left/right+before+submitting.) | *one click, one square* | [**right &rarr;**](https://github.com/nilaymastaadmi/nilaymastaadmi/issues/new?title=snake:right&body=Submit+this+issue+and+the+bot+moves+the+shared+snake+one+square%2C+then+closes+the+issue.+Nothing+else+happens.+You+can+edit+the+title+to+up/down/left/right+before+submitting.) |
|  | [**&darr; down**](https://github.com/nilaymastaadmi/nilaymastaadmi/issues/new?title=snake:down&body=Submit+this+issue+and+the+bot+moves+the+shared+snake+one+square%2C+then+closes+the+issue.+Nothing+else+happens.+You+can+edit+the+title+to+up/down/left/right+before+submitting.) |  |

</div>

**Last moves:** [@nilaymastaadmi](https://github.com/nilaymastaadmi) up
<!--SNAKE:END-->

<sub>There is one snake and everyone shares it. Clicking an arrow opens a pre-filled
issue; submitting it runs a GitHub Action that moves the snake one square, redraws the
board, and closes the issue. No account of mine, no third-party service, about 300 lines
in [`game/`](game/). Walking it into a wall is allowed and will be recorded under your
name forever.</sub>

---

## What I've built

### Silicon

Things that end up on a chip.

- **[axi-cdc-uvm](https://github.com/nilaymastaadmi/axi-cdc-uvm)** `SystemVerilog` `UVM` `SVA`
  An AXI4-Lite slave whose writes cross into an unrelated clock domain through a
  gray-coded async FIFO. 100 seeds at 100 MHz against 27 MHz: 11,495 crossings, 0
  scoreboard mismatches, 1,266,540 assertion checks, 18/18 functional coverage. The UVM
  environment and the bound SVA also run clean on Cadence Xcelium 25.03 under UVM 1.2.
- **nebula-slacksmith** `private` `Verilog`
  Latency-changing RTL optimisation that emits its own proof obligations, so a
  transformation has to justify itself rather than be trusted.
- **rv32-dsp-soc** `private` `Verilog`
  A RISC-V RV32 core with DSP extensions, synthesised and timed.
- **analog-pmic-sky130** `private` `SKY130`
  Two-stage Miller-compensated OTA and an LDO regulator: gm/Id sizing, 15-corner PVT
  characterisation, Monte Carlo offset, measured loop stability.
- **gmid-char-sky130** `private` `SKY130`
  A gm/Id framework that sizes transistors from measured device data instead of guesswork.

### Agents

LLM systems, plus the harness that grades them. The harness is the part I care about.

- **[market-query-agent](https://github.com/nilaymastaadmi/market-query-agent)** `Python`
  An agent that answers questions about Indian equity data by writing SQL. 93.8% on 48
  graded questions, 40/40 on the answerable tiers, $0.0160 per task, 100% SQL citation
  rate. The failure taxonomy is hand-labelled, and a shallow automated classifier
  disagreed with the hand label on 3 of 3 failures. That disagreement is the result.
- **[alpaca-hackathon](https://github.com/nilaymastaadmi/alpaca-hackathon)** `Python`
  An options agent that refuses to trade. It checks whether volatility is actually
  expensive before selling it, and on its first live run it declined: implied 12.81
  against trailing realised 13.28. Every decision, refusals included, is a signed
  artifact you can verify with `make verify`.
- **[jaw2026-trust-reliability](https://github.com/nilaymastaadmi/jaw2026-trust-reliability)** `Python`
  333 questions over 687 documents with no database, schema, or entity mapping supplied.
  It rebuilds the withheld database (41 tables, 9,973 rows) and answers deterministically.
  Scores 100.000 on the official evaluation set.

### Seeing and hearing

Models pointed at images and audio.

- **[pcb-drishti-pro](https://github.com/nilaymastaadmi/pcb-drishti-pro)** `Python` `YOLO`
  PCB defect detection with a rupee-cost RELEASE / REWORK / SCRAP layer on top, so the
  output is a decision rather than a bounding box. 0.717 held-out-board mAP@0.5 on board
  designs it never trained on, and about 97% fewer false positives on out-of-domain
  photos. The model is still served: one `curl` from the README returns real detections.
- **heart-murmur-index** `private` `Python`
  A 3,163-image spectrogram dataset of phonocardiograms, indexed and manifested so the
  structure is reproducible even though the images stay local.

### Deciding

Work whose deliverable is a decision, and the reasoning that has to survive someone
attacking it.

- **[sih2026-handoff](https://github.com/nilaymastaadmi/sih2026-handoff)** `research`
  The full decision package behind one competition entry: a 30-problem sweep, a
  competitor model, prior-art kill tests, and an adversarial audit that tried to overturn
  the pick and could not. Written so a stranger can reconstruct the reasoning from zero.

---

### Tools

`SystemVerilog` `UVM` `SVA` `Verilog` `Yosys` `SKY130` `ngspice` `Python` `C++` `PyTorch` `Git` `Linux`

Several projects above are private because they are coursework-adjacent or still running.
Happy to walk through any of them.
