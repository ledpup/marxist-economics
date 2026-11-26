[↑ Plans](README.md)

---

# Planning

*Stub.* How a plan for final outputs could sit beside the simulation's [pull system](simulation-engine.md#demand-and-orders), so the two can be compared. The mathematics, the names (Leontief, von Neumann, Jacobi, Gauss–Seidel) and what modern machines can do are in [Planning for final outputs](../../notes-opus5_5/planning-and-computation.md). The source is chapter 6 of *[Towards a New Socialism](../../Documents/towards_a_new_socialism/06_Detailed_Planning.md)*. The *Fundamental Principles* does not deal with planning.

## Why keep it

The brief's model is pull: the store reorders, and each unit reorders from its suppliers. That is not "no planning". It is a distributed version of the same iteration (each order passes the requirement one step up the chain), with stocks as buffers. A computed plan is the centralised alternative. The aim is to find out what pull does badly, and whether a plan would fix it, before deciding either way.

## Policies as drop-in modules

Each approach is one **policy module**. The scenario names the policy to use (`policy: "pull"`), and changing that one line changes how every unit decides what to make. Nothing else in the model or the books changes, so the same seeded world can be run under each and the results compared.

| Module | How a unit decides what to make | Needs | Source | Status |
| --- | --- | --- | --- | --- |
| **`pull`** | Reorders when stock falls below target; orders pass up the chain | Recipes, target stocks, lead times | [Engine](simulation-engine.md#demand-and-orders), the brief | The default, first |
| **`plan-io`** | Solves *g = Ag + f* by Jacobi or Gauss–Seidel for the period's final targets, then checks machine and labour limits and cuts the lowest-priority targets if they are broken | *A*, *l*, targets *f*, priorities, capacities | *TNS* ch. 6 | Later |
| **`plan-lp`** | Linear program: maximise a weighted sum of final outputs subject to *(I − A)g ≥ f* and the capacity and labour limits. Also yields shadow prices | As `plan-io`, plus weights; a LP solver | Kantorovich, von Neumann; Dapprich and Cockshott 2023 (*not read*) | Later |
| **`plan-harmony`** | Cockshott's relaxation heuristic: move resources from industries with above-average harmony to those below, with a falling bias | As `plan-io`, plus a harmony function | *TNS* ch. 6; Cockshott 1990 (*not read*) | Later |
| *Mixed* | A plan sets a base amount and pull adjusts to what actually sells. Not a fifth algorithm: a plan module and `pull` composed | Both | | If the others suggest it |

### The shape of a module

- **One interface.** A policy is given a read-only view of the world (stocks, recipes, capacities, the crew available, recent sales, the clock) and returns **production orders** and **stock targets** per unit. It never writes to the state. The engine applies the orders in the "Demand and orders" step and everything downstream (production, logistics, accounting) runs as before.
- **Two ways to be called:** every tick (pull reorders as stock falls) or once per planning period (the plans, say weekly). The module says which.
- **Deterministic.** A policy draws any random numbers from the engine's one generator ([determinism](simulation-engine.md#random-numbers-and-determinism)), so a run with a given seed and policy repeats exactly.
- **Solvers are separate from policies.** A linear solver (Jacobi, Gauss–Seidel, an exact solve) and an LP solver are libraries. `plan-io` and `plan-harmony` use the first kind or their own loop; `plan-lp` uses the second. The same linear solver also computes the values used by the [accounting check](#experiments).
- **Same measures for all.** The engine records the same comparison figures whatever the policy: stock-outs, stock held, idle crew and machine hours, hours per pair, orders placed per tick (to see swings up the chain).

## What the plan needs from the model

- **A matrix of technical coefficients *A*** and a **labour vector *l***, both derived from the [recipes](shoe-scenario.md): input per unit of output, direct hours per unit. Wear on machines and buildings is a coefficient too (the book counts "numbers worn out" per year).
- **A target of final outputs *f*:** to begin with, the store's expected sales per period. Where targets come from in a real plan is open ([questions](../../notes-opus5_5/planning-and-computation.md#questions-to-keep)).
- **A solver:** Jacobi iteration, *g* ← *Ag* + *f*, until the change is small. For the shoe chain, *A* is a few rows, so it can also be solved exactly; the exact answer is the test of the iteration.
- **Constraints**, checked after the solve: machine capacity, and labour supply. If they are broken, cut the lowest-priority targets and solve again.
- **Orders** issued per period from the gross outputs, in place of the reorder rule.

## Experiments

1. **Values from the recipes.** Compute *v* = *l*(*I* − *A*)<sup>−1</sup> and check it against the hours the books accumulate for each product, including the book's 125,000 hours for 40,000 pairs. Add to the [testing plan](testing.md).
2. **Each policy against the others** on the same seeded world: stock-outs, stock held, idle crew and machine time, hours per pair.
3. **Shocks:** a machine breaks, a shipment is late, demand jumps. How long before each policy recovers?
4. **Lead times along the chain.** Whether pull's orders swing more the further they go up the chain.

## Open questions

- Who sets the plan in a world run by workers' councils ([Workers' democracy](workers-democracy.md))? The *Towards a New Socialism* answer is a central planning body under votes and juries; the GIC gives none.
- Where do the coefficients come from in the simulation: the recipes (exact) or each unit's reports (which can be wrong, once [dishonesty](simulation-engine.md) is in)?
- How are crates of 20 and whole machines handled, since a plan's linear answer will not come out in whole crates?
- Is the harmony function ([chapter 6](../../Documents/towards_a_new_socialism/06_Detailed_Planning.md#the-harmony-function)) worth building, or is a plain Jacobi solve plus cuts enough for the shoe chain?

---

[↑ Plans](README.md)

## To fetch when back at a PC

The cloud session can't reach some sites (arxiv.org, Cockshott's Glasgow page, bactra.org). These are the sources the [note](../../notes-opus5_5/planning-and-computation.md) marks *not read*. Saving them as PDFs in `PDFs/` and reading them would settle the points in brackets.

Fetched on 26 November 2026, except where noted. Saved but not yet read.

- Cockshott, "Application of Artificial Intelligence Techniques to Economic Planning" (`dcs.gla.ac.uk/~wpc/reports/plan_with_AIT.html`): the harmony algorithm in full [what `plan-harmony` should do exactly; the shape of the harmony function]. This is the same paper as Cockshott (1990), cited in chapter 6 (*Future Computing Systems* 2, 1990): its title matches and nothing in its references is later than 1989. It does not contain the comparison with lp-solve, which must be in a later paper. Saved: [PDF](../../PDFs/APPLICATION%20OF%20ARTIFICIAL%20INTELLIGENCE%20TECHNIQUES%20TO%20ECONOMIC%20PLANNING.pdf).
- Dapprich and Cockshott (2023), "Input-output planning and information", *J. Economic Behavior & Organization* 205, doi:10.1016/j.jebo.2022.10.043 [the LP and shadow-price version; `plan-lp`]. **Not fetched:** the publisher's copy is paywalled, and the Westminster repository refuses automated requests. Check it in a browser. Dapprich's [PhD thesis](https://theses.gla.ac.uk/81793/8/2020DapprichPhD.pdf) (Glasgow, 2020) is free and covers related ground.
- arXiv 2005.01539 ("Open Loop In Natura Economic Planning"), 2606.19214 ("Testing Centralized and Polycentric Computational Planning") and 2412.13564 ("The networked input-output economic problem") [recent tests of these methods, and of planning without a single centre]. Saved: [Open loop](../../PDFs/OPEN%20LOOP%20IN%20NATURA%20ECONOMIC%20PLANNING.pdf), [Centralized and polycentric](../../PDFs/TESTING%20CENTRALIZED%20AND%20POLYCENTRIC%20COMPUTATIONAL%20PLANNING.pdf), [Networked](../../PDFs/THE%20NETWORKED%20INPUT-OUTPUT%20ECONOMIC%20PROBLEM.pdf).
- Shalizi, "In Soviet Union, Optimization Problem Solves You" (`bactra.org/weblog/918.html`, 2012) [the sceptical case on scale]. Saved: [PDF](../../PDFs/IN%20SOVIET%20UNION%2C%20OPTIMIZATION%20PROBLEM%20SOLVES%20YOU.pdf).
- Chapter 8 (the marketing algorithm), already in this repository [where the targets *f* could come from].
