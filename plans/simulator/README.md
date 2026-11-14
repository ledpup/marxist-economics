[↑ Marxist Economics](../../README.md)

---

# Plans: a simulation of production in labour time

Plans for a web-based simulation of production under the GIC's model in the *[Fundamental Principles](../../Documents/fundamental_principles/README.md)*. The economics is summarised in [The economic model of the *Fundamental Principles*](../../notes-opus5_5/fundamental-principles-economic-model.md). The simulation starts with the shoe chain worked out in that note.

These are drafts. Most plans are stubs: they name the parts and the open questions, and get filled in as work starts.

## What the simulation is for

To **see hours accumulate and move**. Workers' hours and the wear on machines enter a product. The product is passed on at its production time and becomes part of the next unit's means of production. The finished shoe reaches the consumer cooperative's store. A worker buys it with labour certificates and comes back to work the next day.

The view is aerial, 2D and on a grid, a bit like SimCity. Goods are animated as they move, but this is not a transport simulation. Buildings and vehicles can be clicked to show who is there, what they are doing, and what the hours add up to.

## The plans

| Plan | What it covers | Status |
| --- | --- | --- |
| [Gaps in the brief](gaps-in-the-brief.md) | What the brief below leaves out or needs to settle, with a proposal for each. **Start here.** | Draft |
| [Glossary](glossary.md) | The terms the simulation uses, the GIC's term behind each, and the Spanish | Draft |
| [Data model](data-model.md) | The abstract model: definitions, the world, the books, policies | Draft |
| [Shoe scenario](shoe-scenario.md) | The first scenario: units, buildings, functions, recipes and figures | Draft |
| [Workers' democracy](workers-democracy.md) | Who runs a workplace and sets its rules: workers' councils, not trade unions; dismissal; a job for those who want one. Contrasts the GIC with *Towards a New Socialism* | Draft |
| [Accounting](accounting.md) | The books: direct transfers, social average, labour certificates, payout factor, by-product method, invariants | Draft |
| [Simulation engine](simulation-engine.md) | The clock, the daily cycle, the systems that run each tick, random numbers and determinism, dishonesty | Stub |
| [User interface](user-interface.md) | The map, zoom, selection panels, time controls, views of the hours | Stub |
| [Technology](technology.md) | Options for the web stack and a recommendation | Draft |
| [Internationalisation](internationalisation.md) | English and Spanish from the start; translatable data | Stub |
| [Testing](testing.md) | Checks against the book's figures, invariants, determinism | Stub |

## Decisions taken from the brief

- **Terms:** "labour certificate", not "consumption money". "Direct transfer", not "giro settlement". See the [glossary](glossary.md).
- **Joint production:** the by-product method. The main product carries all the hours up to the split-off point; the by-product carries only its own hours after it. See [Accounting](accounting.md#joint-products-the-by-product-method).
- **Scope:** simple reproduction of the shoe chain. Luxury goods, which leave the cycle, are out of scope.
- **Random numbers** come from a seeded generator, so a run can be repeated.
- **Languages:** English and Spanish, switchable at run time.

Patrick's answers on the gaps (2026-11-09) settled more. The details are in [Gaps in the brief](gaps-in-the-brief.md):

- **Unit types** are the GIC's: productive, public, mixed.
- **The shoe's hours end at the store** as individual consumption; the loop back to the worker is shown but not booked as an input.
- **The rest of the economy** sits at the map's edge as one aggregate unit.
- **Branches** exist from the start, for the social average.
- **Child carers are paid** as public work, through a child care unit with a budget, at its centre or at home (renamed from home carers 2026-11-10). A child's primary carer is a full-time child carer for the child's first year; school starts at 6. Care is paid following the [assessment of the 2026 debate](../../notes-opus5_5/general-social-work.md#assessment-my-reading). **Students are paid from age 12.** Both lower the payout factor.
- **Pay never depends on skill or speed**, but each person has their own pace, and a slow crew raises the unit's production time. Machines set the pace of machine work.
- **Machines and buildings** both carry hours and wear, and exist at the start. Machine-building is a later chain (2026-11-10). New technology is out of scope.
- **No gender** in the model (2026-11-10). In Spanish, roles are named by trade or activity.
- **Housing is out of scope** (2026-11-10): existing homes, outside the books.
- **People who do not work** (2026-11-10): retirement is a choice from 65, credited 20 hours a week on top of any work, up to a full week; part-time work is open at any age; the ill and injured are credited their usual hours until fit. Children consume out of the adults' certificates, with nothing extra per child. Their credited hours lower the payout factor.
- **A 32-hour week** (2026-11-10): four days of 8 hours. Units run at capacity Monday to Friday; each full-timer's day off can fall on any weekday, and some may choose five days. Part-time is a 4-hour morning or afternoon shift.
- **Repeatable runs** (2026-11-11): one seeded generator; the same build, scenario and seed give the same run. Runs from different builds need not match.
- **Internationalisation** (2026-11-11): names in the data are translation keys; Spanish roles are named by trade or activity; numbers and dates are formatted by the browser's `Intl`; the Spanish terms stay provisional until checked against Spanish editions of the GIC and Marx.
- **The designer and boutique lines** (2026-11-14): the designer works in the shoe factory; the mainline design is fixed means of production, worn per pair. Boutique lines (a later version) are made on 0, 1 or 2 of a cordwainer's days a week, with trainees on 2, at their own higher production time.
- **Workers' democracy** (2026-11-14): each unit is run by its workers' council, which sets its own working week, shifts and part-time patterns and can dismiss as a last resort. Councils, not trade unions. A job for those who want one, not full employment. See [Workers' democracy](workers-democracy.md).
- **The simulation** (2026-11-11): a tick is one simulated minute, and play starts at real time; certificates weekly, books closed monthly and yearly. Hours are integer seconds, with remainders carried so the books balance exactly. Goods move in batches. Runs can be saved and loaded, and the books exported as CSV. Dishonesty (theft, cooking the books, shirking) comes soon after the first builds, but from phase 1 the engine keeps what happened apart from what was reported, and the books are written only from reports.

## Phases

1. **Headless core.** Data model, books and a daily cycle for the shoe chain, run without graphics. Its yearly totals are checked against the book's 125,000 hours for 40,000 pairs.
2. **Map.** Grid, buildings, zoom and pan, time controls, a selection panel for buildings.
3. **People and goods in motion.** People go to work and home again; shipments animate between buildings; vehicles can be clicked.
4. **Views of the hours.** A product's hours broken down into f, c and l, the flow of hours along the chain, the books of each unit. Spanish.
5. **Wider model.** Three shoe factories for a real social average; a clinic; expansion. Then scale.

## Patrick's brief

> Create a plan(s) for a software simulation of the model. The software will be the simulation of production. As we have shoes already worked out, start with that. We'll want multiple plans for each of the different areas. An abstract model of the data, the simulation module (that operates over the model), the user interface, etc. Stub most of it out for now. A plan for a sub-component can just have a few lines if need be. Find gaps I have with the below.
>
> **Model components**
>
> The components we will need to model are in dot points, with some of their properties.
>
> - Person: id, name, gender (m/f/not disclosed), age, roles (id, skill level, hours worked), employer(s), residence
> - Role: id, name (home carer, electrician, chemical worker, cordwainer, designer, student)
> - Consumable: id, name, production hours
> - Machine: id, name, production hours, depreciation (wear and tear)
> - Building: id, name, location, type (residential, productive, consumer store), capacity, functions, machines, consumables
> - Function: id, name, role id. Functions are things like "braiding works", "thread works". A building can have multiple functions.
> - Location: lat, long
> - Transport: id, name, speed, operator, location
> - Operational unit: id, name, type (public, private, mixed), location, employees (list of person)
>
> **Simulation**
>
> The software will appear as an aerial viewpoint to the user of the operational units, the links between them, and residencies. It will work a bit like [SimCity](https://en.wikipedia.org/wiki/SimCity). A grid is fine. 2 dimensional is fine. This is not a transport simulation, although we want to animate goods moving around. The buildings can be clicked on. When clicked, we'll be able to see a list of the people who are there and what they are doing. Each day, consumables will need to be delivered to the buildings, people need to arrive at work, machines are used, components are made and transported to the next part of the production process (may be moved within the building or transported). We'll use random numbers for some things so have a seed.
>
> The main point is to see the hours accumulate, transfer into the products, and how they then go into the next product as a consumable. In many ways, the end product (the shoe) becomes a consumable for the worker to be able to come back the next day. I.e., it re-enters the production process again. Only luxury items don't do that and we don't need to consider these here.
>
> **Technology choices**
>
> I want it to run on a website. Can be JavaScript, Web Assembly, or anything that can animate a number of simple objects around our map. We'll want to zoom in/out. We'll need to be able to click on the visible elements - transport, buildings most. The languages I'm used to are C#, Blazor or other SPA (Vue, React), JavaScript. I'm not tied to anything in particular. A game engine that can run on Web Assembly might be good. Provide options. Ultimately, I may want to simulate a large amount of data, so we want something efficient.
>
> **Other changes**
>
> - Use "by-product method" for joint production
> - Use "labour certificate" instead of "consumption money"
> - Use "direct transfer" instead of "giro settlement"
>
> **Important**
>
> - Design this with internationalisation in mind. We want to be able to switch languages easily. Can support English and Spanish to begin with.
>
> **Shoe example**
>
> - Buildings
>   - Tannery
>   - Sole moulding works
>   - Power station
>   - Homes (where workers live)
>
> We don't necessarily need all of those buildings as separate buildings. Buildings can have multiple functions.
>
> Create a new "plans" folder.

---

[↑ Marxist Economics](../../README.md)
