[↑ Plans](README.md)

---

# Shoe scenario

The first scenario: the shoe chain from [Following a shoe through the chain](../../notes-opus5_5/fundamental-principles-economic-model.md#following-a-shoe-through-the-chain), cut down to what one small town can show. The shoe factory's yearly totals are the book's ([7 d](../../Documents/fundamental_principles/07_The_Communist_Production.md#d-communist-reproduction)); the tannery's are from the note's illustration; everything else is invented and marked so.

## Scale

The book's factory makes 40,000 pairs a year with 62,500 hours of work. Over 250 working days that is **160 pairs and 250 hours of work a day**. A full-time week is 32 hours, four days of 8 ([gap 44](gaps-in-the-brief.md#decided)), or about 1,600 hours a year, so the factory needs **about 39 people**, with about 31 at work every day. Small enough to simulate every person, and large enough to need a map.

## Units, buildings and functions

The brief's buildings (tannery, sole moulding works, power station, homes), plus the ones the chain needs ([gap 29](gaps-in-the-brief.md#the-data)). Thread and braiding share a building with sole moulding, as the brief allows.

| Operational unit | Type | Building | Functions | Roles (people) |
| --- | --- | --- | --- | --- |
| Shoe factory | productive | Shoe factory | cutting, closing, lasting, finishing | cordwainer (39, two of them part-time child carers), designer (1) |
| Tannery | productive | Tannery | tanning, leather finishing | chemical worker (5) |
| Components works | productive | Components works | sole moulding, flash grinding, thread works, braiding works | chemical worker (4), textile worker (1) |
| Power station | mixed | Power station | generation | electrician (3) |
| Freight unit | productive | Depot | freight (2 lorries) | driver (4) |
| Consumer cooperative | productive | Cooperative store | retail | store worker (4) |
| School | public | School | teaching | teacher (4); students aged 12 and over are paid for their hours ([gap 8](gaps-in-the-brief.md#decided)) |
| Child care unit | public | Child care centre | child care | child carer (8): 4 at the centre, 4 at home ([gap 8](gaps-in-the-brief.md#decided)) |
| None: existing housing | out of scope ([gap 43](gaps-in-the-brief.md#decided)) | Homes (about 50 dwellings), there from the start | — | — |
| Rest of the economy | boundary | Gate, at the map's edge | supply, receipt | — |

About 65 workers and 8 child carers; about 120 people in all, with children, students and the retired. Roles not in the brief (textile worker, driver, store worker, teacher) are *new*; the brief's home carer is renamed child carer.

A child under 1 is looked after full-time by their primary carer, who is a child carer for that year; the centre takes the infant part-time only. From 1 to 5, children spend the working day at the centre, or at home with a child carer. Of the four carers at home, one has an infant, one cares at home only, and two also work part-time in the shoe factory, on a morning or an afternoon shift; their children are at the centre during those hours. From 6, children go to school. The numbers are *invented*.

The school and the child care unit make the payout factor fall below 1 from the start. Their budgets, in hours a year, are *to fill in*.

## The chain

```
                ┌──────────── electricity (charged to units, free to homes) ──────────────┐
                │                                                                         │
 GATE ──hides, chemicals──► TANNERY ──upper leather──────────────────────► SHOE FACTORY ──shoes──► COOPERATIVE ◄── HOMES
 (rest of        │                                                           ▲   ▲   │              STORE
  the economy) ──synthetic rubber──► COMPONENTS WORKS ──soles, thread, laces─┘   │   └──offcuts──► GATE
                 │                                                                │
                 └──lining, boxes, adhesive, eyelets, fuel ───────────────────────┘
 Every arrow between buildings is a freight leg run by the freight unit.
 Shoes not bought in the town go back through the gate.
```

## Figures

### Shoe factory (the book's figures, a year)

| Input | Hours | From |
| --- | --- | --- |
| f: wear on machines and building | 1,250 | |
| c: upper leather | 30,000 | Tannery |
| c: soles | 14,000 | Components works |
| c: lining, boxes, adhesive, eyelets | 10,000 | Gate |
| c: electricity | 2,500 | Power station |
| c: inbound freight | 2,000 | Freight unit |
| c: laces, thread | 2,750 | Components works |
| l: hours worked | 62,500 | |
| **40,000 pairs** | **125,000** | 3.125 hours a pair |

The c lines are the note's illustration, with the gate's inputs grouped.

### Tannery (the note's illustration, a year)

| | Hours |
| --- | --- |
| f | 1,000 |
| c: hides | 14,000 (book check) or 2,000 (by-product method) |
| c: chemicals | 5,000 |
| c: freight | 1,500 |
| c: energy and water | 1,000 |
| l | 7,500 |
| **Upper leather** | **30,000** or **18,000** |

### Components works (*invented*, a year)

| Product | f | c | l | Total |
| --- | --- | --- | --- | --- |
| Soles | 700 | 7,300 (rubber, electricity, freight) | 6,000 | 14,000 |
| Thread | — | — | — | 1,250 |
| Laces | — | — | — | 1,500 |

To fill in: the split for thread and laces, the power station, the freight unit, the store. The downstream figures in [the note](../../notes-opus5_5/fundamental-principles-economic-model.md#downstream-from-the-factory-to-the-worker) give the store's share (0.20 hours a pair) and the freight.

### Recipes

To fill in, per function: inputs and outputs per batch, crew, machines, minutes, kWh. A batch is a crate of 20 pairs (8 a day).

## Two versions

| Version | Hides arrive at | Shoe factory's year | Purpose |
| --- | --- | --- | --- |
| **Book check** | 14,000 hours | 1,250 + 61,250 + 62,500 = 125,000; 3.125 a pair | Reproduces the book's figures. A test, not the default |
| **By-product method** (default) | 2,000 hours: the slaughterhouse's post-split-off hours only | 1,250 + 49,250 + 62,500 = 113,000; 2.825 a pair | The brief's choice of method. Shows how much an accounting convention moves the figure |

## The rest of the economy

One aggregate unit at a gate on the edge of the map ([gap 4](gaps-in-the-brief.md#decided)).

- **Supplies** at fixed production times: hides, chemicals, synthetic rubber, lining, boxes, adhesive, eyelets, fuel, replacement machines, and the households' daily basket (food, heat, clothes other than shoes).
- **Receives** the shoes the town doesn't buy (nearly all of them: about 120 people buy one pair a year each, against 160 pairs a day) and the leather offcuts.
- Keeps books like any unit. Over a period, what it receives and what it supplies should roughly match: that is simple reproduction for the town as a whole. The difference is shown, not hidden.

## People and the day

- Units run 08:00–16:00, Monday to Friday ([gap 44](gaps-in-the-brief.md#decided)). Each full-timer has one weekday off, and the days off are spread evenly over the week, so the factory runs at capacity every day; a few choose all five days. Part-time shifts are 08:00–12:00 or 12:00–16:00, and part-timers may add a fifth day. People travel from home to work along the grid; how they get there (on foot, by bike, bus or car) is not modelled ([gap 16](gaps-in-the-brief.md#decided)).
- Everyone has one pair of shoes, which lasts a year ([gap 18](gaps-in-the-brief.md#decided)). At the start, each pair has a random age, so pairs wear out on different days. When a pair is worn out, its owner goes to the store for a new one, paid from the household's certificates.
- Each household draws its daily basket from the store.
- Each person has a pace of their own, set at the start from the seed. In the shoe factory, cutting and closing are mostly hand work, so the cordwainers' pace shows in the factory's hours per pair. Sole moulding is mostly machine time, so it hardly shows there.
- Random: who is absent, each person's pace and its daily variation, machine breakdowns, when a household shops, the age of each pair of shoes at the start.

## Later versions

- Three shoe factories, as in [8 d](../../Documents/fundamental_principles/08_Average_Working_Hour_as_Basis_of_Production.md#d-the-difference-in-company-productivity): 40,000, 65,000 and 100,000 pairs, to show the social average.
- A clinic, lowering the payout factor further.
- The slaughterhouse inside the map, applying the by-product method directly.
- 10 % expansion ([E9](../../notes-opus5_5/fundamental-principles-economic-model.md#e9-expansion-of-production)).

---

[↑ Plans](README.md)
