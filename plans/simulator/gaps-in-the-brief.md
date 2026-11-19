[↑ Plans](README.md)

---

# Gaps in the brief

What the [brief](README.md#patricks-brief) leaves out, gets at odds with the GIC's model, or needs to settle before code is written. Gaps keep their numbers when they move from Open to Decided.

**Open: 13.** Each has a proposal that stands as the default until overruled.
**Decided: 39.** In [Decided gaps](gaps-decided.md), each with the decision and why.
Patrick's answers, which settled them, are in [Patrick's answers on the gaps](gaps-answers.md).

## Open

### The economics

- **7. Setting the payout factor during a period.** The book never says how a running factor is set before the year's totals exist ([What the book leaves open](../../notes-opus5_5/fundamental-principles-economic-model.md#what-the-book-leaves-open)). With child care and the school (gap 8) the factor is below 1 from phase 1; a clinic comes in phase 5. *Proposal:* the factor in use is the last period's, reconciled at the end of each period. → [Accounting](accounting.md#the-payout-factor)
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
