[↑ Plans](README.md) · [Gaps in the brief](gaps-in-the-brief.md)

---

# The key number: day one, from money to hours

The simulation starts where the GIC say a communist economy starts: with the books in money, converted to working hours **once**, by a single number ([17 b](../../Documents/fundamental_principles/17_Final_Considerations.md#b-from-the-money-account-to-the-working-time-account), [17 c](../../Documents/fundamental_principles/17_Final_Considerations.md#c-the-key-number)). This page records what the GIC say, how I read it, a first estimate of the number, and what it means for the model. It revises [gap 5](gaps-decided.md#the-economics). Everything marked *estimate* is a guess for Patrick to correct.

## What the GIC say

- **The conversion is one-off, and borrowed from history.** Money is not abolished by decree. A proletarian revolution will first print money (inflation is certain), operational life stalls, and then "stabilization" means a new unit of account. If the workers can abolish wage labour, that unit is the working hour. "The conversion of money into working hours will then be done in the same way as in the past the conversion of paper marks into gold marks" ([17 b](../../Documents/fundamental_principles/17_Final_Considerations.md#b-from-the-money-account-to-the-working-time-account)). Germany's 1923 conversion (a trillion paper marks to one gold mark) is their model.
- **The number is hours per unit of money.** "If this average turns out to be 0.80 Dollar 1 working hour", every unit multiplies its money amounts by 1¼ (1 ÷ 0.80). The passage mixes guilders, dollars and marks; the arithmetic is the same whichever is meant ([E11](../../notes-opus5_5/fundamental-principles-economic-model.md#e11-the-key-number-converting-money-to-hours)).
- **It converts the stock, not the labour.** The shoe factory's f (Mark 1,000) and c (Mark 49,000) become 1,250 and 61,250 hours. l is the hours worked, 62,500, already in hours. So the key number touches only means of production.
- **How to find it.** Take mass-produced goods (coal, electricity, iron, potash). From the books read the tons produced and the *actual cost price*; leave out interest on capital; work out the hours used; so find the money per hour of each industry; average them for "a provisional general average".
- **It is an estimate, and they say so.** "It is not possible to calculate the first key number exactly. We can only try to estimate it as accurately as possible." Once everyone keeps books in hours, "the actual production times are displayed very quickly." Their warning is Russia in 1921–23 ([footnote 102](../../Documents/fundamental_principles/17_Final_Considerations.md#c-the-key-number)): firms restarting without a cost basis set prices arbitrarily, and the figures soon proved wrong.
- **There is an outside.** The changeover happens inside an economy with other economies and other classes around it. The GIC never follow the outside after day one. Foreign trade is mentioned once ([10 f](../../Documents/fundamental_principles/10_The_General_Social_Work.md#f-the-marxist-solution)).

## What it means for the simulation

1. **Day one is a conversion.** The scenario's opening books are in money, with a stated key number. At tick 0 every stock, machine, building and product is converted once, and each carries its hours from then on. The conversion is an entry in the books, so it can be shown and checked. Nothing is converted from money afterwards.
2. **The gate is the explicit outside.** What crosses it on day one (hides, chemicals, rubber, lining, boxes, and so on) has a money price in the scenario, converted at the key number. This replaces gap 5's "estimates, never converted from money".
3. **Inside products get a provisional time and then a real one.** Leather, soles and shoes start at their converted figures. At the first close, the actual averages from the books replace them ([Accounting](accounting.md#the-social-average)). That is the GIC's "displayed very quickly", and the model can show it: estimate against actual.
4. **What stays an estimate is what comes through the gate.** The model doesn't follow the outside, so its products keep the day-one hours. How wrong the key number was then shows in the town's actual production times (see [sensitivity](#how-much-the-key-number-matters)). What the gate does after day one is open ([gap 52](gaps-in-the-brief.md#the-economics)).
5. **Hours are integers.** Conversion gives fractions of a second, so each amount is rounded to whole seconds with the remainder carried, as everywhere else ([simulation decisions](gaps-decided.md#the-simulation)).

## A first estimate of the number

The GIC's method is bottom-up, from industries whose books we don't have for our town. I tried three routes. The figure that matters is **money per working hour**; the key number is its reciprocal.

| Route | Money per hour | Reasoning |
| --- | --- | --- |
| **Whole economy** | about $98, less about a third: **$60–70** | OECD GDP per hour worked for the US in 2023 is about $97.7 in current PPP dollars ([The Global Economy, from OECD](https://www.theglobaleconomy.com/USA/productivity_current_USD/)). Total hours in the economy go into total final product, so GDP ÷ hours is the money per hour of all labour. The GIC leave out interest, so I take off about a third for profit, interest, rent and taxes. *The third is my assumption.* |
| **Coal, the GIC's own example** | **$150–300** | US coal in 2023: $54.04 a short ton and 5.66 tons per employee hour ([EIA Annual Coal Report](https://www.eia.gov/coal/annual/)), so $306 per hour of miners' work. Counting the hours behind the explosives, diesel and machines would perhaps double the hours, giving about $150. Mining is capital-intensive and its prices include royalties, so it sits well above the average. *The doubling is my assumption.* |
| **A shoe** | **$10–50** | A European analysis puts the labour in a branded sneaker at 60 to 90 minutes, with $16–25 ex-factory ([Complex](https://www.complex.com/sneakers/2016/05/sneaker-manufacturer-cost), second-hand and rough). The book's shoe is 3.125 hours; a durable leather shoe at about $150 ex-factory gives $48 an hour. A low-wage plant gives a far lower figure. |

The routes disagree because the GIC's method has a catch. Direct hours in a capital-intensive industry understate the hours behind its product, so the money per hour comes out too high. That is why the whole-economy route is the anchor, and why the GIC's average "of all these industries" is only provisional.

**Default: $60 an hour, so a key number of 1 ÷ 60 = 0.01667 hours per dollar.** $1 is one minute of average labour. It is a parameter of the scenario, and a scenario can set another economy's figure. It plays the part of the GIC's 0.80 → 1¼.

A check from the other side: a full-time worker's 26.6 hours of certificates a week ([gap 44](gaps-decided.md#the-economics)) is $1,600 at $60, or about $83,000 a year. Spread over the people that worker supports (about 1.8 each, with children, retired and students), that is about $46,000 a head, the same order as US personal consumption per head (about $60,000, which includes healthcare and housing, both outside this scenario). That is a reasonable sign the number isn't badly out.

## Opening figures for the shoe scenario

The book's figures (in hours) written as the money books they would have started from, at $60 an hour. The hours are the book's and the illustration's; the dollars are *estimates* derived from them, and for the gate lines are the money prices the scenario would carry. A year, for 40,000 pairs.

| Line | Hours | Dollars (*estimate*) | Per pair | From |
| --- | --- | --- | --- | --- |
| Shoe factory f: wear on machines and building | 1,250 | 75,000 | $1.88 | Town |
| c: upper leather | 30,000 | 1,800,000 | $45.00 | Tannery |
| c: soles | 14,000 | 840,000 | $21.00 | Components works |
| c: lining, boxes, adhesive, eyelets | 10,000 | 600,000 | $15.00 | **Gate** |
| c: electricity | 2,500 | 150,000 | $3.75 | Power station |
| c: freight | 2,000 | 120,000 | $3.00 | Freight unit |
| c: laces, thread | 2,750 | 165,000 | $4.13 | Components works |
| l: hours worked | 62,500 | *not converted* | | Workers |
| **Shoe factory, 40,000 pairs** | **125,000** | | | 3.125 hours a pair |
| Tannery c: hides | 14,000 (book check) or 2,000 (by-product) | 840,000 or 120,000 | | **Gate** |
| Tannery c: tanning chemicals | 5,000 | 300,000 | | **Gate** |
| Components works c: synthetic rubber | *to fill*, part of 7,300 | | | **Gate** |

Notes:

- The per-pair figures look plausible for a durable leather shoe: about $45 of leather and $21 of soles in a pair whose whole production time, 3.125 hours, is $187.50 at this key number. That is my judgment, not a source.
- Electricity at 2,500 hours is $150,000, about 1.9 GWh a year at the 2024 US industrial price of 8.13 cents a kWh ([EIA](https://www.eia.gov/electricity/sales_revenue_price//pdf/table_4.pdf)), or 46 kWh a pair. That looks high for a shoe factory (my guess is a tenth). The scenario's own recipes, in kWh per batch, should decide it; the book's 2,500 isn't a target.
- The by-product hides, $120,000 for about 10,000 hides, is about $12 a hide; US hide prices have fallen a long way ([Leatherbiz](https://leatherbiz.com/News/154398)). *The hide count and the price are both unchecked.*
- The households' daily basket from the gate is whatever their certificates buy after shoes: with about 68 workers at $1,600 a week, about $110,000 a week, which is the gate's biggest flow. Its split into food, clothes and so on is *to fill*.

## How much the key number matters

Only the gate's share depends on it once the books are running. In the book check, the gate supplies the hides (14,000), the tanning chemicals (5,000) and the shoe factory's lining, boxes, adhesive and eyelets (10,000): 29,000 of the shoe's 125,000 hours, plus some rubber, so **about a quarter**. If the key number is 20 % too high or too low, the shoe's production time is about 5 % out (3.125 becomes about 3.3 or 2.97). Everything else is the town's own labour and wear, which the books measure.

A run can show this directly: the same scenario with the key number set 20 % high, against the base run.

## Open

- **After day one, what does the gate do?** [Gap 52](gaps-in-the-brief.md#the-economics).
- **Which economy's $60?** The default is a rich-country economy-wide figure. A scenario in a poorer economy would have a far lower money-per-hour and so a different key number, though the same hours.

---

[↑ Plans](README.md) · [Gaps in the brief](gaps-in-the-brief.md)
