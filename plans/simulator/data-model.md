[↑ Plans](README.md)

---

# Data model

The abstract model the simulation runs over. It is independent of language and storage: the [technology](technology.md) plan decides how it is held in memory. The brief's components are all here, reworked where the [gaps](gaps-in-the-brief.md) call for it. New entities are marked *new*.

## Principles

- **Four layers.**
  - *Definitions*: the catalogue, fixed for a scenario (roles, products, functions, machine types, branches).
  - *The world*: what exists and changes (people, units, buildings, machines, batches, vehicles).
  - *The books*: an append-only record of what happened (work, transfers, certificates, purchases).
  - *Policies*: the rules a scenario chooses (payout factor timing, who is paid, joint-product method).
- **Ids** are stable strings in scenario files (`role.cordwainer`, `bld.tannery`) and small integers at run time.
- **Names are translation keys** for anything defined by the scenario (`role.cordwainer` → "Cordwainer" / "Zapatero"). People's names are plain text. See [Internationalisation](internationalisation.md).
- **Hours are fixed-point** (integer micro-hours), never floating point. See [Accounting](accounting.md#numbers).
- **Every quantity of hours keeps its split** into f, c and l, so the screen can always show where a product's hours came from.

## Overview

```
DEFINITIONS                         THE WORLD                               THE BOOKS
                                    
Branch ◄──── Product ◄─────────────── Batch (qty, f/c/l hours, place)        Account (per unit, per household)
               ▲  ▲                     ▲                                      ▲
               │  └── Recipe in/out ─┐  │ made / used by                       │ entries
MachineType    │                     │  │                                      │
   ▲           │     Function ◄──────┴── Building ──── OperationalUnit ────── Transfer (unit → unit)
   └── Machine ┼──── (needs roles,         │  (grid cell,     │ (productive/    WorkLog (person, hours)
       (hours, │      machine types)       │   footprint)     │  public/mixed)  CertificateIssue
        life)  │                           │                  │                 Purchase (household → store)
Role ◄─────────┼──── Skill ◄── Person ─────┼── Employment ────┘
               │               │  └── Household ── lives in ── Building (dwelling)
VehicleType ◄──┴── Vehicle ── owned by the freight unit, driven by a Person; carries Shipment (Batch, from → to)
```

## Definitions

### Role

From the brief. A kind of work.

| Field | Notes |
| --- | --- |
| id, nameKey | `role.cordwainer`. In Spanish, named by the trade or activity, not the person: see [Internationalisation](internationalisation.md#job-titles) |
| kind | `productive`, `public`, `care` (child carer), `study` (student). Decides what policy applies to certificates |

### Branch

*New.* All units that make the same product. Needed for the social average.

| Field | Notes |
| --- | --- |
| id, nameKey | `branch.footwear` |
| products | The products whose social average this branch keeps |

### Product

The brief's "Consumable", widened. A *kind* of thing; quantities of it are [batches](#batch).

| Field | Notes |
| --- | --- |
| id, nameKey | `prod.upper-leather` |
| unit | `pair`, `m2`, `kg`, `m`, `kWh`, `box`, `basket` |
| category | `circulating` (raw material, consumable: c), `fixed` (machine, building: f), `consumer` (for households), `service` (freight, electricity, which are used as they are made) |
| branch | Which branch's social average applies |
| initialHoursPerUnit | Production time on day one, before the books have any history. Split into f/c/l where known |
| wearDays | Consumer durables only: how long it lasts in use. Shoes: 365 days ([gap 18](gaps-in-the-brief.md#decided)) |

### Function

From the brief ("braiding works", "thread works"), with the recipe it was missing. A production process that a building can host.

| Field | Notes |
| --- | --- |
| id, nameKey | `fn.cutting` |
| inputs | List of (product, quantity per batch) |
| outputs | List of (product, quantity per batch, `main` or `byProduct`). See [the by-product method](accounting.md#joint-products-the-by-product-method) |
| crew | List of (role, people, minimum skill level) |
| machines | List of (machine type, count) |
| machineMinutes, handMinutes | Time per batch. Machine time runs at the machine's pace, whoever tends it. Hand time runs at the crew's [pace](#skill): a fast worker can halve it, but no one makes the machine go faster |
| energy | kWh per batch |

### MachineType

*New*, split from the brief's Machine.

| Field | Notes |
| --- | --- |
| id, nameKey | `mt.sewing-machine` |
| productionHours | Hours embodied in one machine |
| lifeHours | Hours of use before it is worn out. f per hour of use = productionHours ÷ lifeHours |
| breakdownRate | Chance per hour of use; uses the random stream for breakdowns |

### VehicleType

*New.* Like MachineType, plus speed and capacity.

| Field | Notes |
| --- | --- |
| id, nameKey, productionHours, lifeHours | As for MachineType (life in hours of driving) |
| speed | Cells per simulated minute |
| capacity | Batches, or volume |
| energy | kWh or fuel per cell travelled |

## The world

### Location

From the brief, changed from latitude and longitude to the grid.

| Field | Notes |
| --- | --- |
| x, y | Grid cell |
| lat, long | Optional. For placing the grid on a real map later |

### OperationalUnit

From the brief. The body that keeps the books and holds the right of disposal.

| Field | Notes |
| --- | --- |
| id, name | Name is plain text (units have proper names), or a key for generic ones |
| type | `productive`, `public`, `mixed`. Not "private": see [gap 2](gaps-in-the-brief.md#decided) |
| branches | For productive units. A unit can make products of several branches (the components works makes soles, thread and laces); it keeps its books per product |
| buildings | One or more. The unit's location is that of its buildings |
| account | Its books |
| publicBudget | Public units: hours a period, set by the scenario (GSW budget) |

Its employees come from [Employment](#employment), not a list on the unit.

### Building

From the brief.

| Field | Notes |
| --- | --- |
| id, name | |
| unit | The operational unit that runs it. Dwellings have none: they are existing housing, outside the books for now, with no hours and no wear ([gap 43](gaps-in-the-brief.md#decided)) |
| location, footprint | Grid cell of the top-left corner; width × height in cells |
| kind | For drawing only: `dwelling`, `works`, `store`, `public`, `depot`, `power`, `gate` (the edge of the map) |
| functions | Functions it hosts, each with a number of workstations |
| machines | Machine instances in it |
| stock | Batches held, with a storage capacity |
| capacity | Separate limits: residents (dwellings), workers on shift, storage |
| productionHours, lifeYears | Buildings wear too: part of f |

### Machine

From the brief.

| Field | Notes |
| --- | --- |
| id, type | |
| building, function | Where it stands and what it is used for |
| hoursUsed | Running total. Wear charged so far = hoursUsed × productionHours ÷ lifeHours |
| state | `idle`, `working`, `broken`, `worn out` |

### Batch

*New.* A quantity of one product in one place. Replaces the brief's "consumables" list on buildings.

| Field | Notes |
| --- | --- |
| product, quantity | |
| hours | Production time per unit, split into f, c and l |
| hoursBasis | `own` (this unit's figure) or `social` (the branch average it was passed on at) |
| place | A building's stock, a vehicle, or a household |
| madeBy, madeOn | Unit and date, for the panel |
| sources | Optional: hours by source branch, for showing a product's chain. Kept per batch, not per item |

### Person

From the brief.

| Field | Notes |
| --- | --- |
| id, name | Plain text, not translated |
| birthDate | Age is derived from the simulation's date |
| retired | From 65, by choice ([gap 9](gaps-in-the-brief.md#decided)); at the start, drawn from the seed |
| illness | Current illness or injury, if any: start, expected end. Drawn from the seed |
| household | Replaces "residence": the household lives in a dwelling |
| skills | List of [Skill](#skill) |
| employments | List of [Employment](#employment). Replaces "employer(s)" |
| activity | What they are doing now: `home`, `travelling`, `working` (with function), `shopping`, `studying`, `atChildCare` (a child under 6 at the centre), `caring`, `absent`. For the selection panel |
| position | Building, or a grid position while travelling |

### Skill

*New.* Replaces the brief's "roles (id, skill level, …)".

| Field | Notes |
| --- | --- |
| person, role | |
| level | Which functions a person may do |
| pace | How fast they work by hand, as a multiple of the average (from about 0.6 to 1.6), drawn from the seed; it can rise with experience. A slower crew raises the unit's production time. **Never** changes certificates: see [gap 10](gaps-in-the-brief.md#decided) |

### Employment

*New.* Replaces "employer(s)" and the hours on the role.

| Field | Notes |
| --- | --- |
| person, unit, role | |
| place | The building where the work is done. Usually the unit's own; a child carer caring at home works in their own dwelling ([gap 8](gaps-in-the-brief.md#decided)) |
| hoursPerWeek, shift | Full time is 32 hours ([gap 44](gaps-in-the-brief.md#decided)). Anyone of working age may choose part-time ([gap 9](gaps-in-the-brief.md#decided)). Shift: start time and days. A child carer who also works part-time in a productive unit has two employments |
| from, to | Dates |

### Household

*New.*

| Field | Notes |
| --- | --- |
| id, dwelling | |
| members | People |
| account | Pooled labour certificates |
| holdings | Consumer goods in use: one pair of shoes per member, each with its owner and the day it came into use ([gap 18](gaps-in-the-brief.md#decided)). At the start, each pair's age is random, from the seed |
| basket | Daily needs from the rest of the economy: food, heat and the like, as a product in hours |

### Vehicle

The brief's Transport, split into type and instance.

| Field | Notes |
| --- | --- |
| id, type | |
| unit | The freight unit that owns it ([gap 16](gaps-in-the-brief.md#decided)) |
| location, route | Current cell, and the cells ahead. Routes are straight lines or simple grid paths, not traffic |
| cargo | Shipments |
| driver | A person, employed by the freight unit (the brief's "operator") |
| hoursUsed | For wear, as for machines |

### Shipment and Order

*New.*

| Entity | Fields |
| --- | --- |
| Order | From unit, to unit, product, quantity, date wanted, status |
| Shipment | Order, batch, from building, to building, requested, vehicle, departed, arrived. Status: `queued` (waiting in the freight queue), `loaded`, `delivered` |

## The books

Append-only. See [Accounting](accounting.md) for what each one means.

| Record | Fields |
| --- | --- |
| Account | Owner (unit or household), balances: withdrawn from the community, transferred to the community, certificates held |
| WorkLog | Person, unit, function, start, minutes worked |
| Transfer | Direct transfer between units: date, from, to, batch, quantity, hours (f/c/l) |
| WearEntry | Machine or building, unit, date, hours of f charged |
| CertificateIssue | Person, household, period, hours worked, hours credited without work and why (retired, ill), payout factor, certificates issued |
| Purchase | Household, store, product, quantity, hours |
| PeriodClose | Period, branch social averages, each unit's over or under, payout factor |

## Scenario and policies

A scenario is one file (JSON or YAML) holding the definitions, the starting world and the policies.

| Field | Notes |
| --- | --- |
| seed | For the random streams |
| startDate, clock | Tick length, working day, week, accounting period |
| definitions, world | As above |
| policies.payoutFactor | `fixed` (a value), or `previousPeriod` (computed and reconciled) |
| policies.jointProducts | `byProduct` (the brief's choice); others possible later |
| policies.roles | Per role kind: `paid` or `unpaid`, and from what age. Default ([gap 8](gaps-in-the-brief.md#decided)): child carers paid as public work for hours recorded by the child care unit, at the centre or at home, within its budget; students paid from age 12 |
| policies.workingWeek | Full-time hours a week (default 32: four days of 8), the days units run (default Monday to Friday), the full-time pattern (default four days, with the day off spread evenly over the week, and a five-day option) and part-time shift lengths (default 4 hours, morning or afternoon) |
| policies.nonWorkers | Default ([gap 9](gaps-in-the-brief.md#decided)): children through child care, school and their household; retirement a choice from age 65, credited 20 hours a week on top of any hours worked, up to a full week (32) in all; the ill and injured credited their usual hours; anyone permanently unable to work, a full week. Nothing extra per child. Each can be switched off |
| policies.childCare | Under 1: the primary carer is a full-time child carer, credited a full working week; the centre takes the child part-time only, up to the hours a week set here. From 1: the centre full-time, or a carer at home. From 6: school ([gap 8](gaps-in-the-brief.md#decided)) |
| policies.commuting | `notCosted` in phase 1 |
| keyNumber | Optional: converts a scenario's money figures to hours ([E11](../../notes-opus5_5/fundamental-principles-economic-model.md#e11-the-key-number-converting-money-to-hours)) |

Runs can be saved (scenario plus current state plus books) and the books exported as CSV.

---

[↑ Plans](README.md)
