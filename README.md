<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/nilaymastaadmi/nilaymastaadmi/main/assets/banner-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/nilaymastaadmi/nilaymastaadmi/main/assets/banner-light.svg">
  <img alt="Nilay Toshniwal. ECE final year, BITS Goa. RTL design and verification, and LLM agents I measure rather than demo. An animated timing diagram: a 100 MHz aclk domain crossing into an unrelated 27 MHz cclk domain through a gray-coded async FIFO. 11,495 crossings, 0 scoreboard mismatches, 1,266,540 assertion checks, 18 of 18 bins covered."
       src="https://raw.githubusercontent.com/nilaymastaadmi/nilaymastaadmi/main/assets/banner-light.svg" width="100%">
</picture>

Two lines of work: RTL design and verification, and LLM agents that ship with the
evaluation harness attached. The common thread is that every repository below states a
number and hands you a way to check it yourself.

The banner is not decoration: it is the design in
[axi-cdc-uvm](https://github.com/nilaymastaadmi/axi-cdc-uvm), drawn on one time axis, so
the two traces really are in a 100:27 period ratio.

---

## Silicon

**[axi-cdc-uvm](https://github.com/nilaymastaadmi/axi-cdc-uvm)** &middot; SystemVerilog, UVM, SVA

An AXI4-Lite slave whose write payloads cross into an unrelated clock domain through a
Gray-coded asynchronous FIFO, verified against a scoreboard rather than by inspection.

100 constrained-random seeds, 100 MHz against 27 MHz so edges drift through every phase
relationship instead of settling into a pattern:

| | |
|---|---:|
| transactions crossed the domain | 11,495 |
| scoreboard mismatches | 0 |
| protocol and CDC assertion checks | 1,266,540 |
| assertion failures | 0 |
| functional coverage, union across seeds | 18/18 = 100% |

The UVM environment and the bound SVA properties were also run on Cadence Xcelium
25.03-s001 with UVM 1.2, all three tests clean. Reproduce with `make test && make regress`.

---

## Agents, with the evaluation attached

**[market-query-agent](https://github.com/nilaymastaadmi/market-query-agent)**

A tool-using LLM agent that answers analytical questions about Indian equity data by
writing and executing SQL, plus the harness that measures how well it actually works.
Wiring up tool calls is easy. Almost nobody reports task success rate, cost per task, and
a taxonomy of how it fails.

93.8% on 48 graded questions. 40/40 on answerable tiers, 5/8 on unanswerable.
$0.0160 mean cost per task, 1.9 mean tool calls, 100% SQL citation rate.

The most useful output is the failure taxonomy, hand-labelled from episode logs. A shallow
automated classifier disagreed with the hand label on 3 of 3 failures, which is the
argument for hand-labelling stated as a measurement instead of an assertion.

**[jaw2026-trust-reliability](https://github.com/nilaymastaadmi/jaw2026-trust-reliability)**

333 natural-language questions over 687 unstructured documents, with no supplied database,
schema, or document-to-entity mapping. The organisers withheld the database, so the system
rebuilds it (41 tables, 9,973 rows) and then answers by executing deterministic queries.

Scores 100.000 on the official evaluation set.

**[alpaca-hackathon](https://github.com/nilaymastaadmi/alpaca-hackathon)**

An options agent that refuses to trade. It measures whether volatility is actually
expensive before selling it, and declines when it is not. On its first live run it
refused, because implied volatility was 12.81 against a trailing realised 13.28.

Every decision it makes, including every refusal, is a signed artifact you can verify
yourself with `make verify`.

**[pcb-drishti-pro](https://github.com/nilaymastaadmi/pcb-drishti-pro)**

PCB defect detection with a rupee-cost RELEASE / REWORK / SCRAP decision layer, built for
the QC supervisor at a small high-mix assembly shop. The model learns defect classes
rather than board templates, so a new board design needs zero inspection programming.

0.717 held-out-board mAP@0.5 on board designs the model never trained on, and roughly 97%
fewer false positives on out-of-domain photos. Served live, and testable in 30 seconds
from the README.

Seven approaches were tried. Five lost, and the write-ups for the ones that lost are in
the repository next to the two that shipped.

---

## Tools

`SystemVerilog` `UVM` `SVA` `Verilog` `Yosys` `SKY130` `ngspice` `Python` `C++` `Git` `Linux`

Most of the analog and RISC-V work is in private repositories. Happy to walk through any
of it.
