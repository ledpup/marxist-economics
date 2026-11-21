[↑ Notes and research](../README.md#comparisons-and-extensions)

---

# The payout factor at the scale of a world

Patrick asked whether the GIC's payout factor (FIC) can be worked out for a large economy, or the whole world, and whether combining regional results loses information. This note works through it. It is a research note by Claude, written from a brief by Patrick. Points marked *my reading* or *my calculation* are interpretation or arithmetic, not something the book says. Figures marked *estimate* are rough.

## Patrick's prompt

> Number 7: payout factor. Is it accurate to say this equation is the most involved? You said it is done every year. What made you decide that? The book shows two forms, one with productive units and then one with mixed units added. And there is the new variable H. How does this function work in a large economy? We need all the hours for all the operational units, productive, public, mixed? Does it get calculated for a region? Wouldn't that be fraught as some regions have more technology and resources? Does it then need to be done for the whole world? Can that work? There are 8 billion people on the planet. How many are working? 4 billion? Estimate how many operational units we'd have at that scale. Can the equation be calculated at the regional level and then be combined between regions? Does that work mathematically or have we made it nonsense by losing information?

## Short answers

- **Is it the most involved equation?** No. It is a ratio of two sums. The production equation and the social average are no harder. It is the most *far-reaching*: every other figure in the model depends only on a unit's own inputs or its branch, while the payout factor depends on the whole economy at once.
- **Why every year?** The book did not decide that, and nor should I have implied it. The year comes from the book's thought experiment ("all goods produced in one year are brought together in one large warehouse"), which it then calls a simplification: "in reality, it does not take place after a year, but at every minute of the day" ([10 g](../Documents/fundamental_principles/10_The_General_Social_Work.md#g-the-payout-factor)). The period for a running factor (the last closed period's, reconciled at each close) is my proposal for [gap 7](../plans/simulator/gaps-in-the-brief.md#the-economics), not the book's.
- **Can it be done at scale, and can regions be combined?** Yes, exactly. The factor is a sum over units divided by a sum over units. Sums can be taken region by region and added, with no loss, provided each region reports its two sums and not its factor. See [combining regions](#combining-regions).
- **Does scale make it fraught?** The arithmetic doesn't. What the book leaves open is how far the pool reaches, and who bears costs nobody chose. See [where the difficulty is](#where-the-difficulty-is).

## The forms

The book has three forms, not two. I merged them in the [accounting plan](../plans/simulator/accounting.md#the-payout-factor).

| Form | Equation | Where |
| --- | --- | --- |
| Productive and public units | FIC = (L − (F<sub>p</sub> + C<sub>p</sub>)) / (L + L<sub>p</sub>) | [10 g](../Documents/fundamental_principles/10_The_General_Social_Work.md#g-the-payout-factor), [E7](fundamental-principles-economic-model.md#e7-the-payout-factor-fic) |
| With mixed units | FIC = (L − {(F<sub>p</sub> + C<sub>p</sub>) − (F'<sub>p</sub> + C'<sub>p</sub>)}) / (L + L<sub>p</sub>) | [10 i](../Documents/fundamental_principles/10_The_General_Social_Work.md#i-mixed-operational-units), [E8](fundamental-principles-economic-model.md#e8-the-payout-factor-with-mixed-units) |
| With expansion | FIC = (L − (F<sub>p</sub> + C<sub>p</sub>) − a(F<sub>t</sub> + C<sub>t</sub>)) / (L + L<sub>p</sub>) | [13 e](../Documents/fundamental_principles/13_The_Expansion_of_Production.md#e-the-influence-on-the-payout-factor), [E10](fundamental-principles-economic-model.md#e10-the-payout-factor-with-expansion) |

The H term is mine, not the book's: the hours credited to people who don't work ([gap 9](../plans/simulator/gaps-decided.md#the-economics)). It goes in the bottom line only.

*My reading.* Write S for everything taken off the top (the public units' means of production, net of what mixed units charge to other units, plus expansion), and D for the bottom line, L + L<sub>p</sub> + H. Then:

- **N = L − S** is the product left for individual consumption.
- **D = L + L<sub>p</sub> + H** is all hours that claim a share of it.
- **FIC = N ÷ D**, and the share held back is 1 − FIC = (S + L<sub>p</sub> + H) ÷ D.

This is all the equation is. Every form above, and any further deduction (a disaster fund, special accumulation), only adds a term to S.

## What a large economy needs

Not "all the hours for all the units" as detail. Five totals are enough:

1. L, hours worked in productive units.
2. L<sub>p</sub>, hours worked in public units.
3. H, hours credited to those who don't work.
4. The public units' means of production, F<sub>p</sub> + C<sub>p</sub>, less what mixed units charge to other units.
5. Expansion and the other funds.

Everything else cancels. The productive units take back their own F + C by construction ([E6](fundamental-principles-economic-model.md#e6-the-productive-units-budget)), so they appear only through their hours. No quantities, prices or product counts enter. Each unit reports a handful of numbers a period; the central office, or any office, adds them. The book's own picture is "a simple summation in the Giro Office".

## How big the world is

*Estimates.* The ILO's 2024 figures, as summarised by the [Progressive Policy Institute](https://www.progressivepolicy.org/trade-fact-of-the-week-half-of-the-worlds-3-51-billion-workers-dont-have-regular-pay-or-labor-law-protections/), are a labour force of about 3.7 billion, with about 3.5 billion employed, out of about 8 billion people. So **about 3.5 billion people work**, a little under your 4 billion. About 58 % of them are in informal work, much of it farming and small trade, which the GIC treat "with the greatest restraint" ([17 d](../Documents/fundamental_principles/17_Final_Considerations.md#d-utopism)).

The number of operational units depends on what counts as a unit: a plant or enterprise with its own books. Counts of businesses worldwide run from about 350 to 500 million, mostly micro-enterprises, from secondary sources with no stated method ([DemandSage](https://www.demandsage.com/?p=6897), [BytePlus](https://www.byteplus.com/en/topic/500841)). From memory, the US has about 8 million establishments with employees, for about 130 million employed: *about 16 each* (not checked against the Census Bureau's [County Business Patterns](https://www.census.gov/programs-surveys/cbp/about.html)).

| Average workers per unit | Units for 3.5 billion workers |
| --- | --- |
| 20 (the US establishment, and below) | about 175 million |
| 100 | about 35 million |
| 1,000 (large plants, with the GIC's consolidation) | about 3.5 million |

My guess is **tens of millions**, 30 to 100 million, with public units (schools, clinics, child care, water, power) a few percent of them. The size of the data is not a problem: 100 million units reporting five numbers each, as 8-byte values, is about 4 GB a period. A world total is a tree of sums (unit, town, region, continent, world), five or six levels deep, and sums of this kind can be taken in any order.

## Combining regions

For regions r = 1…R, each region reports N<sub>r</sub> and D<sub>r</sub>, with N = ΣN<sub>r</sub> and D = ΣD<sub>r</sub>. Then

FIC = ΣN<sub>r</sub> ÷ ΣD<sub>r</sub> = Σ (D<sub>r</sub> ÷ D) × FIC<sub>r</sub>

That is exact. The world factor is the **weighted average of the regional factors, weighted by each region's bottom line** (its hours claiming a share). Nothing is lost if the two sums are passed up. Something *is* lost if only the regional factors are passed up, because the weights are gone.

Example (*invented*):

| Region | N (million hours) | D (million hours) | FIC |
| --- | --- | --- | --- |
| A | 542 | 650 | 0.834 |
| B | 300 | 500 | 0.600 |
| **World** | **842** | **1,150** | **0.732** |

The simple average of 0.834 and 0.600 is 0.717, which is wrong. The weighted average is 0.732, which is right. The same holds for a world, a region, and a town: the town's factor is the weighted average of its units'.

Two properties follow. A factor computed at any level is consistent with the one above it, and the claims always equal the product: FIC × D = N at every level, so nothing is "created" or "lost" by aggregating.

## Where the difficulty is

It is not the arithmetic. Two things are not the payout factor's business at all, and one is open.

**Not open: the width of the social average.** I first listed this as an open question, because 8 d says "the average of all shoe factories in the district" in one sentence. That was a misreading. The social average is **per product, across the whole industry** that makes it: "calculated over the entire social shoe production", "the average of the entire footwear industry" ([8 d](../Documents/fundamental_principles/08_Average_Working_Hour_as_Basis_of_Production.md#d-the-difference-in-company-productivity)). It has to be, because it is Kautsky's "socially necessary work": any narrower slice would give the same shoe two production times. "District" is a loose word in a sentence whose neighbours say otherwise; it is the only use of it in the chapters on the average. The book even names location among the reasons units differ ("one company has a better location than another"), so geography is already inside the average, as one more cause of over- and under-productivity. Regions with more technology or resources are therefore not a second problem: their units are simply above the average, and their hours balance those below it.

**Not the payout factor's concern either.** The payout factor is not an average over an industry. It is one sum over all hours worked in the pool, and one over all the claims on it. Geography enters only through the "local tax", where a district chooses its own public units ([10 h](../Documents/fundamental_principles/10_The_General_Social_Work.md#h-the-growth-process-of-communism)). The two are different aggregations: **the social average runs across a product's units, and the payout factor runs across everything in one accounting system.**

**What is open: the reach of the accounting system.** Both aggregations run over whatever sits inside one set of books: one giro office. A world with one set of books has a world average and a world factor. If instead there are several systems, each has its own averages and its own factor, and goods that cross between them need a conversion, which is exactly the problem of the outside, and the key number is the GIC's only answer to it ([17 b](../Documents/fundamental_principles/17_Final_Considerations.md#b-from-the-money-account-to-the-working-time-account)). The book never says how far its giro office reaches. For the simulation this is already settled: the town is one system, the gate is the boundary ([gap 5](../plans/simulator/gaps-decided.md#the-economics)).

**Two further points, neither a gap for the simulation:**

- **Differences nobody chose.** The book allows a district's factor to differ for what it chooses. It says nothing on an older population (more H), or a region needing more public means of production. *My reading:* a shared factor for common costs plus a local deduction for local choices, as S split into a pooled and a local part.
- **Resources are not counted.** The hours in a product are labour, past and present. A region with rich ore or soil has goods with fewer hours in them for the same use. The book has no place for this ([What the book leaves open](fundamental-principles-economic-model.md#what-the-book-leaves-open)), and, like greenhouse gases ([gap 50](../plans/simulator/gaps-decided.md#the-economics)), it is out of scope for the simulation. It is a finding about the book.

A practical one, of time: a factor needs all the reports, and at scale they arrive at different times. That is why the running factor has to be the last closed period's.

## For the plans

- **Gap 7** keeps its proposal (the last closed period's factor, reconciled at the close). The period is a scenario variable.
- **The simulation** keeps N and D as the two numbers every aggregate reports, so any level can compute its factor and be combined with others exactly. Nothing is computed from factors.
- **The social average** is per product across every unit in the model that makes it, however many towns there are. Nothing to decide.
- **For a later version with several towns:** a shared factor for common costs, and a local deduction for what a town chooses (10 h). That is the book's own mechanism; the plans don't use it yet.

## Sources

- GIC, *[Fundamental Principles of Communist Production and Distribution](../Documents/fundamental_principles/README.md)*, [8 d](../Documents/fundamental_principles/08_Average_Working_Hour_as_Basis_of_Production.md#d-the-difference-in-company-productivity), [10 g–i](../Documents/fundamental_principles/10_The_General_Social_Work.md#g-the-payout-factor), [13 e](../Documents/fundamental_principles/13_The_Expansion_of_Production.md#e-the-influence-on-the-payout-factor)
- ILO labour-force figures, via [Progressive Policy Institute](https://www.progressivepolicy.org/trade-fact-of-the-week-half-of-the-worlds-3-51-billion-workers-dont-have-regular-pay-or-labor-law-protections/) (a secondary summary; the ILO's own database was not checked)
- Number of businesses: [DemandSage](https://www.demandsage.com/?p=6897), [BytePlus](https://www.byteplus.com/en/topic/500841) (secondary, no stated method)
- Related notes: [The economic model of the *Fundamental Principles*](fundamental-principles-economic-model.md); [General social work and productive work](general-social-work.md)

---

[↑ Notes and research](../README.md#comparisons-and-extensions)
