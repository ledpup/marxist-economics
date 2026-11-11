[↑ Plans](README.md)

---

# User interface

*Stub.* What the person using the simulation sees and does.

## The map

- Aerial, 2D, on a grid. Buildings are blocks with an icon for their kind; dwellings are smaller and clustered.
- **Links** between units: a line for each regular supply route, its width by hours carried in the last day or week.
- **Moving things:** vehicles carrying crates along the links; people as dots moving to and from work, however they travel (shown only when zoomed in).
- **Zoom and pan** with the wheel, pinch and drag. Detail appears with zoom: whole town → buildings and links → people and crates.
- The rest of the economy is a gate at the edge of the map.

## Selection

Click a building, vehicle, crate or person. A side panel shows:

| Selected | Panel |
| --- | --- |
| Building | Its unit and functions; the people there now and what each is doing; machines and their wear; stock, with hours per unit; the unit's books for today and the period |
| Vehicle | Its cargo, where from and to, the hours the leg is adding |
| Crate (batch) | Product, quantity, hours per unit split into f, c and l, where they came from |
| Person | Household, roles, skills and pace, today's activity, hours worked this week, certificates |
| Gate | What has come in and gone out, and the balance |

## Time

- Pause and play. The run starts at real time (1×).
- Speed: a range slider on a logarithmic scale, with faster and slower buttons that move it one stop. Stops: 1×, 10×, 60× (a minute a second), 600×, 3,600× (an hour a second), 86,400× (a day a second), and maximum. The current multiple is shown beside the slider.
- Step an hour, a day, to the end of the period.
- The date and time; the seed, with a button to restart from it or a new one.

## Views of the hours

The point of the simulation ([Plans](README.md#what-the-simulation-is-for)).

- **Hours on the move:** colour crates by hours per unit, or by f/c/l share.
- **A product's chain:** for a pair of shoes, a tree or flow diagram of where its hours came from, branch by branch.
- **Unit books:** the period's (f + c) + l, written out as the book does.
- **Branch table:** units, output, own figure, social average, over and under.
- **Fast and slow:** a crew's members with their pace, the minutes each batch took, the unit's hours per pair against the branch average, and everyone's certificates per hour, which stay the same.
- **Payout factor:** the formula with this period's numbers, showing what the school, child care, the retired and the ill take. A switch reruns the period with child care, students, retirement or sick pay unpaid, for comparison.
- **The loop:** a pair of shoes from factory to store to a household, and the household's worker back at the factory the next day, with the books showing where the hours stop.

## Other

- Language switcher (English, Spanish) that changes everything on screen without a reload ([Internationalisation](internationalisation.md)).
- Load and save scenarios and runs; export the books.
- Keyboard controls for time; colours that work for colour-blind users; works on a laptop screen first, a tablet later.

---

[↑ Plans](README.md)
