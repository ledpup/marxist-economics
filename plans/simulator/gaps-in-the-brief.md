[↑ Plans](README.md)

---

# Gaps in the brief

What the [brief](README.md#patricks-brief) leaves out, gets at odds with the GIC's model, or needs to settle before code is written. Gaps keep their numbers when they move from Open to Decided.

**Decided: 27.** 1, 2, 3, 4, 6, 8, 9, 10, 11, 12, 16, 18, 19, 31, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45.
**Open: 18.** Each has a proposal that stands as the default until overruled.

## Open

### The economics

- **5. Where the chain starts.** Hides, synthetic rubber, cotton, chemicals and fuel come from outside. They need a production time on arrival. *Proposal:* the scenario gives one per product, taken from the [shoe illustration](../../notes-opus5_5/fundamental-principles-economic-model.md#following-a-shoe-through-the-chain) or converted from money with the key number ([E11](../../notes-opus5_5/fundamental-principles-economic-model.md#e11-the-key-number-converting-money-to-hours)). → [Shoe scenario](shoe-scenario.md)
- **7. Setting the payout factor during a period.** The book never says how a running factor is set before the year's totals exist ([What the book leaves open](../../notes-opus5_5/fundamental-principles-economic-model.md#what-the-book-leaves-open)). With child care and the school (gap 8) the factor is below 1 from phase 1; a clinic comes in phase 5. *Proposal:* the factor in use is the last period's, reconciled at the end of each period. → [Accounting](accounting.md#the-payout-factor)
- **13. Joint products inside the chain.** The by-product method is chosen. The hide comes from the slaughterhouse, outside the chain at first, so the scenario applies the method through the hides' arrival figure. Inside the chain, cutting leaves leather offcuts and sole moulding leaves flash. *Proposal:* recipes mark each output as *main* or *by-product*. → [Accounting](accounting.md#joint-products-the-by-product-method)
- **14. The designer's work is not used up in one pair.** *Proposal:* the designer's hours are part of the factory's l, like any other worker's (simplest, and true to the book). A design as fixed means of production, spread over a run like a machine, is an option for later. → [Shoe scenario](shoe-scenario.md)
- **15. The mixed unit.** The power station charges factories and supplies homes free ([E8](../../notes-opus5_5/fundamental-principles-economic-model.md#e8-the-payout-factor-with-mixed-units)). *Proposal:* metering per consumer and a split of its books. → [Accounting](accounting.md#the-mixed-unit)
- **17. What decides how much to make?** The book leaves the production plan open. *Proposal:* the cooperative store orders when its stock falls below a target, and each unit upstream does the same for its inputs (a pull system). When the store runs short, first come, first served. → [Simulation engine](simulation-engine.md#demand-and-orders)
- **20. Day one.** Stocks, machines and buildings have no recorded hours at the start. *Proposal:* the scenario sets them; the key number is the method if a scenario starts from money figures. → [Shoe scenario](shoe-scenario.md)

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

## Decided

- **1. The books.** **Decision:** an account for each operational unit and each household, a record of every direct transfer, and a production time carried on every batch of goods. *Why:* the brief's main point is to "see the hours accumulate", but its model had nowhere to keep them. → [Accounting](accounting.md), [Data model](data-model.md#the-books)
- **2. Types of operational unit.** **Decision:** the GIC's three: **productive**, **public** (general social work, free to use) and **mixed** (free to households, charged to other units) ([10 a](../../Documents/fundamental_principles/10_The_General_Social_Work.md#a-two-forms-of-distribution), [10 i](../../Documents/fundamental_principles/10_The_General_Social_Work.md#i-mixed-operational-units)). Not "private". *Why:* there is no private property in the model; the nearest thing is a unit outside the system of direct transfers, which gets no raw materials ([16](../../Documents/fundamental_principles/16_The_Economic_Dictatorship_of_the_Proletariat.md)). → [Data model](data-model.md#operationalunit)
- **3. The shoe's hours end at the store.** **Decision:** the screen shows the loop (shoe → worker → work the next day); in the books the shoe's hours end as individual consumption when the worker buys it with certificates. *Why:* l is the hours worked, not the hours of goods consumed. Adding the shoe's hours to the next product would count the same labour twice, and would bring back Marx's *variable capital* (the wage as a cost of production), which the GIC's equation drops. → [Accounting](accounting.md#labour-certificates)
- **4. The rest of the economy.** **Decision:** one aggregate unit at a gate on the edge of the map. It supplies raw inputs and other consumer goods at fixed production times, receives the shoes not bought locally, and keeps books like any unit. *Why:* a shoe chain can't keep its workers alive. A pair costs about 3.6 hours and lasts months; a full-time worker gets about 26.6 hours of certificates a week. Workers also need food, housing and heat, and the tannery needs hides and chemicals the chain doesn't make. → [Shoe scenario](shoe-scenario.md#the-rest-of-the-economy)
- **6. Branches.** **Decision:** a **Branch** entity from the start; a later scenario with the book's three shoe factories. *Why:* goods pass on at their branch's social average, not the unit's own figure ([E3](../../notes-opus5_5/fundamental-principles-economic-model.md#e3-the-social-average-production-time)). With one factory the two are the same, and one plant over, another under, the branch balanced, never shows. → [Data model](data-model.md#branch), [Accounting](accounting.md#the-social-average)
- **8. Child carers and students.** **Decision:** both are paid as public work. Their hours count in L<sub>p</sub>, so they lower the payout factor for everyone, from phase 1. Both are policies, so a run can switch them off and compare.
  - **Child carers** (the brief's "home carers", renamed 2026-11-10) are paid as in the note's [assessment of the debate](../../notes-opus5_5/general-social-work.md#assessment-my-reading). On the arithmetic the IDA is right: paid care is public labour, and nothing is counted twice. Lueer's point about control also holds, so care is paid only where it is collective enough to have its own operational unit, budget and books. A public **child care unit** runs a **child care centre** and records every child carer's hours, within a budget set in advance by the congress.
  - **The first year.** No full-time care at the centre under age 1. The child's primary carer leaves their workplace for that year and works full-time as the child's carer: the child care unit records a full working week (32 hours, gap 44) for them, and they are credited like any other worker. Caring for an infant is necessary labour. The carer can still use the centre part-time, paid for by the community, as a break, without losing their full week.
  - **Where the care happens.** From age 1, some children spend the whole working day at the centre while their carers work. Some carers work part-time in a productive unit, with the child at the centre during those hours, and care for the child themselves the rest of the time. A few, likely very few, care for the child privately at home and nowhere else. The unit records care at home as well as at the centre; care it doesn't record stays outside the accounts. Care that can't be timed (a night with a sick child) could be paid as a flat rate per dependant from the same budget: an option for later, since it no longer measures labour.
  - **School** starts at 6. In part it is child care too: children are there while the adults who look after them work. **Students** are paid from age 12, for their hours at school. Younger children are not.
  - None of this depends on gender ([gap 31](#decided)): anyone can be a child carer or a teacher.
  - *Why:* neither is a job in a productive unit. The GIC treats training as a social cost but doesn't say whether students are paid; care for children gets nothing in the book.

  → [Data model](data-model.md#scenario-and-policies), [Accounting](accounting.md#labour-certificates), [Shoe scenario](shoe-scenario.md#units-buildings-and-functions)
- **9. People who do not work.** **Decision:** they are provided for out of the social product (Marx's "funds for those unable to work"), in certificates, through the payout factor. Each group is a policy, so a run can switch it off and compare.
  - **Children** are provided for by child care and school ([gap 8](#decided)). Their food, shoes and other goods come out of the household's certificates, earned by its adults: a worker with three children is paid the same per hour as a single worker. The GIC calls this "a great injustice in practical consumption" and accepts it ([9 i](../../Documents/fundamental_principles/09_Average_Working_Hour_as_Basis_of_Consumption.md#i-fair-distribution)); so does the simulation.
  - **Retirement** is a choice from 65, never compulsory. A retired person is credited **20 hours a week**, less than the full week of 32: full retirement is a lower income. The 20 is a starting figure. From 65, a person may go on working, full-time or part-time. A retired person who works is credited their hours worked plus the 20, up to a full week of 32: working 1 hour gives 21, and 12 hours gives 32. Beyond 32 hours worked they are credited their hours worked, like anyone else. The 20 is a top-up to a full week, never more than one.
  - **Part-time work** is open to anyone of working age, not only to carers. Certificates follow the hours worked: if someone can get by on less, that is their choice.
  - **The ill and injured** are credited their usual hours while they can't work (a full week for a full-timer), and are expected back at work as soon as they are fit. Illness and injury are random absences drawn from the seed. Someone permanently unable to work is credited a full week. Special equipment for permanent disabilities is out of scope for now.
  - **In the books.** Hours credited without work (H) are not labour, so they are in neither L nor L<sub>p</sub>. They add to the bottom line of the payout factor, and lower it for everyone: FIC = (L − …) / (L + L<sub>p</sub> + H). This is the note's [illustration](../../notes-opus5_5/unemployment-and-inability-to-work.md#supporting-non-workers-through-the-payout-factor), with the deduction counted in credited hours.
  - *Why:* the book barely covers them ([Unemployment and inability to work](../../notes-opus5_5/unemployment-and-inability-to-work.md)); Marx's third deduction does, and the payout factor is where the GIC's scheme can carry it.

  → [Accounting](accounting.md#labour-certificates), [Data model](data-model.md#scenario-and-policies), [Simulation engine](simulation-engine.md#systems-in-order-each-tick)
- **10. Pay never depends on skill or speed; production time does.** **Decision:** one hour worked is one hour credited, whoever works it ([Unskilled and skilled labour](../../notes-opus5_5/fundamental-principles-economic-model.md#unskilled-and-skilled-labour)). Skill level decides which functions a person may do. Each person also has a **pace** of their own, drawn from the seed, and some are much faster than others. A slower crew raises the unit's production time, and the simulation should show it. But very few are faster than a machine: a recipe splits its time into machine time, which runs at the machine's pace whoever tends it, and hand time, which runs at the worker's. *Why:* the book does not discuss speed within a unit. → [Data model](data-model.md#skill), [Simulation engine](simulation-engine.md#production)
- **11. Machines and buildings carry hours and wear.** **Decision:** both have production hours and a working life; f per hour of use = production hours ÷ working life. New technology (moral wear and tear) is out of scope. → [Accounting](accounting.md#wear-and-tear-f)
- **12. Who makes the machines?** **Decision:** machines and buildings exist at the start, with hours given by the scenario. Replacement machines come through the gate from the rest of the economy (gap 4) at fixed production times. Machine-building is a later chain. *Why:* it isn't part of the shoe chain, and following the shoe doesn't need it. → [Shoe scenario](shoe-scenario.md#the-rest-of-the-economy)
- **16. Transport is a shared service, and freight is never free.** **Decision:** freight is a service any unit can call on, on demand. A unit with goods to send puts a shipment in a single queue shared by all units, and the freight unit serves it first come, first served, as its vehicles come free. The freight unit owns the vehicles and keeps books like any productive unit: each leg passes its hours (f, c and l) to the receiving unit ([10 i](../../Documents/fundamental_principles/10_The_General_Social_Work.md#i-mixed-operational-units)). The brief's "operator" is the person driving, employed by the freight unit. Commuting is not costed, and how people get to work (on foot, by bike, scooter, motorbike, car, bus or train) doesn't matter: the screen shows them moving along the grid, but the journey is not counted. *Why:* the queue is the simplest scheme that lets several units share the vehicles; the book says nothing about getting people to work. → [Data model](data-model.md#vehicle), [Simulation engine](simulation-engine.md#logistics), [Accounting](accounting.md#direct-transfers)
- **18. Shoes last a year.** **Decision:** a pair of shoes lasts **one year** in use. At the start, everyone has one pair, of a random age drawn from the seed, so pairs wear out on different days and demand is spread over the year, not bunched at the start. When a pair wears out, its owner buys a new one at the cooperative store with the household's certificates. Everything else a household needs comes as a daily basket from the rest of the economy ([gap 4](#decided)), as proposed. *Why:* worn-out shoes are what drive demand for the chain's product. At one pair a year each, the shoe scenario's 120 or so people buy a pair about every three days; 10,000 people ([gap 36](#decided)) buy about 27 a day, against the factory's 160. → [Data model](data-model.md#household), [Shoe scenario](shoe-scenario.md#people-and-the-day)
- **19. Expansion, large projects, the disaster fund are out of scope for now.** **Decision:** the scenario is simple reproduction. Expansion (a), special accumulation and the disaster fund keep their place in the payout factor ([E10](../../notes-opus5_5/fundamental-principles-economic-model.md#e10-the-payout-factor-with-expansion)) but are zero until a later phase. *Why:* following the shoe through the chain doesn't need them. → [Accounting](accounting.md#the-payout-factor), [Shoe scenario](shoe-scenario.md#later-versions)
- **31. No gender; age from a birth date.** **Decision:** gender is removed from the model: it plays no part in this. A person has a birth date, and their age (young child under 6, at school from 6, a paid student from 12, working age, retired) is derived from the simulation's date. No role depends on gender: anyone can do any work, child care and teaching included. *Why:* in the GIC's model one hour is one hour, whoever works it. In Spanish, roles are therefore named by trade or activity (gap 40). → [Data model](data-model.md#person)
- **33. Time scale.** **Decision:** a tick is one simulated minute. Play starts at real time (1×), with a speed slider and faster and slower buttons, up to as fast as the engine can run. Certificates are issued weekly; the books are closed monthly and yearly. *Why:* a minute is fine enough for shifts, journeys and batches, and keeps every duration a whole number ([gap 35](#decided)). → [Simulation engine](simulation-engine.md#the-clock), [User interface](user-interface.md#time)
- **34. Hours must balance exactly.** The branch's books "must *always* be 'balanced'" ([8 d](../../Documents/fundamental_principles/08_Average_Working_Hour_as_Basis_of_Production.md#d-the-difference-in-company-productivity)). **Decision:** hours are held as integer seconds. A division (a social average, wear per hour, a payout factor) rounds to the nearest second and carries the remainder to the next entry, so totals balance exactly. A rate per item is kept as a fraction, seconds over quantity, so goods made in bulk don't round to nothing. *Why:* sums of fractional hours drift, and the books would never quite balance; a minute is a whole number of seconds, so recording work never rounds. → [Accounting](accounting.md#numbers)
- **35. Runs repeat within the same build.** **Decision:** the same build, scenario and seed give the same run, with any commands given during it replayed at the same tick. Runs from different builds need not match: a new module may change how an old seed plays out. A seed is necessary, not sufficient. A run also needs:
  - **One seeded generator** with a fixed algorithm (for example PCG32 or xoshiro128\*\*) for the whole engine.
  - **Ordered iteration.** People, units and buildings are always processed in id order.
  - **Integers** in the books and in everything that feeds them: pace in thousandths, durations in whole minutes. No `Math.random`, `Math.log`, `Math.exp` or `Math.pow` in the engine: the same build runs in different browsers, and their last digits can differ.
  - **Nothing from outside the run.** The engine never reads the real clock: play speed only changes how often the interface calls `step`, never what a step does. Commands given during a run (a policy switched mid-year) are logged with their tick.
  - Random: absence, breakdowns, each person's pace, household demand, and later dishonesty ([gap 45](#decided)).

  *Why:* replay within a build is what's needed for now. A separate stream per system, or draws keyed by person and day, would keep old seeds stable across builds, and keep unrelated draws unchanged when one policy is switched on; neither is needed yet. The cost: two runs with the same seed and different policies also differ by chance (different people fall ill), so a comparison needs several seeds, not one. → [Simulation engine](simulation-engine.md#random-numbers-and-determinism), [Testing](testing.md#determinism)
- **36. Scale.** The brief asks for "a large amount of data". **Decision:** about **10,000 people**, every one an agent: a town, not a region. The shoe scenario's 120 or so people are the first step ([Shoe scenario](shoe-scenario.md#scale)); 10,000 is what the engine and the map must handle. Aggregate mode (a crew as a count, not people) is kept for anything larger and is not built for now. *Why:* every person stays visible and clickable, as the brief wants, and the scale fits the chosen technology: TypeScript holds tens of thousands of agents in typed arrays, and PixiJS draws that many sprites. → [Technology](technology.md#decision), [Simulation engine](simulation-engine.md#performance)
- **37. Batches, not items.** **Decision:** goods are made and moved in batches: the factory's 160 pairs a day move as eight crates of 20, not 160 sprites. A batch carries its production time as a whole. *Why:* with 10,000 people on the map ([gap 36](#decided)), every pair as well would be too much to draw and to track, and the books post whole batches anyway ([gap 34](#decided)). → [Simulation engine](simulation-engine.md#production)
- **38. Saving and exporting.** **Decision:** scenarios are files. A run can be saved and loaded: the scenario, the current state and the books, with the generator's state and the log of commands, so a loaded run carries on as it would have ([gap 35](#decided)). The books can be exported as CSV. → [Data model](data-model.md#scenario-and-policies), [Simulation engine](simulation-engine.md#saving)
- **39. Names in the data are translation keys.** **Decision:** the data holds a key (`role.cordwainer`), and the translations live in language files. People's names, and units' proper names, are not translated. *Why:* the brief asks for languages to switch easily, which can't happen if names are fixed in the data. → [Internationalisation](internationalisation.md#rules), [Data model](data-model.md)
- **40. Spanish roles are named by trade or activity.** Spanish job titles have gender: *zapatero* / *zapatera*, *el* / *la electricista*. **Decision:** in Spanish a role is named by its trade or activity (*Zapatería*, *Docencia*, *Cuidado infantil*), and sentences about a person keep the job noun out ("Ana · Zapatería · corte", "trabaja en el corte"). *Why:* the model holds no gender ([gap 31](#decided)), so it can't choose between the two forms, and a person must be addressed correctly. → [Internationalisation](internationalisation.md#job-titles), [Glossary](glossary.md#roles)
- **41. Numbers and dates follow the language.** **Decision:** the browser's `Intl` formats them for the current language: 3.18 hours in English is "3,18 horas" in Spanish. *Why:* it is built into every browser, and FormatJS uses it ([Technology](technology.md#decision)). → [Internationalisation](internationalisation.md#rules)
- **42. Spanish terms for the GIC's concepts.** **Decision:** the Spanish in the glossary stays provisional until it is checked against a Spanish edition of the *Fundamental Principles* and the usual Spanish translations of Marx's *Critique of the Gotha Programme*. *Why:* the terms should be the ones Spanish readers of the book and of Marx already know. → [Glossary](glossary.md)
- **43. Housing is out of scope.** **Decision:** the simulation uses existing housing. Dwellings are there from the start; no unit runs them, and they carry no hours and no wear in the books. *Why:* the book does not say how housing is provided, and it isn't needed to follow the shoe. → [Shoe scenario](shoe-scenario.md#units-buildings-and-functions), [Data model](data-model.md#building)
- **44. The working week.** Not in the brief. **Decision:** a full-time week is **32 hours**: four days of 8 hours. Units, the shoe factory included, run 8 hours a day, five days a week, Monday to Friday. The factory runs at capacity every day, so each full-timer's day off can fall on any weekday, spread evenly across the week: about four-fifths of a crew is at work every day. Some may choose to work all five days, and are credited for every hour. Part-time work is a 4-hour shift, morning or afternoon; part-timers may also work a fifth day. *Why:* the 40-hour week belongs to capitalist societies, where much of the work is useless. Without that work, the same production needs fewer hours each. With the book's figures, the shoe factory's 62,500 hours a year need about 39 people instead of 31. → [Shoe scenario](shoe-scenario.md#scale), [Data model](data-model.md#scenario-and-policies)
- **45. People are not always honest.** Not in the brief. People are lazy and opportunistic, and the simulation shouldn't assume otherwise. Wanted soon after the first builds, not in them. The kinds:
  - **Theft** of consumer goods from warehouses, distribution centres, the store, and vehicles in transit.
  - **Cooking the books.** A unit reports more hours than were worked, or less output than was made; a person claims hours not worked; care at home is recorded but not given (the weak point of [gap 8](#decided)); a stock count hides a loss.
  - **Shirking.** Feigned illness, credited at the usual hours ([gap 9](#decided)); working below one's pace while credited the full hour.

  The GIC's answer is that control "is guided by the public registration of the factual course of operational life. That is, production is controlled by reproduction" ([14 b](../../Documents/fundamental_principles/14b_The_Control_of_Operational_Life_II.md#b-control-under-communism)): a unit whose production time is well above its branch's average shows up in the books. It also admits that the control of public units "does not offer so many forms of automatic control": only their budget can be checked. The simulation can test both claims: what the books catch, how soon, and what they miss.

  **Decision:**
  - **Two records from phase 1.** The engine keeps what happened (the goods in each place, the minutes each person actually worked) apart from what was reported, and the books are written only from reports. Until dishonesty is switched on, the two agree. Adding the split later would mean reworking every system that writes the books.
  - **Opportunism.** Each person has a level drawn from the seed: most take small chances when they are unlikely to be seen, a few take large ones, some take none. Each kind of dishonesty is a policy with its own rate, off by default.
  - **Detection by the GIC's own means first:** a stocktake at the end of each period (book stock against what is there), each unit's production time against its branch's average, and each public unit against its budget. Inspectors and other bodies come later, if those miss too much.
  - **In the books,** goods found missing at a stocktake are written off as a loss, recorded against the unit so its figures show it. The loss is product no longer there for certificates to claim, so it comes off the top of the payout factor and lowers it for everyone.
  - What happens to someone caught is left open.

  → [Simulation engine](simulation-engine.md#dishonesty), [Data model](data-model.md#scenario-and-policies)

## Patrick's answers

His answers as he gave them, grouped by topic. A short note before each says what he was answering; one after says what came of it, so a change of mind can be followed.

### 2026-11-09: the first list of gaps

*Context:* answers by gap number to the first list of gaps and proposals. "Debate" is which reading of the 2026 German debate on paying for care work to follow.

> 1. The proposal is correct
> 2. My mistake. Use GIC
> 3. My mistake.
> 4. Good idea, use proposal
> 6. Yes, use the proposal
> 8. Home carer is paid as per the debate. Students... I'm not sure. Let's just say paid from 12 years old for now.
> 10. Correct, never change the pay. "A slower worker raises the unit's production time": that's correct. We want to see that in operation. It's a fact of life that some people are significantly faster than others... but very few are faster than a machine.
> 11. Buildings need hours too. Yes, new tech is out of scope.
>
> Debate: as per your interpretation of what was correct.

### 2026-11-10: gender and housing (gaps 31 and 43)

> Gender options: remove gender. It plays no part in this. Everyone's gender can be "not disclosed".
>
> 43. Housing: out of scope for now. We'll use existing housing for now.

### 2026-11-10: child carers (gap 8)

*Context:* gap 8 had decided that home carers are paid through a home care unit, with the carers working in their own homes.

> 8. Home carers: rename to child carers. Some child care can occur solely at a child care centre while parents work. Some carers may work part-time in industry, and the child goes to a care centre during those times. Some carers, likely very few, will do private care only. School, a form of child care in some ways, starts at 6.
>
> None of this is gendered. A man can do child care work. A trans woman can do it. Teachers could be male or female. We simply do not care. All that is required is that it is addressed correctly.

*Outcome:* a child care unit runs a child care centre and records carers' hours, at the centre or at home. School starts at 6.

> What is a typical minimum age for starting at a child care centre? Considering a rule: no full-time care under the age of 1 or something. The primary carer will be on "paid" leave until then. They still have the option of some part-time care, paid by the community, so they don't go insane. But there will be other full-time infant carers on leave.

*Context for the next answer:* Claude read "paid leave" as a payment from the social fund to someone not working, like the provision for those unable to work (gap 9), and asked how much it should pay.

> I meant "leave" from their workplace. They are full-time workers for the child's welfare. Set it to 1 year. We can easily beat all the capitalist countries. Don't sweat Marx too much; he missed things. Besides, it's necessary labour.

*Outcome:* the primary carer is a full-time child carer for the child's first year, credited a full working week, as labour. The centre takes infants part-time only.

### 2026-11-10: who makes the machines (gap 12)

*Context:* the proposal was that machines and buildings exist at the start, with hours given by the scenario.

> 12. Who makes the machines? Machine-building is a later chain.

*Outcome:* the proposal is decided.

### 2026-11-10: the working week (gap 44)

*Context:* the working week was not among the gaps.

> The working week: not covered in the gaps, but it should be addressed. The typical week in a capitalist society (with a huge number of people doing bullshit jobs) is 40 hours. Let's drop to 32. People could do 4 days at 8 hours a day. Let's assume the shoe factory operates for 8 hours a day and most people work 8 hours. 2 carers may work 4 hours, a morning or afternoon shift.

*Outcome:* a 32-hour week, and about 39 people in the shoe factory instead of 31. Claude assumed units run Monday to Friday, with each person's day off on a rota, and asked whether the factory should close on Fridays instead.

> Let's have the factory run 5 days a week. Some people may choose to work 5 days. Part-timers may be able to work the 5th day. We could stagger full-timers: some Mon–Thu, some Tue–Fri.

*Outcome:* Claude wrote in the two patterns, Monday to Thursday and Tuesday to Friday, and pointed out what they do to the crew: about 39 at work from Tuesday to Thursday, about 20 on Monday and Friday, with the machines partly idle on those days.

> Don't have Mon–Thu and Tue–Fri. The factory needs to run at capacity. People will have to have their extra day off on any day of the week.

*Outcome:* each full-timer's day off can fall on any weekday, spread evenly, so about 31 are at work every day and the factory runs at capacity.

### 2026-11-10: scale (gap 36)

*Context:* the one gap left that needed an answer: how many people the simulation must handle (hundreds, ten thousand, a million?), which decides the technology. The proposal was every person an agent up to about 10,000, with aggregates above that.

> Scale: somewhere around ten thousand

*Outcome:* about 10,000 people, every one an agent. The technology choice (TypeScript and PixiJS) stands; aggregate mode isn't built for now.

### 2026-11-10: shoes last (gap 18)

*Context:* the proposal was that each household holds consumer goods that wear out, which drives demand, plus a daily basket for everything else. It didn't say how long a pair lasts or what people own at the start.

> 18. Shoes last. They last one year. Everyone has a pair at the start of simulation of random age

*Outcome:* one pair per person, lasting a year; each pair's age at the start is drawn from the seed. The daily basket stays as proposed.

### 2026-11-10: expansion, large projects, the disaster fund (gap 19)

*Context:* the proposal was to leave them out while the scenario is simple reproduction, keeping their place in the payout factor.

> 19: correct, out of scope for now

*Outcome:* the proposal is decided.

### 2026-11-10: transport (gap 16)

*Context:* the proposal was that freight is costed and commuting is not, and that the brief's "operator" on Transport should be an operational unit.

> 16: freight is costed; commuting is not costed. Operator was supposed to be the person using the transport. I'd rather transport be a service that can be used by multiple operating units, on demand, using a queuing system. It needs to be very simple though, so can be owned by an operating unit.

*Outcome:* the operator is the driver. The freight unit owns the vehicles and serves a single queue of shipments from all units, first come, first served. Claude wrote that people walk the grid to work.

> Commuting: they don't have to walk. I don't care how they get to work. Walk, ride, scooter, car, bus, train, motorbike. Doesn't matter.

*Outcome:* the way people get to work is not modelled; they are shown moving along the grid, and the journey is not costed.

### 2026-11-10: people who do not work (gap 9)

*Context:* the proposal was a policy for each group (children, the retired, the ill and the injured), funded through the payout factor, with children consuming through their household.

> 9. People who do not work: I believe children are already fully catered for as part of child care.
> Retirement is an option from 65. Workers may opt for parttime work if they want. To be honest, parttime work should be an option for any age. If they can get by on less, that's fine with us. Full retirement needs to be a lower income. 20 hours garanteed maybe?
> Ill and injured: fulltime allowance. Some people have permanent disabilities and require special equipment. Out of scope that aspect for now. In general, we expect ill and injured to return to work as soon as fit.

*Outcome:* retirement is optional from 65, credited 20 hours a week; part-time work is open at any age; the ill and injured are credited a full week until fit. Hours credited without work go in the bottom line of the payout factor. Claude assumed a retired person who works part-time is credited the larger of their hours worked and the 20, and asked about it. Claude also asked whether an ill part-timer gets a full week or their usual hours.

> 1. The way you've written that it seems like there would be no incentive to work in "retirement". You get to 20 hours minimum. If you work 1 hour, you get 21 hours "pay". However, if you work 40 hours, you have not retired and you get 40 hours "pay". It no longer "pays" to retire at 32 hours. So you can work 12 hours to get up to the standard fulltime work.

*Outcome:* a retired person who works is credited their hours worked plus the 20, up to 32 a week. From 32 hours worked, they are credited their hours like anyone else. Claude pointed out that between 12 and 32 hours worked the credit stays at 32. Two questions were still open: what an ill part-timer is credited, and whether households get anything for each child, given that the GIC calls paying a worker with children the same as a single worker "a great injustice".

> 2. paid their usual hours.
> 3. Yes, it comes out of an adult's income. It is "a great injustice" though not as much as neo-Nazi trillionaires.

*Outcome:* the ill and injured are credited their usual hours. Children consume from the adults' certificates, with nothing extra per child, as in the book.

### 2026-11-11: internationalisation (gaps 39 to 42)

*Context:* the four proposals were translation keys in the data, Spanish roles named by trade or activity, the browser's `Intl` for numbers and dates, and Spanish terms checked against Spanish editions before they are fixed.

> Internationalisation: accept the 4 proposals

*Outcome:* all four are decided as proposed. Which Spanish to use (Spain's or a Latin American one) is still open in [Internationalisation](internationalisation.md#rules).

### 2026-11-11: repeatable runs (gap 35) and dishonesty (gap 45)

*Context:* gap 35's proposal was "one random stream per system, ordered iteration, integer arithmetic in the books", with absence among the random events.

> 35. A seed alone does not make a run repeatable: what does "one random stream per system" mean? A seed may not be sufficient but it is necessary. I think we have everything else for this point, right?
>
> You mention "absence". We will want to build-in theft of consumer items from warehouses and distribution centres, people trying to cook the books, etc. It does not need to be in the first builds, but we'll want it sooner than later. Humans are inherently lazy and opportunistic. Capitalists and other socialists are idealistic about that, but we don't need to be.

*Outcome:* gap 35's proposal now keys each draw by system, person and day, which goes further than one stream per system, and adds two conditions the list was missing: no browser maths functions in the engine, and nothing read from outside the run (the real clock, or unlogged commands). Dishonesty is a new open gap, 45. Its first consequence comes in phase 1: what happened and what was reported are kept apart from the start.

*Context for the next answer:* Claude explained that one shared stream lets a new module shift every later draw, and proposed going further than one stream per system: each draw keyed by system, person and day, so old seeds keep their other draws when modules or policies are added.

> One stream per system: you may have gone too far there. If we add a new module to the simulation, I don't care if the simulation plays out differently with an old seed. I only care about replay within the same build - at least for now.

*Outcome:* gap 35 is decided: one seeded generator for the whole engine, repeatable within the same build. The other conditions stay: ordered iteration, integers, no browser maths functions, nothing from outside the run. Claude pointed out the cost: comparing two policies needs several seeds, since with one stream a policy also changes who falls ill.

### 2026-11-11: the simulation (gaps 33, 34, 37, 38 and 45)

*Context:* the proposals under "The simulation": a one-minute tick with play starting at real time; integer seconds in the books, with a rounding rule; goods moved in batches; saving, loading and CSV export; and for dishonesty, two records (what happened and what was reported) from phase 1, opportunism drawn from the seed, and detection by the GIC's own means.

> Accept all proposals in "The simulation". That is: 33, 34, 37, 38, 45

*Outcome:* all five are decided as proposed. Dishonesty itself still comes after the first builds, but the two records are built in phase 1. What happens to someone caught is still open.

---

[↑ Plans](README.md)
