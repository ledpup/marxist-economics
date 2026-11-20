[↑ Plans](README.md)

---

# Gaps in the brief

What the [brief](README.md#patricks-brief) leaves out, gets at odds with the GIC's model, or needs to settle before code is written. Gaps keep their numbers when they move from Open to Decided.

**Open: 14.** Each has a proposal that stands as the default until overruled.
**Decided: 40.** In [Decided gaps](gaps-decided.md), each with the decision and why.
Patrick's answers, which settled them, are in [Patrick's answers on the gaps](gaps-answers.md).

## Open

### The economics

- **53. Care of disabled people.** Gap 8 pays child care, through the child care unit, and school takes over at 6. Gap 9 credits a disabled adult a full week, gives nothing extra per child, and leaves special equipment out of scope. None of this fits a profoundly disabled child, whose care may be lifelong, intense, partly at night, and never passed to a school; nor an adult cared for at home. Neither the GIC nor TNS say anything about the carers ([note](../../notes-opus5_5/the-outside-and-the-edges.md#domestic-labour)). *Proposal:*
  - **The carer is paid as public work**, as child carers are: a public **care unit** records their hours, at home or at a centre, within a budget set by the congress. Their hours are in L<sub>p</sub>. There is no age limit: the care goes on as long as it is needed, for a child or an adult.
  - **Hours by assessed need, not stopwatch.** Much of the care can't be timed (nights, being on call). The care unit sets the weekly hours by an assessment of need, reviewed periodically, and records those. This no longer measures labour exactly, as gap 8's flat-rate option doesn't; it is the price of bringing the work into the books at all.
  - **Respite.** The care unit runs, or buys from a centre, regular breaks for the carer, as the child care centre does for a parent in a child's first year.
  - **The disabled person's needs are public provision**, free, like health care: equipment, therapy, adapted housing. They don't come out of the household's certificates. This is where "nothing extra per child" (gap 9) would be at its most unjust. It reopens gap 9's "special equipment out of scope" for the design, though the shoe scenario need not model it in phase 1.
  - **A disabled person who can work** works, at their own pace, and is credited their hours like anyone else; pace never changes pay ([gap 10](gaps-decided.md#the-economics)). Credited hours (H) top them up to a full week if they can work only part of it, as for the retired.
  - A policy, so a run can switch it off and compare. It lowers the payout factor, as child care does.

  → [Accounting](accounting.md#labour-certificates), [Data model](data-model.md#scenario-and-policies)
- **54. Housework that isn't care.** Cooking, cleaning, laundry and the upkeep of a home stay off the books. Women do most of it: 76.2 % of unpaid care hours worldwide (ILO, 2018). TNS credit it only when it is collective, in a commune; in a family, never ([note](../../notes-opus5_5/the-outside-and-the-edges.md#domestic-labour)). *Proposal:* record it beside the books, as hours *not credited*, so the largest outside is visible: a policy, off by default, drawn per household from the seed. A later version can add communal kitchens and laundries as units (TNS's commune, or a public or productive unit), and show the hours they save.
- **48. Leaving a unit, and finding another.** Gap 47 lets a council dismiss, and leaves people free to refuse work. Neither book says what happens next ([unemployment note](../../notes-opus5_5/unemployment-and-inability-to-work.md#what-the-book-leaves-open)). *Proposal:*
  - **How a dismissal is decided.** By the unit's assembly (its delegates, in a large unit), by vote, with the reason recorded in the unit's books, which are open to all. Never by one person, and never by a body outside the unit.
  - **Appeal.** A dismissed worker can appeal to a body the congress of councils sets up. One option is TNS's: a jury drawn by lot from workers of other units.
  - **Between units.** Someone whose unit shrinks or closes, or who is dismissed, is credited their usual hours for a search period while they look for another place: hours credited without work (H), as for illness ([gap 9](gaps-decided.md#the-economics)). A starting figure of 8 weeks. Dismissal is not a sentence to hunger. After the period, or for someone who leaves by choice, nothing until they work again, unless they are unable to.
  - **Finding a place.** Each unit posts its vacancies, within its planned labour budget. A person applies; the unit's assembly accepts or declines, as TNS's project workers do ("has convinced those currently working on it of her suitability"). Nobody is assigned.
  - **Those who refuse to work** get no certificates and keep the free services: child care, school, electricity and water at home.

  → [Workers' democracy](workers-democracy.md#dismissal-where-we-break-with-tns)

### The data

- **21. "Consumable" mixes the kind of thing with the stock of it.** *Proposal:* **Product** (the kind: "upper leather", unit m², branch "tanning") and **Batch** (a quantity of it, where it is, its production time). "Consumable" becomes a category of product (circulating means of production), alongside machines (fixed) and consumer goods. → [Data model](data-model.md#product)
- **22. Functions have no recipe.** *Proposal:* a function carries a recipe: inputs, outputs, machine and hand time, crew, machines, power. → [Data model](data-model.md#function)
- **23. Units of measure.** Pairs, m² of leather, kg of rubber, kWh, metres of thread. → [Data model](data-model.md#product)
- **24. Operational unit and building overlap.** Both have a location. *Proposal:* the unit keeps the books and runs one or more buildings; the building is the physical place, holds the functions and has the location. → [Data model](data-model.md#operationalunit)
- **25. Person, role, employer and hours.** *Proposal:* **Skill** (person, role, level, pace) and **Employment** (person, unit, role, hours a week, shift). Hours worked go in a work log, not on the person. → [Data model](data-model.md#employment)
- **26. Households.** People share homes and children depend on adults. *Proposal:* a **Household** that lives in a dwelling and pools its members' certificates. → [Data model](data-model.md#household)
- **27. Building capacity, of what?** *Proposal:* separate limits for residents, workers and storage. → [Data model](data-model.md#building)
- **28. Building types.** Public buildings, warehouses and depots are missing. *Proposal:* a building's kind follows from its functions; keep a kind field only for drawing. → [Data model](data-model.md#building)
- **29. Buildings missing from the shoe example.** *Proposal:* add the shoe factory, the consumer cooperative's store, the components works (thread, laces, soles), a freight depot, a school and a child care centre. → [Shoe scenario](shoe-scenario.md)
- **30. Location.** Latitude and longitude don't fit a grid. *Proposal:* a grid cell (x, y) and a footprint; latitude and longitude optional. → [Data model](data-model.md#location)
- **32. "What they are doing".** *Proposal:* each person has a current activity (at home, travelling, cutting uppers, at school, at the child care centre, caring, shopping). → [Data model](data-model.md#person)

---

[↑ Plans](README.md)
