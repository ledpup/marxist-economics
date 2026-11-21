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
4. **What stays an estimate is what comes through the gate.** The model doesn't follow the outside, so its products keep the day-one hours. How wrong the key number was then shows in the town's actual production times (see [sensitivity](#how-much-the-key-number-matters)). After day one the gate keeps those hours and money is not used again ([gap 52](gaps-decided.md#the-economics)).
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

## Decided and open

- **After day one** the gate keeps the converted hours; no money is used ([gap 52](gaps-decided.md#the-economics)).
- **The $60 an hour is a default**, a scenario variable. A scenario set in a poorer economy would have a different money per hour and so a different key number, with the same hours. The equations and logic matter more than the values.
- **Where the book is silent or wrong** is the thing to investigate. So far: the GIC never say how the outside is converted, or what becomes of it after day one; and their method of averaging industries from direct hours is biased towards capital-intensive ones (above).

---

[↑ Plans](README.md) · [Gaps in the brief](gaps-in-the-brief.md)
