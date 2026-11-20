[↑ Plans](README.md)

---

# Planning

*Stub.* How a plan for final outputs could sit beside the simulation's [pull system](simulation-engine.md#demand-and-orders), so the two can be compared. The mathematics, the names (Leontief, von Neumann, Jacobi, Gauss–Seidel) and what modern machines can do are in [Planning for final outputs](../../notes-opus5_5/planning-and-computation.md). The source is chapter 6 of *[Towards a New Socialism](../../Documents/towards_a_new_socialism/06_Detailed_Planning.md)*. The *Fundamental Principles* does not deal with planning.

## Why keep it

The brief's model is pull: the store reorders, and each unit reorders from its suppliers. That is not "no planning". It is a distributed version of the same iteration (each order passes the requirement one step up the chain), with stocks as buffers. A computed plan is the centralised alternative. The aim is to find out what pull does badly, and whether a plan would fix it, before deciding either way.

## Policies

| Policy | How a unit decides what to make | Status |
| --- | --- | --- |
| **Pull** | Reorders when stock falls below target | The default ([engine](simulation-engine.md#demand-and-orders)) |
| **Plan** | Produces what the period's plan says | Later |
| **Mixed** | Plan sets a base amount; pull adjusts for what actually sells | Later, if the other two suggest it |

## What the plan needs from the model

- **A matrix of technical coefficients *A*** and a **labour vector *l***, both derived from the [recipes](shoe-scenario.md): input per unit of output, direct hours per unit. Wear on machines and buildings is a coefficient too (the book counts "numbers worn out" per year).
- **A target of final outputs *f*:** to begin with, the store's expected sales per period. Where targets come from in a real plan is open ([questions](../../notes-opus5_5/planning-and-computation.md#questions-to-keep)).
- **A solver:** Jacobi iteration, *g* ← *Ag* + *f*, until the change is small. For the shoe chain, *A* is a few rows, so it can also be solved exactly; the exact answer is the test of the iteration.
- **Constraints**, checked after the solve: machine capacity, and labour supply. If they are broken, cut the lowest-priority targets and solve again.
- **Orders** issued per period from the gross outputs, in place of the reorder rule.

## Experiments

1. **Values from the recipes.** Compute *v* = *l*(*I* − *A*)<sup>−1</sup> and check it against the hours the books accumulate for each product, including the book's 125,000 hours for 40,000 pairs. Add to the [testing plan](testing.md).
2. **Pull against plan** on the same seeded world: stock-outs, stock held, idle crew and machine time, hours per pair.
3. **Shocks:** a machine breaks, a shipment is late, demand jumps. How long before each policy recovers?
4. **Lead times along the chain.** Whether pull's orders swing more the further they go up the chain.

## Open questions

- Who sets the plan in a world run by workers' councils ([Workers' democracy](workers-democracy.md))? The *Towards a New Socialism* answer is a central planning body under votes and juries; the GIC gives none.
- Where do the coefficients come from in the simulation: the recipes (exact) or each unit's reports (which can be wrong, once [dishonesty](simulation-engine.md) is in)?
- How are crates of 20 and whole machines handled, since a plan's linear answer will not come out in whole crates?
- Is the harmony function ([chapter 6](../../Documents/towards_a_new_socialism/06_Detailed_Planning.md#the-harmony-function)) worth building, or is a plain Jacobi solve plus cuts enough for the shoe chain?

---

[↑ Plans](README.md)
