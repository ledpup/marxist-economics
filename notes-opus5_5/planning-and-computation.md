[↑ Notes and research](../README.md#on-towards-a-new-socialism)

---

# Planning for final outputs: Leontief, Neumann and what computers can do now

A guide to the mathematics behind chapter 6 of *[Towards a New Socialism](../Documents/towards_a_new_socialism/06_Detailed_Planning.md)* ("Detailed Planning"): the simultaneous-equation method, the iterative methods (Jacobi, Gauss–Seidel), the book's own "harmony" algorithm, and the names it drops (Leontief, von Neumann). It asks which of these problems count as solved today, what a modern machine can do with them, and how they bear on the simulator's pull system.

This is a research note by Claude, written from a brief by Patrick. Points marked *my reading*, *my calculation* or *my measurement* are interpretation, arithmetic or my own run, not something the sources say. Sources I could not open are marked *not read*. The *Fundamental Principles* has almost nothing on planning (see [What the GIC does instead](#what-the-gic-does-instead)).

## Summary

- **The "simultaneous equation method" is Leontief's input–output model.** Given a target of final outputs *f* and a matrix of technical coefficients *A*, the gross outputs *g* that support it satisfy *g = Ag + f*, so *g = (I − A)<sup>−1</sup>f* ([note 2 of the chapter](../Documents/towards_a_new_socialism/06_Detailed_Planning.md#planning-in-the-ussr)). This is linear algebra, not optimisation. There is no objective to maximise; it finds the one point where every industry's supply matches its uses.
- **The "estimation method" in the same chapter is the iteration**, not a separate idea: guess *g*, push it through *A*, get a better *g*, repeat. Jacobi and Gauss–Seidel are the two classic ways to do it. The round-by-round result has a plain meaning: round *k* adds the requirements *k* steps up the supply chain (*my reading*: this is the Neumann series, below).
- **Optimisation does enter, but later in the chapter.** Once stocks of machines and the supply of labour limit what is possible, "which targets do we cut?" is a constrained optimisation problem. The book's harmony algorithm is a heuristic for it. Linear programming (Kantorovich, Dantzig, and von Neumann's growth model) is the standard tool for the same question.
- **The linear core is solved, and now cheaply.** *My measurement*: a Jacobi solve of 10 million products with 20 inputs each took 27 seconds on one core of an ordinary 4-core cloud machine; 1 million products with 200 inputs each took 29 seconds. The book's own estimate was half an hour on a 1 GIPS machine for 10 million × 200 × 100 rounds. Gaussian elimination, which the book rules out, is still hopeless at that size.
- **The computing was never the whole problem.** What remains open: getting the coefficients, joint production and choice of technique, time and stocks, uncertainty, lumpy plants and batches, and who sets the targets. None of these is a matter of faster machines.
- **For the simulator** (*my reading*): a pull system isn't "no planning". It is a distributed, asynchronous version of the same iteration, with stocks as the buffer. A later *plan* policy, computed with Jacobi on the recipes the model already holds, would let the two be run against each other on the shoe chain. See [What this means for the simulator](#what-this-means-for-the-simulator) and the [planning plan](../plans/simulator/planning.md).

## The problem as the book states it

| Book's term | Symbol | Meaning | In the simulator |
| --- | --- | --- | --- |
| Gross output | *g* | All of an industry's product, whatever it is used for | A unit's production per period |
| Intermediate output | *Ag* | The part used up inside the productive system | Batches shipped to other units as circulating means (c) |
| Final (net) output | *f* | The part available for consumption or net investment | What reaches the store; additions to stock |
| Technical coefficient | *a*<sub>ij</sub> | Product *i* needed directly per unit of product *j* | A line in a [recipe](../plans/simulator/shoe-scenario.md), divided by the batch size |
| Input–output table | *A* | The matrix of the above | All the recipes together |

The balance is *g = Ag + f*. The book's chapter shows the two-industry case, puts it in matrix form in a note, and says the answer is "the inverse of the Leontief matrix (*I − A*)" multiplied into *f*. The same matrix gives labour values in chapter 3: values *v* satisfy *v = vA + l*, where *l* is the direct labour per unit, so *v = l(I − A)<sup>−1</sup>* ([E6 and E7 in the model note](towards-a-new-socialism-economic-model.md#e7-computing-it-at-scale)). One computation, two uses: quantities by columns, hours by rows. (*my reading*)

The book gives the scale argument in three steps:

1. Direct solution (Gaussian elimination) is of order *n*<sup>3</sup>. Hopeless for millions of products.
2. The table is mostly zeros: toothpaste doesn't go into sausages. Store it as linked lists, not an array.
3. Use an iterative method that accepts such lists. Cost is products × average inputs × rounds: "10 million products with an average of 200 direct inputs each, and 100 iterations" is 2 × 10<sup>11</sup> operations, "a little over half an hour" at a billion instructions a second.

## The names

### Leontief

Wassily Leontief built the input–output table and its algebra in the 1930s (the book's "1930s and '40s"). The inverse (*I − A*)<sup>−1</sup> is called the Leontief inverse. Its entry (*i*, *j*) is the gross output of *i* needed, directly and indirectly, per unit of final output of *j*. The model assumes:

- one way of making each product (no choice of technique);
- one product per process (no joint production);
- fixed coefficients (no substitution as the scale changes).

These are strong, and later sections show where they bite. Leontief also had a *closed* version that treats households as one more industry: workers supply labour and consume goods. That is the loop in the shoe chain, where the shoe comes back as the worker's means of reproduction (*my reading*).

### Neumann: two different men

- **Carl Neumann (19th century) and the Neumann series.** For a matrix *A* whose powers die away, (*I − A*)<sup>−1</sup> = *I* + *A* + *A*<sup>2</sup> + *A*<sup>3</sup> + … Read as economics, *f* is final demand, *Af* is what the last stage needs, *A*<sup>2</sup>*f* is what *that* needs, and so on up the chain. The series converges when the spectral radius ρ(*A*) is below 1. [One source](https://percy-raskova.github.io/babylon/concepts/leontief-analysis.html) from the search describes the Leontief inverse this way.
- **John von Neumann (1937) and the growth model.** A model of an expanding economy with several processes, joint production, and a choice among techniques. It drops Leontief's three assumptions, and its dual side gives prices as shadow values. It was developed alongside, and independently of, Kantorovich's planning mathematics in the USSR, and is a root of linear programming ([sources on the two models](https://arxiv.org/pdf/0707.0491)). The book's "Leontief and von Neumann" points at the pair: Leontief for the plan's arithmetic, von Neumann for the question of *which processes to run*.

The chapter itself uses only the first man's ideas without naming him. That is the reason the iteration works: the Jacobi round *g*<sup>(*k*+1)</sup> = *Ag*<sup>(*k*)</sup> + *f*, started from *g*<sup>(0)</sup> = *f*, produces exactly the partial sums of the Neumann series (*my calculation*).

### Jacobi and Gauss–Seidel

Both solve a linear system by repeated sweeps.

| Method | Rule for one sweep | Good at | Bad at |
| --- | --- | --- | --- |
| **Jacobi** | Compute every new *g*<sub>i</sub> from the *previous* sweep's values | Parallel: every row is independent, so it fits many cores or a GPU | Slower: typically about twice as many sweeps as Gauss–Seidel (see the note below) |
| **Gauss–Seidel** | Compute *g*<sub>i</sub> in order, using the new values already found in this sweep | Fewer sweeps; in place, so half the memory | Order-dependent, harder to parallelise (needs colouring or blocks) |

For a Leontief system the iteration converges for any starting guess exactly when the economy is *productive*: ρ(*A*) < 1. Equivalent forms are the Hawkins–Simon conditions and "(*I − A*)<sup>−1</sup> exists and is non-negative" ([condition sources](https://arxiv.org/pdf/2401.15099)). A column sum of *A* below 1 is a convenient, sufficient test, not the exact one. Economically: each product, in its own units and at current technique, makes more than it uses up, so the system has a surplus to give to *f*. The book says convergence follows "if there is a unique solution", which is slightly loose; the precise condition is productivity.

The error shrinks by about ρ(*A*) per sweep. So the number of sweeps depends on how thin the surplus is. In my run below, with ρ ≤ 0.6, 20 to 30 sweeps reached 10<sup>−8</sup>; the book's 100 sweeps allows for ρ near 0.84. An economy with only a thin net surplus (ρ near 1) needs many more. That is a property of the economy, not of the machine (*my calculation*).

On the Jacobi / Gauss–Seidel gap: for non-negative *A* the Stein–Rosenberg theorem says that when one method converges the other does too, and Gauss–Seidel converges at least as fast. I didn't find a source for this in the search; it is standard numerical analysis from memory, so check it before relying on it.

**Asynchronous version.** Chazan and Miranker's "chaotic relaxation" (1969) showed that these iterations converge even when rows update in any order, using stale values, provided ρ(|*M*|) < 1 ([search summary](https://core.ac.uk/download/4380768.pdf)). For a Leontief system this holds when ρ(*A*) < 1 (*my reading*). Each industry's computer can recompute its own gross output whenever it receives news of its customers' needs, with no global clock. This is the bridge to the pull system below.

## Is the estimate a mathematical optimisation?

Three different things are in the chapter, and only the last two are optimisation.

| Problem | Where | What kind of problem | Status |
| --- | --- | --- | --- |
| Gross outputs for given final targets | "Planning in the USSR" and before | Solving *n* linear equations (a fixed point) | Solved, at any size, by iteration |
| Do stocks of machines and labour allow it? | "Detail planning and stock constraints" | A feasibility check: compute each industry's needs from *g* and the per-unit coefficients, sum them, compare with stocks | Easy once *g* is known |
| If not, which targets give way, and by how much? | "A new plan-balancing algorithm" | Constrained optimisation: maximise a social satisfaction measure subject to resource limits | Heuristic in the book; standard tools exist |

**The harmony algorithm.** Cockshott's own method (the book cites Cockshott 1990) maximises the total of a "harmony" function over industries, subject to resource limits. The function is zero at target, negative below, and positive but flattening above it ([figure 6.4](../Documents/towards_a_new_socialism/figures/figure-6-4.png)). That is a utility function with diminishing returns. The nine steps are a relaxation heuristic: repeatedly take resources from the industries with above-average harmony and give them to the ones below, with a bias *B* that starts high and falls to stop it settling in a poor local optimum. The book claims it is roughly linear in the size of the problem (*n* industries × *m* inputs each), tested on about 4,000 industries in 300 seconds on a Sun workstation, and extrapolated to 10 million products.

Two observations (*my reading*):

- The formula in the text (*u* = (output − goal)/goal; harmony = −*u*<sup>2</sup> for *u* < 0, √*u* otherwise) doesn't match the figure. The formula's slope at the target is 0 from below and unbounded from above, so it is *flatter* on the shortage side, with a kink at the target; the figure (smooth, steep below) and the prose ("rapidly negative" for shortfalls) have it steeper. I haven't altered the source text. The function matters because the whole method is shaped by where the curve bends.
- The standard alternative is linear programming: maximise a weighted sum of final outputs (or pick the proportional scale-up of the target list) subject to *(I − A)g ≥ f* and the stock and labour limits. The dual variables of that LP are shadow prices, which is von Neumann's and Kantorovich's insight. A [search result](https://www.dcs.gla.ac.uk/~wpc/reports/plan_with_AIT.html) (*not read*) reports that Cockshott's later paper compares the harmony algorithm with the LP package lp-solve, finding harmony much cheaper on highly disaggregated plans. That is the author's own comparison; I haven't checked it.

So the chapter's answer to your question is: the first method is not optimisation; the second is, and it chooses a different solution method (heuristic relaxation) from the one an economist would first reach for (LP) mainly on grounds of cost at huge scale.

## Is it still considered solved?

The honest answer is "which part?".

### What is solved

- **The linear input–output solve.** Nobody disputes that *g = Ag + f* can be solved for tables of any size anyone can build. National statistical offices do it routinely on tables of a few hundred industries, and the sparse-iteration route the book describes is ordinary numerical practice. The book's critics (Nove's "twelve million discrete items") are answered on the arithmetic alone.
- **Large linear programs.** The first-order method PDLP, and its GPU versions (cuPDLP), solve LPs with billions of non-zero coefficients, which barrier solvers cannot fit in memory ([PDLP paper](https://arxiv.org/html/2501.07018): test set of 125 million to 6.3 billion non-zeros). So the constrained version, with stocks and labour, is also within reach at the size of the book's economy, *if* it is a linear program.
- **Distributed and asynchronous solving.** [Multi-GPU PDLP](https://arxiv.org/html/2601.07628) and asynchronous Jacobi are active research. A search result reports that communication can erase the speedup from adding GPUs, which is the same point the book makes about telecommunications.

### What is not, and isn't a computing problem

1. **The data.** The matrix *A* must be written down: tens of millions of coefficients, kept current. The book says as much ("a prodigious amount of detailed information must be gathered") and returns to it in [chapter 9](../Documents/towards_a_new_socialism/09_Planning_and_Information.md). The [2023 paper by Dapprich and Cockshott](https://econpapers.repec.org/RePEc:eee:jeborg:v:205:y:2023:i:c:p:412-422) argues the information can be gathered, answering Hayek, and offers both labour values and LP shadow prices as valuations. I haven't read it; the point at issue is whether the reported coefficients are honest and how fast they go stale.
2. **Joint production and choice of technique.** Leontief assumes neither. With them the problem is an LP over *processes*, not a system of linear equations, and the solution can change discontinuously. Joint products are also a question for the GIC's accounting (the simulator already chose the [by-product method](../plans/simulator/accounting.md#joint-products-the-by-product-method)).
3. **Time.** The static model ignores how long things take. Stocks, lead times and construction of capital need a *dynamic* model with a matrix of capital coefficients. Dynamic Leontief models are known to be unstable, producing negative or oscillating outputs unless handled carefully (from memory; *unverified* here). The book's own point is that stock constraints matter more the shorter the plan period.
4. **Uncertainty.** Plans are made against forecasts. Breakdowns, weather and demand surprises call for a feedback loop, which is why the book has [chapter 4's](../Documents/towards_a_new_socialism/04_Basic_Concepts_of_Planning.md) feedback control and chapter 8's marketing algorithm.
5. **Lumpiness.** Plants come in whole units and batches in whole crates. Rounding a linear solution to whole units is an integer problem; those are much harder in general (NP-hard), though in practice good heuristics exist.
6. **Where the targets come from.** *f* is an input. The book's answer is strategic planning, votes on the main budget shares, and the marketing feedback of chapter 8; none of that is mathematical.

(*my reading*) The usual summary among economists would be: the calculation objection of Mises and the 1930s debate has largely been dissolved by computing; the knowledge, incentive and dynamics objections have not. The book says the same when it says computerisation "is no panacea".

## What a modern machine can do

I ran the book's calculation. Setup: random sparse productive matrix, each row with *k* non-zero entries in random columns, scaled so no row sums above 0.6; Jacobi sweeps *g* ← *Ag* + *f* until the largest relative change was below 10<sup>−8</sup>; SciPy sparse matrix, one thread, 15 GB RAM, 4 cores.

| Products *n* | Inputs each *k* | Non-zeros | Sweeps | Time | Per sweep |
| --- | --- | --- | --- | --- | --- |
| 100,000 | 200 | 20 million | 27 | 0.8 s | 0.03 s |
| 1,000,000 | 200 | 200 million | 27 | 29 s | 1.1 s |
| 10,000,000 | 20 | 200 million | 19 | 27 s | 1.4 s |

Dense Gaussian elimination (LAPACK, 4 cores): 2.8 s for *n* = 8,000. At the *n*<sup>3</sup> rate that is about 64 days for a million products, and the dense matrix alone (10<sup>12</sup> entries) is 8 TB (*my calculation*, by extrapolation). The book's "30 years" for a million products, by the way, is its own slip: 10<sup>18</sup> steps at 10<sup>10</sup> a second is 3 years ([the model note](towards-a-new-socialism-economic-model.md#e7-computing-it-at-scale)). Whichever figure one takes, direct solution is still out.

Extrapolation to the book's full size, 10 million products × 200 inputs (2 billion non-zeros), 100 sweeps (*my calculation*, not measured):

| Machine | Cost per sweep | 100 sweeps |
| --- | --- | --- |
| One core, as measured (about 190 million non-zeros a second) | about 11 s | about 18 minutes |
| A server with 100 GB/s memory bandwidth: 2 billion × 12 bytes ≈ 24 GB a sweep, if bandwidth-bound | about 0.25 s | about 25 s |
| A GPU with 2 to 3 TB/s memory bandwidth, if the matrix (24 GB at double precision, 16 GB with single-precision coefficients) fits in its memory | about 10 ms | a few seconds |

The surprising thing is the first row. One core now is only about twice as fast as the book's idealised 1 GIPS machine, because sparse iteration is limited by memory access, not arithmetic. The real gains since 1993 come from **memory capacity** (the whole table in RAM) and **parallelism** (many cores, GPUs), not from clock speed. The table's bandwidth rows assume the sweep achieves close to peak bandwidth, which random access seldom does; take them as the right order of magnitude, not a prediction.

For the harmony algorithm I haven't the code, so I can't measure it. Its 1990 benchmark (4,000 industries, 300 seconds on a 3 MIPS workstation) is now trivial: modern cores are at least a thousand times faster, putting it well under a second. The extrapolation to 10 million products at roughly linear cost then lands somewhere between minutes and an hour on one core, and less with parallelism (*my estimate*, flagged as such because the real constant depends on the program).

**Beyond the book.** Large stocks of real-world product data exist already inside firms such as Walmart and Amazon, and the planning-from-inside-capitalism argument (Phillips and Rozworski's *The People's Republic of Walmart*, and Cockshott's own writing) leans on that. I haven't checked the details here and so don't rely on it.

## What the GIC does instead

The *Fundamental Principles* has no planning in this sense. Its coordination is by accounting: each unit books what it takes from the community and what it hands back, at the social average hours per branch, and the "over" or "under" shows whether it is slower or faster than its branch ([the model note](fundamental-principles-economic-model.md#what-the-book-leaves-open)). What gets made is settled by the units' own orders and by the workers' councils; the book doesn't say how a shortage or surplus is dealt with. The GIC's production equation (f + c) + l is the *value* side of the Leontief model (the row-vector *v = vA + l*, where *A* includes wear on the durable goods), but the GIC computes it by adding up what actually flowed, not by solving it in advance. (*my reading*)

## What this means for the simulator

The simulation is [a pull system](../plans/simulator/simulation-engine.md#demand-and-orders): the store holds a target stock and reorders, and each unit does the same for its inputs. (*my reading*) It would be wrong to treat this as the alternative to planning.

- **The pull system is also an iteration.** An order from the store reaches the shoe factory, which orders leather and soles, which order from the tannery and the sole works, which order electricity. Each tick passes the requirement one step up the chain, which is the Neumann series *f*, *Af*, *A*<sup>2</sup>*f* … carried out in real time, with every unit as one row of the matrix. Loops (electricity needs coal, coal-mining needs electricity; the shoe feeds the worker) are settled by the stocks that sit between units, not by solving them at once. It is the asynchronous, stale-information case of the previous section; Chazan and Miranker say it converges.
- **What differs is when, and from what.** Pull reacts to sales that have already happened and to stocks that have run down, with lead times. It overshoots and undershoots when a chain is long (the "bullwhip effect" known from supply-chain studies). A plan computes the requirement for a whole period beforehand from a target, and can look at capacity and labour limits before anything is made. It also needs the targets and the coefficients, which pull doesn't.
- **A tie to the accounts.** The books' result for each product (hours accumulated through the chain) must equal the Leontief value *v = l(I − A)<sup>−1</sup>* computed straight from the recipes. That gives the [testing plan](../plans/simulator/testing.md) an independent check for the book's 125,000 hours for 40,000 pairs, besides the invariants it already has. For the shoe chain, *A* is a few lines and can be solved exactly.
- **A "plan" policy as a later experiment.** The engine's stub already lists it: "*Later:* a production plan from the congress of workers' councils, as an alternative policy". Concretely: build *A* and *l* from the recipes, take a target of final goods (say the store's expected weekly sales), solve for gross outputs by Jacobi, and issue production orders per period. Run the same seeded world under pull, plan and a mix, and compare stock-outs, idle time, stock held, and hours per pair. The [planning plan](../plans/simulator/planning.md) sets this out.

Neither the GIC nor the simulator's brief needs central planning; the point of keeping the plan as a policy is to find out what pull does badly, and whether a computed plan would fix it, before deciding. That fits Patrick's wish not to dismiss the approach.

## Questions to keep

- Which targets would a congress of workers' councils set, and how would they reach the plan? The book assumes votes on budget shares and market feedback; the GIC says nothing.
- How would the coefficients be kept honest in a system where each unit reports its own? ([chapter 9](../Documents/towards_a_new_socialism/09_Planning_and_Information.md) discusses techniques; the simulator's later "dishonesty" feature touches the same thing.)
- Does the harmony function's shape matter to the result? The formula and the figure disagree; test both in a simulation, or look for the authors' later statement of the function.
- At what plan period do stock constraints bind? The book says the shorter the period, the more they matter.

## Sources

Read in full: the repository's chapter 6 and the existing model notes. Cited from search results only, *not read in full*: the [PDLP paper](https://arxiv.org/html/2501.07018) and its [multi-GPU follow-up](https://arxiv.org/html/2601.07628); [condition for a unique positive solution](https://arxiv.org/pdf/2401.15099); the [Leontief-inverse overview](https://percy-raskova.github.io/babylon/concepts/leontief-analysis.html); [Kantorovich and linear programming](https://arxiv.org/pdf/0707.0491); [asynchronous matrix iterations](https://core.ac.uk/download/4380768.pdf); Dapprich and Cockshott, "[Input-output planning and information](https://econpapers.repec.org/RePEc:eee:jeborg:v:205:y:2023:i:c:p:412-422)" (*Journal of Economic Behavior & Organization*, 2023); Cockshott's [application of AI techniques to economic planning](https://www.dcs.gla.ac.uk/~wpc/reports/plan_with_AIT.html). Several other recent arXiv titles turned up (on centralised and polycentric computational planning, and networked input–output problems) but arxiv.org was not reachable from this session, so I haven't read them. The timings are from my own run; the code was a short SciPy script and is not kept in the repository.

---

[↑ Notes and research](../README.md#on-towards-a-new-socialism)
