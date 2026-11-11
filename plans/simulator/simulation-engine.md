[↑ Plans](README.md)

---

# Simulation engine

*Stub.* The module that advances the [data model](data-model.md) through time and writes the [books](accounting.md).

## Shape

- **Headless.** No drawing, no browser APIs. It runs in a Web Worker in the app, and in Node for tests and batch runs.
- **One entry point:** `step(state, ticks) → events`. The user interface sends commands (pause, speed, select) and receives events and snapshots. It never changes the state directly.
- **Systems** run in a fixed order each tick (see below). Each reads and writes its own part of the state.

## The clock

- One tick is one simulated minute.
- The day, week, and accounting period (month, year) are set in the scenario.
- The tick sets the resolution of simulated time, not the speed of play. Speed is a multiple of real time, set in the user interface ([Time](user-interface.md#time)): from paused and 1× (real time, the default) up to as fast as the engine can run. At 1× a tick passes every real minute, and the map interpolates movement between ticks so people and vehicles still move smoothly. At high speed nothing is animated; only totals update.
- Step controls: one hour, one day, to the end of the period.

## Systems, in order each tick

1. **Schedule.** Starts and ends shifts; decides absences at the start of a day. Illness and injury start at random and last a random time; the person is credited their usual hours while off and goes back to work when fit ([gap 9](gaps-in-the-brief.md#decided)).
2. **People.** Moves each person along their day: home → work, school or child care centre → store → home. A child under 1 stays with their primary carer, with some part-time hours at the centre. From 1 to 5, a child goes to the centre while the adults who care for them work, or stays at home with a child carer; from 6, children go to school. Child carers work their shifts at the centre or at home. Commuting is shown but not costed.
3. **Production.** Each function with its crew present, its machines working and its inputs in stock advances its current batch.
4. **Demand and orders.** Units and the store reorder.
5. **Logistics.** Assigns shipments to vehicles; moves vehicles; unloads.
6. **Consumption.** Households wear their goods, draw their basket, shop.
7. **Accounting.** Records work, wear and transfers as they happen; issues certificates weekly; closes periods.
8. **Events.** Collects what changed for the user interface.

## Production

- A function works in **batches** (a crate of 20 pairs), not single items.
- A batch needs its crew (roles, minimum skill), its machines (not broken) and its inputs (taken from the building's stock at the start).
- Time per batch is the recipe's machine time plus its hand time divided by the crew's pace. Each person's pace is set at the start from the seed, with a small daily variation, and can rise with experience. A fast crew shortens the hand work, but never the machine time ([gap 10](gaps-in-the-brief.md#decided)).
- The minutes actually worked go to the work log. A slower crew therefore raises the batch's l, while each worker is still credited hour for hour.
- Finished batches go to the building's stock, ready for the next function or for shipping. Moves inside a building are not transfers.
- Joint outputs are marked main or by-product ([Accounting](accounting.md#joint-products-the-by-product-method)).

## Demand and orders

- **Pull.** The store keeps a target stock of each product; when it falls below, it orders from the unit that makes it. Each unit does the same for its inputs.
- Orders to the rest of the economy are always filled, after a lead time.
- When the store runs out, households queue, first come first served. The book does not say how shortages are handled ([What the book leaves open](../../notes-opus5_5/fundamental-principles-economic-model.md#what-the-book-leaves-open)).
- *Later:* a production plan from the congress of workers' councils, as an alternative policy.

## Logistics

- Transport is a service any unit can call on, on demand ([gap 16](gaps-in-the-brief.md#decided)). When a batch is ready to go, the sending unit puts a shipment in a single queue shared by all units. The freight unit owns the vehicles and serves the queue first come, first served, as vehicles come free. The shipment waits at the sender until then.
- Kept very simple: no priorities, no grouping of loads, no route planning.
- Vehicles move in straight lines or along simple grid paths at their speed. No traffic, no road network in phase 1.
- On arrival, the goods and the freight leg are two direct transfers ([Accounting](accounting.md#direct-transfers)).

## Random numbers and determinism

The same build, scenario and seed give the same run. Runs from different builds need not match ([gap 35](gaps-in-the-brief.md#decided)).

- One seed in the scenario, and **one seeded generator** for the whole engine, with a fixed algorithm (for example PCG32 or xoshiro128\*\*).
- People, units and buildings are always processed in id order. No iteration over hash maps whose order can vary.
- Integers in the books ([Accounting](accounting.md#numbers)) and in everything that feeds them: pace in thousandths, durations in whole minutes. No `Math.random`, `Math.log`, `Math.exp` or `Math.pow` in the engine; their last digits can differ between browsers. Floating point is allowed only for positions on screen.
- The engine never reads the real clock. Play speed changes how often the interface calls `step`, not what a step does. Commands given during a run are logged with their tick.
- Test: the same scenario and seed give the same hash of the state after a year ([Testing](testing.md#determinism)).

## Dishonesty

*Later, soon after the first builds* ([gap 45](gaps-in-the-brief.md#decided)). Theft, cooking the books and shirking, each a policy, off by default.

- **From phase 1**, the engine keeps what happened (goods in each place, minutes actually worked) apart from what is reported, and the books are written only from reports. With dishonesty off, the two always agree; a test checks it.
- A person's opportunism, drawn from the seed, and the chance of being seen decide whether they take an opportunity.
- Detection: a stocktake at the end of each period, each unit's production time against its branch's average, and each public unit against its budget ([14 b](../../Documents/fundamental_principles/14b_The_Control_of_Operational_Life_II.md#b-control-under-communism)).

## Performance

- State held as arrays of plain numbers per field (structure of arrays), not as objects per person, once numbers reach the thousands.
- People who are at home or at work do nothing between their events: schedule the next event rather than check every tick.
- The target is about 10,000 people, every one an agent ([gap 36](gaps-in-the-brief.md#decided)). Past that, whole units could switch to aggregate mode: a crew is a count, not people. Not built for now.

## Saving

- Save: scenario, current state, books. Load restores the run exactly, including the generator's state and the log of commands given during the run.
- Export the books as CSV.

---

[↑ Plans](README.md)
