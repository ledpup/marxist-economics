[↑ Plans](README.md)

---

# Accounting

The books are the point of the simulation: they are where the hours accumulate. This plan turns the book's equations ([The equations](../../notes-opus5_5/fundamental-principles-economic-model.md#the-equations)) into rules the [simulation engine](simulation-engine.md) applies. Records are defined in the [data model](data-model.md#the-books).

## Numbers

- Hours are held as **integer micro-hours** (millionths of an hour). In JavaScript, integers are exact up to about 9 × 10<sup>15</sup>, which holds the book's whole economy (1,408 million hours, [E2](../../notes-opus5_5/fundamental-principles-economic-model.md#e2-the-whole-economy)) with room to spare. Past that, 64-bit integers.
- Divisions (a social average, wear per hour, a payout factor) round to the nearest micro-hour. The remainder is carried to the next entry, so totals balance exactly.
- The screen rounds to two decimals: 3.18 hours.

## A unit's books

Every unit, productive or public, keeps (f + c) + l ([E1](../../notes-opus5_5/fundamental-principles-economic-model.md#e1-the-production-equation-one-unit)), in the book's own words:

| Entry | What goes in |
| --- | --- |
| **Withdrawn from the community** | c: input batches received, at the production time they were passed on at, plus freight on them. f: wear on its machines and buildings |
| **Hours worked** | l: from the work log |
| **Transferred to the community** | Its output, at the branch's social average |
| **Over or under** | Transferred minus (f + c + l). Not a profit or loss: a signal that the unit is faster or slower than its branch ([11 d](../../Documents/fundamental_principles/11_Accounting_as_Summary_of_Production_and_Distribution.md#d-transformation-of-terms-no-gain-no-loss78)) |

## The production time of a batch

When a function finishes a batch, the new batch's hours are, from the point of view of the unit that made it:

- **c**: the hours of every input batch used, in full (whatever f/c/l split they had upstream becomes c here), plus electricity and freight.
- **f**: wear on the machines used, for the minutes used, plus a share of the building's wear.
- **l**: the crew's minutes on the batch. A slower crew takes more minutes on the hand work, so its batches carry more hours, and the unit shows "under" against its branch. Each worker is still credited one hour for each hour worked.

Time not spent on any one batch (setting up, cleaning, the designer's work, idle time) is pooled for the period and spread over the period's output in proportion to labour minutes. This is the "shared overheads" problem in the [shoe chain note](../../notes-opus5_5/fundamental-principles-economic-model.md#what-the-fuller-chain-brings-out); the rule used should be shown in the unit's books.

Separately from f/c/l, a batch can keep its **sources**: its hours broken down by the branch they originated in (leather, rubber, electricity …). This is for display only. The GIC's point is that no unit *needs* this history ([8 c](../../Documents/fundamental_principles/08_Average_Working_Hour_as_Basis_of_Production.md#c-the-progress)).

## Direct transfers

When a batch moves from one unit to another, a **direct transfer** is recorded: the sender's "transferred to the community", the receiver's "withdrawn from the community", at the same number of hours. Nothing circulates and nothing can be spent; it is a record, not a payment.

A freight leg is a second transfer: the transport unit passes on its service (its f, c and l for the leg) to the receiving unit, which adds it to c. Freight is never free ([10 i](../../Documents/fundamental_principles/10_The_General_Social_Work.md#i-mixed-operational-units)).

Moving goods inside one building, between its functions, is not a transfer.

## The social average

For each branch and period: Σ (f + c + l) over its units ÷ Σ units of product ([E3](../../notes-opus5_5/fundamental-principles-economic-model.md#e3-the-social-average-production-time)).

- During a period, goods pass on at a **provisional** average: the last period's, or the product's initial figure on day one.
- At the period's close, the actual average is computed, with each unit's over or under. Across the branch they sum to zero.
- The difference between provisional and actual, over the goods already passed on, is recorded as a branch adjustment and shown. *To decide:* whether it is carried into the next period's provisional figure or charged back to the receivers.

With one shoe factory, the average is that factory's figure. The phase 5 scenario has three, as in the book.

## Labour certificates

- Each person's hours are totalled weekly from the work log. Certificates issued = hours worked × payout factor, credited to the household's account.
- The skill level never changes this ([gap 10](gaps-in-the-brief.md#decided)).
- **Child carers and students** from age 12 are paid as public work ([gap 8](gaps-in-the-brief.md#decided)). Their hours are part of L<sub>p</sub>. Carers' hours, at the centre or at home, are recorded by the child care unit, within its budget; students' hours by the school. Child care uses few means of production (the centre's building and supplies; almost none at home), so it adds to the bottom line of the payout factor and hardly at all to the top. Both are [policies](data-model.md#scenario-and-policies) and can be switched off to compare.
- **People who don't work** are credited hours without working ([gap 9](gaps-in-the-brief.md#decided)): a retired person 20 hours a week (retirement is a choice from 65), as a top-up to their hours worked of at most 32 in all, the ill and injured their usual hours until they are fit. Certificates issued = hours credited × payout factor, as for hours worked. Credited hours (H) are not labour, so they are in neither L nor L<sub>p</sub>, but they claim a share of the product, so they go in the bottom line of the payout factor. Each group is a [policy](data-model.md#scenario-and-policies) and can be switched off to compare. Children are provided for by child care and school, and consume out of their household's certificates, with nothing extra per child (the GIC's "great injustice", accepted).
- Certificates are spent at the consumer cooperative's store on goods at their production time, including the store's own share ([Downstream](../../notes-opus5_5/fundamental-principles-economic-model.md#downstream-from-the-factory-to-the-worker)). Spent certificates are cancelled: they do not circulate (Marx's "theatre ticket").
- A purchase takes the goods' hours out of the books as **individual consumption**. They are not added to the next product the worker makes: l is hours worked, not hours consumed ([gap 3](gaps-in-the-brief.md#decided)). The screen shows the loop from shoe to worker to work; the books show the shoe's hours ending at the store.

## The payout factor

The general form, combining [E7](../../notes-opus5_5/fundamental-principles-economic-model.md#e7-the-payout-factor-fic), [E8](../../notes-opus5_5/fundamental-principles-economic-model.md#e8-the-payout-factor-with-mixed-units) and [E10](../../notes-opus5_5/fundamental-principles-economic-model.md#e10-the-payout-factor-with-expansion):

FIC = (L − {(F<sub>p</sub> + C<sub>p</sub>) − (F'<sub>p</sub> + C'<sub>p</sub>)} − a(F<sub>t</sub> + C<sub>t</sub>)) / (L + L<sub>p</sub> + H)

H is the hours credited to people who don't work ([gap 9](gaps-in-the-brief.md#decided)). It is not in the book's formula; it is Marx's "funds for those unable to work", which the GIC never mentions. With H = 0 the formula is the book's.

- Phase 1: the school and the child care unit are public units, and the retired and the ill are credited hours, so the factor is below 1 from the start. There is no expansion (a = 0).
- Phase 5: a clinic.
- The factor in use during a period is the last period's (policy `previousPeriod`), or a fixed value. At the close, the actual factor is computed and the difference shown. The book does not say how this is done.
- Expansion (a), special accumulation and the disaster fund keep their place in the formula but are zero until a later phase ([gap 19](gaps-in-the-brief.md#decided)).

## The mixed unit

The power station meters each consumer ([E8](../../notes-opus5_5/fundamental-principles-economic-model.md#e8-the-payout-factor-with-mixed-units)):

- To units: a direct transfer at production time per kWh.
- To households: free. The f + c of that share counts as public, in F<sub>p</sub> + C<sub>p</sub> less F'<sub>p</sub> + C'<sub>p</sub>, and lowers the payout factor.

## Wear and tear (f)

- **Machines:** productionHours ÷ lifeHours per hour of use, charged to the batch the machine was used on.
- **Buildings:** productionHours ÷ (lifeYears × working days a year) per day, charged to the unit's pooled time for the period.
- **Vehicles:** per hour driven, charged to the freight leg.
- When a machine reaches its life, it is worn out and must be replaced. In phase 1 a replacement arrives from the rest of the economy.

## Joint products: the by-product method

The brief chooses the by-product method ([Joint products](../../notes-opus5_5/fundamental-principles-economic-model.md#joint-products-meat-milk-and-hides)).

- A function's outputs are marked `main` or `byProduct`.
- **All** the function's hours (inputs, wear, labour) go to the main product.
- A by-product carries only the hours of the functions applied to it *after* the split-off point (collecting, salting, baling, carrying).
- In the shoe chain:
  - **Hides** come from the slaughterhouse, outside the chain at first, so the method is applied through the hides' arrival figure: post-split-off hours only. See [Shoe scenario](shoe-scenario.md#two-versions).
  - **Leather offcuts** from cutting are a by-product. They go to the rest of the economy (for leatherboard), carrying only the hours of collecting and baling them.
  - **Flash** from sole moulding is a by-product that is ground and fed back into moulding: a loop inside one unit, carrying only the grinding hours.
- Each unit's books state that the by-product method was used, so the record shows where production time is measured and where it is agreed.

## Invariants

Checked after every tick in tests, and on demand in the app ([Testing](testing.md)):

1. Every direct transfer has equal hours on both sides.
2. Hours are conserved: hours in all stocks + consumed + scrapped = hours entered (labour + wear + arrivals from the rest of the economy).
3. For each unit in each period: transferred to the community = (f + c + l) + over/under.
4. Over a closed period, a branch's overs and unders sum to zero.
5. Certificates issued in a period ≤ hours of consumer goods available to households in that period.
6. No certificate is ever transferred between units.

## Reports

- A unit's books for a period, laid out as in the book: `1,250 + 61,250 + 62,500 = 125,000 working hours`.
- A batch's hours: f, c, l and its sources.
- A branch table, as in [E3](../../notes-opus5_5/fundamental-principles-economic-model.md#e3-the-social-average-production-time).
- The payout factor worked out with the period's figures, as in [E7](../../notes-opus5_5/fundamental-principles-economic-model.md#e7-the-payout-factor-fic).
- The flow of hours along the chain, for the [user interface](user-interface.md#views-of-the-hours).

---

[↑ Plans](README.md)
