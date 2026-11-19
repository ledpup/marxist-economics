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
- **Does scale make it fraught?** The arithmetic doesn't. What is fraught is what the book leaves open: how far the pool reaches, and how wide the social average is. See [where the difficulty is](#where-the-difficulty-is).

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

It is not the arithmetic. The three real questions are open in the book. Each is a *finding*, as Patrick asked.

1. **How far does the pool reach?** One factor for the world means every hour worked earns the same share of the world's product, wherever it is worked. That is the GIC's principle at a larger scale. The book allows a district to differ, but only for what the district chooses: more reading rooms means a lower factor there, "a 'local tax'" ([10 h](../Documents/fundamental_principles/10_The_General_Social_Work.md#h-the-growth-process-of-communism)). It says nothing on differences nobody chose, such as an older population (more H) or a region that must replace more public means of production. If those pool, the burden is shared; if each region keeps its own factor, those differences are paid for by the people who happen to live there. *My reading:* a natural rule is a shared factor for common costs plus a local deduction for local choices, written the same way as above with S split into a pooled part and a local part.
2. **How wide is the social average?** The book says "the average of all shoe factories in the district" in one sentence and "the entire footwear industry" in the next ([8 d](../Documents/fundamental_principles/08_Average_Working_Hour_as_Basis_of_Production.md#d-the-difference-in-company-productivity)). It also says over and under-productivity "balance each other out", which is true however wide the branch is drawn. But the wider the branch, the more it shifts hours from the best-equipped units to the least equipped. This is where technology and resource differences between regions bite. They do not bite in the payout factor, which counts hours worked and does not care how much an hour produces; they show in the production times of goods, and in who is over or under the average.
3. **Resources are not counted.** The hours in a product are labour, past and present. A region rich in ore or fertile soil has goods with fewer hours in them, for the same use. The book has no place for this ([What the book leaves open](fundamental-principles-economic-model.md#what-the-book-leaves-open)). At the scale of a world it would be the largest gap.

There is also a practical one, of time. A factor needs all the reports, and at world scale they arrive at different times, with goods in transit. That is why the running factor has to be the last closed period's, and why the book's year-in-a-warehouse picture is a thought experiment and not a procedure.

## For the plans

- **Gap 7** keeps its proposal (the last closed period's factor, reconciled at the close), but the plan says it is mine and says why. The period is a scenario variable.
- **The simulation** keeps N and D as the two numbers every aggregate reports, so any level (a unit, a town, a district) can compute its factor and be combined with others exactly. Nothing is computed from factors.
- **For a later version with several towns:** a shared factor for common costs, and a local deduction for what a town chooses ([10 h](../Documents/fundamental_principles/10_The_General_Social_Work.md#h-the-growth-process-of-communism)). That is the book's own mechanism; the plans don't use it yet.
- **To investigate next:** how wide the social average should be in the model, since the book says both "district" and "entire industry".

## Sources

- GIC, *[Fundamental Principles of Communist Production and Distribution](../Documents/fundamental_principles/README.md)*, [8 d](../Documents/fundamental_principles/08_Average_Working_Hour_as_Basis_of_Production.md#d-the-difference-in-company-productivity), [10 g–i](../Documents/fundamental_principles/10_The_General_Social_Work.md#g-the-payout-factor), [13 e](../Documents/fundamental_principles/13_The_Expansion_of_Production.md#e-the-influence-on-the-payout-factor)
- ILO labour-force figures, via [Progressive Policy Institute](https://www.progressivepolicy.org/trade-fact-of-the-week-half-of-the-worlds-3-51-billion-workers-dont-have-regular-pay-or-labor-law-protections/) (a secondary summary; the ILO's own database was not checked)
- Number of businesses: [DemandSage](https://www.demandsage.com/?p=6897), [BytePlus](https://www.byteplus.com/en/topic/500841) (secondary, no stated method)
- Related notes: [The economic model of the *Fundamental Principles*](fundamental-principles-economic-model.md); [General social work and productive work](general-social-work.md)

---

[↑ Notes and research](../README.md#comparisons-and-extensions)
