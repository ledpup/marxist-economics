[↑ Plans](README.md) · [Gaps in the brief](gaps-in-the-brief.md)

---

# Patrick's answers on the gaps

His answers as he gave them, grouped by topic. A short note before each says what he was answering; one after says what came of it, so a change of mind can be followed. The gaps themselves are in [Gaps in the brief](gaps-in-the-brief.md) (open) and [Decided gaps](gaps-decided.md).

## 2026-11-09: the first list of gaps

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

## 2026-11-10: gender and housing (gaps 31 and 43)

> Gender options: remove gender. It plays no part in this. Everyone's gender can be "not disclosed".
>
> 43. Housing: out of scope for now. We'll use existing housing for now.

## 2026-11-10: child carers (gap 8)

*Context:* gap 8 had decided that home carers are paid through a home care unit, with the carers working in their own homes.

> 8. Home carers: rename to child carers. Some child care can occur solely at a child care centre while parents work. Some carers may work part-time in industry, and the child goes to a care centre during those times. Some carers, likely very few, will do private care only. School, a form of child care in some ways, starts at 6.
>
> None of this is gendered. A man can do child care work. A trans woman can do it. Teachers could be male or female. We simply do not care. All that is required is that it is addressed correctly.

*Outcome:* a child care unit runs a child care centre and records carers' hours, at the centre or at home. School starts at 6.

> What is a typical minimum age for starting at a child care centre? Considering a rule: no full-time care under the age of 1 or something. The primary carer will be on "paid" leave until then. They still have the option of some part-time care, paid by the community, so they don't go insane. But there will be other full-time infant carers on leave.

*Context for the next answer:* Claude read "paid leave" as a payment from the social fund to someone not working, like the provision for those unable to work (gap 9), and asked how much it should pay.

> I meant "leave" from their workplace. They are full-time workers for the child's welfare. Set it to 1 year. We can easily beat all the capitalist countries. Don't sweat Marx too much; he missed things. Besides, it's necessary labour.

*Outcome:* the primary carer is a full-time child carer for the child's first year, credited a full working week, as labour. The centre takes infants part-time only.

## 2026-11-10: who makes the machines (gap 12)

*Context:* the proposal was that machines and buildings exist at the start, with hours given by the scenario.

> 12. Who makes the machines? Machine-building is a later chain.

*Outcome:* the proposal is decided.

## 2026-11-10: the working week (gap 44)

*Context:* the working week was not among the gaps.

> The working week: not covered in the gaps, but it should be addressed. The typical week in a capitalist society (with a huge number of people doing bullshit jobs) is 40 hours. Let's drop to 32. People could do 4 days at 8 hours a day. Let's assume the shoe factory operates for 8 hours a day and most people work 8 hours. 2 carers may work 4 hours, a morning or afternoon shift.

*Outcome:* a 32-hour week, and about 39 people in the shoe factory instead of 31. Claude assumed units run Monday to Friday, with each person's day off on a rota, and asked whether the factory should close on Fridays instead.

> Let's have the factory run 5 days a week. Some people may choose to work 5 days. Part-timers may be able to work the 5th day. We could stagger full-timers: some Mon–Thu, some Tue–Fri.

*Outcome:* Claude wrote in the two patterns, Monday to Thursday and Tuesday to Friday, and pointed out what they do to the crew: about 39 at work from Tuesday to Thursday, about 20 on Monday and Friday, with the machines partly idle on those days.

> Don't have Mon–Thu and Tue–Fri. The factory needs to run at capacity. People will have to have their extra day off on any day of the week.

*Outcome:* each full-timer's day off can fall on any weekday, spread evenly, so about 31 are at work every day and the factory runs at capacity.

## 2026-11-10: scale (gap 36)

*Context:* the one gap left that needed an answer: how many people the simulation must handle (hundreds, ten thousand, a million?), which decides the technology. The proposal was every person an agent up to about 10,000, with aggregates above that.

> Scale: somewhere around ten thousand

*Outcome:* about 10,000 people, every one an agent. The technology choice (TypeScript and PixiJS) stands; aggregate mode isn't built for now.

## 2026-11-10: shoes last (gap 18)

*Context:* the proposal was that each household holds consumer goods that wear out, which drives demand, plus a daily basket for everything else. It didn't say how long a pair lasts or what people own at the start.

> 18. Shoes last. They last one year. Everyone has a pair at the start of simulation of random age

*Outcome:* one pair per person, lasting a year; each pair's age at the start is drawn from the seed. The daily basket stays as proposed.

## 2026-11-10: expansion, large projects, the disaster fund (gap 19)

*Context:* the proposal was to leave them out while the scenario is simple reproduction, keeping their place in the payout factor.

> 19: correct, out of scope for now

*Outcome:* the proposal is decided.

## 2026-11-10: transport (gap 16)

*Context:* the proposal was that freight is costed and commuting is not, and that the brief's "operator" on Transport should be an operational unit.

> 16: freight is costed; commuting is not costed. Operator was supposed to be the person using the transport. I'd rather transport be a service that can be used by multiple operating units, on demand, using a queuing system. It needs to be very simple though, so can be owned by an operating unit.

*Outcome:* the operator is the driver. The freight unit owns the vehicles and serves a single queue of shipments from all units, first come, first served. Claude wrote that people walk the grid to work.

> Commuting: they don't have to walk. I don't care how they get to work. Walk, ride, scooter, car, bus, train, motorbike. Doesn't matter.

*Outcome:* the way people get to work is not modelled; they are shown moving along the grid, and the journey is not costed.

## 2026-11-10: people who do not work (gap 9)

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

## 2026-11-11: internationalisation (gaps 39 to 42)

*Context:* the four proposals were translation keys in the data, Spanish roles named by trade or activity, the browser's `Intl` for numbers and dates, and Spanish terms checked against Spanish editions before they are fixed.

> Internationalisation: accept the 4 proposals

*Outcome:* all four are decided as proposed. Which Spanish to use (Spain's or a Latin American one) is still open in [Internationalisation](internationalisation.md#rules).

## 2026-11-11: repeatable runs (gap 35) and dishonesty (gap 45)

*Context:* gap 35's proposal was "one random stream per system, ordered iteration, integer arithmetic in the books", with absence among the random events.

> 35. A seed alone does not make a run repeatable: what does "one random stream per system" mean? A seed may not be sufficient but it is necessary. I think we have everything else for this point, right?
>
> You mention "absence". We will want to build-in theft of consumer items from warehouses and distribution centres, people trying to cook the books, etc. It does not need to be in the first builds, but we'll want it sooner than later. Humans are inherently lazy and opportunistic. Capitalists and other socialists are idealistic about that, but we don't need to be.

*Outcome:* gap 35's proposal now keys each draw by system, person and day, which goes further than one stream per system, and adds two conditions the list was missing: no browser maths functions in the engine, and nothing read from outside the run (the real clock, or unlogged commands). Dishonesty is a new open gap, 45. Its first consequence comes in phase 1: what happened and what was reported are kept apart from the start.

*Context for the next answer:* Claude explained that one shared stream lets a new module shift every later draw, and proposed going further than one stream per system: each draw keyed by system, person and day, so old seeds keep their other draws when modules or policies are added.

> One stream per system: you may have gone too far there. If we add a new module to the simulation, I don't care if the simulation plays out differently with an old seed. I only care about replay within the same build - at least for now.

*Outcome:* gap 35 is decided: one seeded generator for the whole engine, repeatable within the same build. The other conditions stay: ordered iteration, integers, no browser maths functions, nothing from outside the run. Claude pointed out the cost: comparing two policies needs several seeds, since with one stream a policy also changes who falls ill.

## 2026-11-11: the simulation (gaps 33, 34, 37, 38 and 45)

*Context:* the proposals under "The simulation": a one-minute tick with play starting at real time; integer seconds in the books, with a rounding rule; goods moved in batches; saving, loading and CSV export; and for dishonesty, two records (what happened and what was reported) from phase 1, opportunism drawn from the seed, and detection by the GIC's own means.

> Accept all proposals in "The simulation". That is: 33, 34, 37, 38, 45

*Outcome:* all five are decided as proposed. Dishonesty itself still comes after the first builds, but the two records are built in phase 1. What happens to someone caught is still open.

## 2026-11-14: the designer (gap 14)

*Context:* the proposal was that the designer's hours are part of the shoe factory's l, like any other worker's, with a design as fixed means of production, spread over a run like a machine, as an option for later.

> "14. The designer's work is not used up in one pair." A designer is in some ways not part of the production process. In some factories, the designers may even be in another country. Having them as part of the factory is a good idea. They are likely to be involved in boutique lines of shoes. Most of the shoe production should involve creating a strong and duration shoe that most people will be happy with for everyday uses. Some consumers (and designers) have a particular interest in shoes. The designer will be involved in create these lines of shoes. They'll have a much higher labour time to produce, will be produced in lower numbers, may involve trainee cordwainers that come in on the weekends, and are producing for the love of shoes. Some consumers will be happy to sacrifice more of their vouchers in the interests of fashion.
>
> To have the designers labour as a fixed means of production is an interesting idea. That can work in the sense that the design work is done upfront, before production is done. That can apply for the mainline shoes. For boutique shoes, a designer may be making improvements and changes for their limited production runs.

*Outcome:* gap 14 is decided: the designer works in the factory; the mainline design is fixed means of production, worn per pair; on boutique runs the designer's hours go into the run's l. Boutique lines are a new open gap, 46, with proposals: trainees credited for their hours, the factory open at weekends for boutique runs, each boutique design its own product at its own production time, buyers chosen by an interest in shoes drawn from the seed, and the whole a later version of the scenario.

## 2026-11-14: trainees on the boutique lines (gap 46)

*Context:* gap 46 proposed that the factory opens at weekends for boutique runs, with trainees' weekend hours credited on top of their week elsewhere, like a fifth day.

> Trainees would not so much do a fifth day, but they could work on a different schedule. 2 days learning the mainline shoes production, 2 days doing botique to improve their skills, taking more time and care to do so. We would need some skilled people on that block as well. Those people would be those who aren't just doing it for the job. An optional route. Other people are just doing it as a job, to make ends meet.

*Outcome:* the weekend proposal is dropped. Trainees split their 32-hour week between the mainline and the boutique block; skilled cordwainers who choose the boutique route work alongside them; everyone else works the mainline. Two consequences are added to the proposal: trainees' skill and pace rise with their hours, and the mainline needs more people to cover the trainees' boutique days. Gap 46 stays open.

## 2026-11-14: joint products (gap 13)

*Context:* the proposal was that recipes mark each output as *main* or *by-product*.

> 13. Joint products inside the chain.
>
> The proposal is good. Is recipe the correct term to use here? I only think of it in terms of food, but I can see how it also could be used for shoe production. No more general suggestion?

*Outcome:* gap 13 is decided as proposed. Claude kept "recipe" for now and set out the alternatives, for Patrick to choose.

*Context for the next answer:* Claude said that "recipe" is the standard term in batch manufacturing (in tanning and rubber compounding too), that "bill of materials" covers only the inputs and "routing" only the steps and times, and offered "production method" as a plainer alternative.

> Keep recipe. You said it was a standard word. I accept that.

*Outcome:* "recipe" stays, and is added to the glossary.

## 2026-11-14: boutique lines (gap 46)

*Context:* Claude asked whether the designer also teaches on the boutique block, and whether skilled cordwainers split their week like the trainees or work the boutique block full-time.

> A designer would teach and design.
> Skilled corwainers' split like the trainees. A single cordwainer may do 0, 1 or two days of boutique.
> All of this is kind of provisional. Just trying to think about what cordwainers do and would like to do.
> I accept the proposal for 46.

*Outcome:* gap 46 is decided, marked provisional. The designer designs and teaches on the boutique block; any cordwainer works 0, 1 or 2 boutique days a week, trainees 2.

## 2026-11-14: mixed units (gap 15)

*Context:* the proposal was that the power station meters each consumer and splits its books: charged to units, free to homes.

> 15. mixed units. The proposal is correct. We need to include water too.

*Outcome:* gap 15 is decided as proposed, with a waterworks as a second mixed unit, run on the same rules. The waterworks' crew (3) and its figures are *invented*; its figures, like the power station's, are still to fill in.

## 2026-11-14: workers' democracy (gaps 47 and 48)

*Context:* not among the gaps. Patrick raised it, asking for a new page that contrasts the *Fundamental Principles* with *Towards a New Socialism*.

> Another gap, we probably need a new page for this, is on workers' democracy. We haev two economic models we could contrast, fundamental principles (our economic model) and TNS. Where I think we break with TNS is over "employment for all" and the lack of a sanction on firing. I can't see how a shop/factory controlled by a workers' council could function without the ability to fire someone. There are cases where that may be the only practical option. That doesn't prevent the worker from seeking work elsewhere.
>
> Many of the policies under the length of the working day, the length of the working week, artisan hours, shift work, fulltime/parttime policies, should be decisions made by the council.
>
> We need a section to compare trade unions with workers' councils and explain the reasons for selecting councils over trade unions.
>
> The reasons against "full employment" is that it seems a demand that is not necessary to accomplish the goals of a post-capitalist state. It is a totalitarian notion and one that obviously is not possible. Some people are born unable to work and there may be others that simply refuse to participate in social life. For the first group, they need to be supported regardless and for the later, if that is their choice, it should be respected, though they may soon realise how impractical such an existant actually is. The ideal of "a job for those that want one" is what we strive for.
>
> Much of this operates above the level of the economic structure, but it'll describe how people will organise social work.

*Outcome:* a new page, [Workers' democracy](workers-democracy.md). Gap 47 records his positions as decided. What happens after someone leaves a unit (how a dismissal is decided, appeal, credit while looking for work, finding a place) is a new open gap, 48, with proposals.

## 2026-11-14: other mixed units, and greenhouse gases (gaps 49 and 50)

> Are there other mixed units? The other main I can think of is gas. That would need to be put high on the list for fasttracked decommisoning. There is also roads, but they're probably public.

*Context for the next answer:* Claude proposed sewage with the waterworks, with the tannery charged for its effluent; waste collection as a later mixed unit; no gas in the town, with heat electric and gas decommissioning a later scenario; and roads public, existing and out of scope.

> I accept all those proposals. Good points on the sewage and waste treatment as costed as the price of production. I have a whole area for carbon emissions (and other GHG like N2O and ozone). Those are currently out of scope. I don't see how they could be added as production costs as there are currently no ways of treating those wastes. I had them down as more bookkeeping.

*Outcome:* gap 49 is decided as proposed. Gap 50 records greenhouse gases as out of scope and, when added, as a record beside the hours, as in the [carbon note](../../notes-opus5_5/carbon-and-labour-time.md). Claude added that work which removes carbon from the air would be labour, and costed.

## 2026-11-18: where the chain starts, and leather or synthetic (gaps 5 and 51)

*Context:* gap 5's proposal was that the scenario gives each product from outside a production time on arrival, taken from the shoe illustration or converted from money with the key number. Its list of inputs (hides, tanning chemicals) assumed a leather upper.

> Where the chain starts. We cannot convert from money because by "outside" we're not assuming a capitalist economy. This is a socialist/communist economy. Outside is something we are not tracking in the model (as yet). We will estimate their labour time.
>
> Those ingredients are assuming a leather upper. What is the split between synthetic uppers and leather? This will introduce a significant discussion with the operational units and beyond as to what basic ingredients to use. To begin with, everything used is what is used from the capitalist production system. But they will need to look at the carbon cost of leather vs synthetic as well as the welfare of cows. Cattle production produces large quantities of methane. They are the single worst source of meat. Can other animals be used? And synthetic uppers are by-products of the fossil fuel industry. All of this is out of scope for this simulation. However, we could have two types of shoe: synthetic and leather.

*Outcome:* gap 5 is decided. Production times from outside are estimates and are never converted from money. Claude gave the split: of the pairs traded worldwide in 2023, about 15 % had leather uppers, about 50 % rubber or plastic, and 29 % textile. Gap 51 is new and open. Choosing materials is out of scope. The proposal is that a later version makes a leather and a synthetic shoe, one pair in four leather by default. Gap 20 (day one) still names the key number for a scenario that starts from money figures; Claude asked whether that should go too.

*Context for the next answer:* the proposal for gap 51 had only two shoes, leather and synthetic, with textile left for later.

> 51. will need to have a textile shoe. They're a major category

*Outcome:* the proposal for gap 51 now has three shoes: leather, synthetic and textile. The default split follows the export figures: about one pair in six leather, one in two synthetic and one in three textile. Each product can have its own life. Gap 51 stays open.

*Context for the next answer:* the proposal had the synthetic and textile uppers arriving through the gate, with no chain behind them, and had left each kind's life to the scenario.

> For 51, offer those 3 types of shoe in the model. Discover a process where their input can come from. Give each a default lifespan. From my experience, leather lasts the longest. I'm not sure of the other two. I think 51 can then be decided, with parts of it marked out of scope.

*Outcome:* gap 51 is decided. Each upper has a chain: leather through the town's tannery; synthetic (polyurethane-coated fabric) from a coating works, and textile from a weaving or knitting mill, both through the gate. Default lives are leather 2 years, synthetic 1 year and textile 9 months, from retail and footwear-guide sources, which agree that leather lasts longest but give no firm figure for synthetics. These replace gap 18's single year. Which materials should be used, and repairs, are out of scope. The shoes still come in a later version, with consumer choice.

## 2026-11-19: day one is a conversion from money (gap 5 revised, gap 52)

*Context:* on 2026-11-18 gap 5 was decided as "outside is communist, estimated in hours, never converted from money".

> We need to revise the decided point 5. In chapter 17 b of Fundamental Principles, GIC do an initial conversion of money to working hours. It's a one-off conversion. Investigate this as the start point for the simulation. We'll estimate some dollar values, do a best guess for the working hours equivalent, and then go from there. It was never my intention to deviate from their suggestion. We need to explore this avenue first. That means there is an "outside", explicitly acknowledged.

*Outcome:* gap 5 is revised: the simulation starts from money books converted once by the key number, and the gate is the explicit outside. The new page [The key number](key-number.md) sets out what 17 b and 17 c say, a first estimate (default $60 an hour, 0.01667 hours a dollar) from three routes, and dollar figures for the shoe scenario, all marked as estimates. Gap 20 (day one) takes the key number as its method. Gap 52 is new and open: what the gate does after day one, and whether the outside keeps trading in money.

> After day one, we don't use money (your proposal). The $60 is just a variable default? It's fine. Can change that later if we want. I'm not concerned too much about variables. The equations and the logic need to be correct. We stick with the book as much as possible. If it's missing something or is incorrect, that's something important to investigate.

*Outcome:* gap 52 is decided as proposed: the gate keeps the day-one hours and money is not used again. The $60 an hour is a variable default. Where the book is silent or wrong, that is recorded as a finding to investigate.

> I accept the proposal on number 20.

*Outcome:* gap 20 is decided as proposed: opening books in money, converted once by the key number.

> Accept 17 as well. A pull system. Is this system to JIT?

*Outcome:* gap 17 is decided as proposed. Claude answered that it is a pull system, but not strictly just-in-time: the targets are buffers.

## 2026-11-19: the payout factor at scale (gap 7)

> Number 7: payout factor. Is it accurate to say this equation is the most involved? You said it is done every year. What made you decide that? The book shows two forms, one with productive units and then one with mixed units added. And there is the new variable H. How does this function work in a large economy? We need all the hours for all the operational units, productive, public, mixed? Does it get calculated for a region? Wouldn't that be fraught as some regions have more technology and resources? Does it then need to be done for the whole world? Can that work? There are 8 billion people on the planet. How many are working? 4 billion? Estimate how many operational units we'd have at that scale. Can the equation be calculated at the regional level and then be combined between regions? Does that work mathematically or have we made it nonsense by losing information?

*Outcome:* a new note, [The payout factor at the scale of a world](../../notes-opus5_5/payout-factor-at-scale.md). Claude's answers: the equation is not the most involved, only the most far-reaching; the year was not the book's decision (it is the thought experiment's), so the period is ours; the book has three forms (with expansion), not two; regions combine exactly if they report N and D and not factors. About 3.5 billion work; operational units number tens of millions. Open in the book: how far the pool reaches, how wide the social average is, and resources. Gap 7 is still open, with its proposal reworded.

---

[↑ Plans](README.md) · [Gaps in the brief](gaps-in-the-brief.md)
