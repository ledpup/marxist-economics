[↑ Notes and research](../README.md#on-towards-a-new-socialism)

---

# The economic model of *Towards a New Socialism*

A guide to W. Paul Cockshott and Allin Cottrell's proposal for a planned economy run on labour time, drawn out of *[Towards a New Socialism](../Documents/towards_a_new_socialism/README.md)* (1993; this text is the 2000 Swedish edition) without the history and the polemic. It sorts the chapters, defines the Marxist terms and the book's own vocabulary, sets out every equation with its terms, and collects what the book says about unskilled labour, unemployment, dismissal, students, youth, retirement, illness and disability, and child care. It then asks whether the book's case for computerised central planning opens a back door to Leninism, Trotskyism or Stalinism. The last section puts the proposal together as a conceptual model.

This is a research note by Claude (Opus 5.5), written from a brief by Patrick. Points marked *my reading*, *my calculation* or *my illustration* are interpretation, arithmetic or construction, not something the book says. Quotations keep the book's British spelling. The note doesn't compare the book with the GIC's *Fundamental Principles*; that is left for a separate note.

## Summary

- **The proposal in one paragraph.** All means of production that people work collectively belong to one public body, which the book calls Planning. Everyone works for "society", not for an enterprise, and is paid one labour token per hour worked. Tokens don't circulate: they are cancelled when spent, can't be transferred to another person, and expire. Every product carries its labour value, the hours needed to make it directly and indirectly, computed by computer from an input–output table. Producer goods are never sold; Planning allocates them. Consumer goods are sold for tokens at prices that clear the market. Where the price runs above the labour value, Planning makes more; where it runs below, less. A flat tax of so many tokens per worker pays for health, education, child care, investment and the incomes of people who can't work. The big shares of the budget are set by popular vote, in hours per week. Planning itself is supervised by juries chosen by lot, not by a government.
- **The model is in chapters 2, 3, 6, 7, 8, 9 and 14, with parts of 4, 5, 10, 12 and 13.** The introduction, chapter 1, chapter 11 and chapter 15 are mostly diagnosis, history and polemic (see [Which chapters to read](#which-chapters-to-read)).
- **The book uses Marx's categories openly** (labour value, exploitation, *c*, *v* and *s*, surplus product, simple and skilled labour) and adds three vocabularies of its own: computing (input–output, iteration, time order), control theory (feedback, the "harmony" function) and Athenian democracy (lot, juries, the assembly). The token has eight names in the book; see [What the token is called](#what-the-token-is-called).
- **There are 25 equations or formal rules.** The core ones are the labour-value equations (ch. 3), the gross-output equations g = Ag + f (ch. 6), the labour-time national accounts (ch. 7) and the marketing rule (ch. 8). Every one is set out with its terms in [The equations](#the-equations).
- **On work and welfare**, the book promises work for everyone but no right to any particular job. It pays students a wage, treats skilled labour as a "produced input" that costs society more but earns its holder no more, and pays non-workers out of the flat tax. It says much less about illness and disability than about unemployment, and nothing about injury at work under socialism. Child care is a citizenship right, provided by the state or by communes, never paid to parents at home.
- **On Leninism** (*my reading*): the book doesn't hide its sympathies. It says plainly that "Soviet society was indeed socialist", and it keeps the Soviet economic core: one owner of all productive property, central allocation of producer goods, and a state monopoly of finance and foreign trade. It also rejects the Leninist political forms outright: the vanguard party in power, the soviets, "democratic centralism" and elections. In their place it puts sortition and referenda. So the risk isn't a hidden Leninist party. It is that the book specifies a highly centralised economy in detail, and the democracy meant to control it only in outline, and leaves no independent organisation (parties, unions, strikes, workers' councils) through which workers could resist that centre. Computation answers the objection that planning is impossible. It doesn't decide who controls the plan. See [A back door to Leninism?](#a-back-door-to-leninism).

## Which chapters to read

### The model

| Chapter | What it adds to the model |
| --- | --- |
| [2. Eliminating Inequalities](../Documents/towards_a_new_socialism/02_Eliminating_Inequalities.md) | Pay in labour tokens, one per hour; what Marx's certificates imply (no circulation, no transfer, cancelled on use, expire); grades A, B and C of labour; skilled labour as a "produced input", with the appendix's multiplier. The tables of 1997 British earnings are illustration. |
| [3. Work, Time and Computers](../Documents/towards_a_new_socialism/03_Work_Time_and_Computers.md) | Why cost in labour time, not money; how to compute labour values from an input–output table; why the computation is feasible (iteration on a sparse table); how enterprises get values over the network. |
| [4. Basic Concepts of Planning](../Documents/towards_a_new_socialism/04_Basic_Concepts_of_Planning.md#levels-of-planning) | Planning as feedback control; the first-order goals; the three levels: macroeconomic, strategic, detailed. |
| [5. Strategic Planning](../Documents/towards_a_new_socialism/05_Strategic_Planning.md) | Industrial structure; the environment decided by referendum, not by formula; the discount rate; which goods are free, which sold, which tolled; agriculture by tender. |
| [6. Detailed Planning](../Documents/towards_a_new_socialism/06_Detailed_Planning.md) | From final targets to gross outputs (g = (I − A)<sup>−1</sup>f); stock and labour constraints; the "harmony" algorithm for adjusting targets. "Planning in the USSR" and "Economic cybernetics in Chile" are history and illustration. |
| [7. Macroeconomic Planning and Budgetary Policy](../Documents/towards_a_new_socialism/07_Macroeconomic_Planning_and_Budgetary_Policy.md) | National accounts in labour time; transfers to non-workers; saving, credit and retirement assets; the flat tax; ground rent; excise; accumulation by plebiscite. The core of distribution. |
| [8. The Marketing of Consumer Goods](../Documents/towards_a_new_socialism/08_The_Marketing_of_Consumer_Goods.md) | The marketing algorithm: market-clearing prices, the price-to-value ratio, the decision rule. |
| [9. Planning and Information](../Documents/towards_a_new_socialism/09_Planning_and_Information.md) | Product codes, stock control, message standards; how to get honest technical data; judging enterprises; no bonuses; workers have no right to a particular job. |
| [10 (from "International trade in context of socialism"). Foreign Trade](../Documents/towards_a_new_socialism/10_Foreign_Trade.md#international-trade-in-context-of-socialism) | Imports paid in labour credits; the rule for what to import and export; the five trade budgets. The first half of the chapter is Ricardo's theory and the capitalist world market. |
| [11, "What we advocate". Trade Between Socialist Countries](../Documents/towards_a_new_socialism/11_Trade_Between_Socialist_Countries.md#what-we-advocate) | One international plan instead of trade between socialist states. The rest of the chapter is Soviet history. |
| [12. The Commune](../Documents/towards_a_new_socialism/12_The_Commune.md) | Voluntary urban communes of 50 to 200 adults; internal work-units; the commune accounts. |
| [13, from "Is democracy possible today?". On Democracy](../Documents/towards_a_new_socialism/13_On_Democracy.md#is-democracy-possible-today) | Votes on television, juries chosen by lot, budget votes in hours per week, the "acephalous" state. The first half is Aristotle against parliaments and Lenin. |
| [14, "The proposed communalist model". Property Relations](../Documents/towards_a_new_socialism/14_Property_Relations.md#the-proposed-communalist-model) | Planning as sole owner, projects without legal personality, the employment agency, self-employment, ground rent, the Environment Trust. The 0–15 scale of property rights (earlier in the chapter) is the tool used to state it. |
| [15, "Distribution, values and prices"](../Documents/towards_a_new_socialism/15_Some_Contrary_Views_Considered.md#distribution-values-and-prices) | A three-point summary of the consumer market, and why a "scalar" allowance needs prices. |

### Diagnosis, history and polemic (skip)

| Chapter | What it is |
| --- | --- |
| [Preface](../Documents/towards_a_new_socialism/00a_Preface_to_the_Swedish_Edition.md) | The 2000 update. Admits the book doesn't say how to get from here to there. |
| [Introduction](../Documents/towards_a_new_socialism/00b_Introduction.md) | The authors' case that the USSR was socialist, and what they take from its failure. Read "[In what sense was the USSR socialist?](../Documents/towards_a_new_socialism/00b_Introduction.md#in-what-sense-was-the-ussr-socialist)" for the Leninism question; skip it for the model. |
| [1. Inequality](../Documents/towards_a_new_socialism/01_Inequality.md) | Capitalism's six sources of inequality, with British figures for 1997. The sections on unemployment, old age and the domestic economy set up later answers. |
| 6, "[Planning in the USSR](../Documents/towards_a_new_socialism/06_Detailed_Planning.md#planning-in-the-ussr)" and "[Economic cybernetics in Chile](../Documents/towards_a_new_socialism/06_Detailed_Planning.md#economic-cybernetics-in-chile)" | Why Gosplan did badly; Stafford Beer's Cybersyn as a precedent. |
| 10, to "Advantages of trade deficits" | Ricardo, comparative advantage, low-wage competition, Kalecki on surpluses. Theory of capitalist trade. |
| 11, to "Less developed countries" | The USSR as an international state; Trotsky and Stalin on socialism in one country. |
| 13, to "Direct democracy or soviet democracy?" | Aristotle on democracy; the critique of soviets, Lenin's *State and Revolution* and democratic centralism. |
| 14, to "The enterprise as focus of contradictions" | Property rights in postwar Britain and the USSR. |
| [15, "Market socialism?"](../Documents/towards_a_new_socialism/15_Some_Contrary_Views_Considered.md#market-socialism) | Replies to Diane Elson and Abel Aganbegyan. |

## Terms

### Marxist terms

| Term | How the book uses it | Where |
| --- | --- | --- |
| Labour theory of value | Assumed, not argued: "human work is alone the source of value". The book sets aside whether it holds for market economies (ch. 10, note 1). | [1, Summary](../Documents/towards_a_new_socialism/01_Inequality.md#summary) |
| Labour value, labour content | The total hours, direct and indirect, needed to make a product. The two terms are used interchangeably. | [3, Defining labour content](../Documents/towards_a_new_socialism/03_Work_Time_and_Computers.md#defining-labour-content) |
| Exploitation | Wages buy less than the hours worked. Measured as *s*/*v*: 98 % in Britain in 1997. Under socialism the category "would not be applicable", since the surplus is disposed of democratically (ch. 2). | [1, Exploitation](../Documents/towards_a_new_socialism/01_Inequality.md#exploitation) |
| Constant capital *c*, variable capital *v*, surplus value *s* | Used only to measure capitalist Britain (Table 1.1). They don't appear in the socialist accounts, which use Current Labour and Depreciation instead. | [1, Exploitation](../Documents/towards_a_new_socialism/01_Inequality.md#exploitation) |
| Necessary product, surplus product | The product that maintains the workers and the means of production, and the rest (for non-producers and net investment). The book's test of a mode of production is how it extracts the surplus. Under socialism it must still be "extracted", by taxing tokens. | [Introduction](../Documents/towards_a_new_socialism/00b_Introduction.md#in-what-sense-was-the-ussr-socialist); [2](../Documents/towards_a_new_socialism/02_Eliminating_Inequalities.md#differential-payment-for-personal-qualities) |
| Mode of production | Capitalist, socialist and a "domestic" mode of production in the family, which exploits women. | [1, Women's economic subordination](../Documents/towards_a_new_socialism/01_Inequality.md#womens-economic-subordination) |
| Productive and unproductive labour | Public administration and finance are left out of productive employment in Tables 1.1 and 2.1. The Soviet accounts' "rather narrow" use of the distinction is criticised. | [1](../Documents/towards_a_new_socialism/01_Inequality.md#exploitation); [7](../Documents/towards_a_new_socialism/07_Macroeconomic_Planning_and_Budgetary_Policy.md) |
| Simple and skilled labour | Simple labour has only the baseline education; skilled labour embodies extra education and counts as a multiple of simple labour for planning, not for pay. Marx's *complex labour* under another name. | [2, Skilled labour as a 'produced input'](../Documents/towards_a_new_socialism/02_Eliminating_Inequalities.md#skilled-labour-as-a-produced-input) |
| Labour certificates | Marx's *Critique of the Gotha Programme* quoted as the model, and Marx's line that Owen's labour money "is no more 'money' than a theatre ticket is". | [2](../Documents/towards_a_new_socialism/02_Eliminating_Inequalities.md) |
| Commodity, commodity form | A good produced for exchange. In the proposal only consumer goods are sold, with "intermediate products never assuming the form of commodities". | [2](../Documents/towards_a_new_socialism/02_Eliminating_Inequalities.md); [2, Comparison with historically existing socialism](../Documents/towards_a_new_socialism/02_Eliminating_Inequalities.md#comparison-with-historically-existing-socialism) |
| Labour power | What the worker sells under capitalism; its sale is "the prelude to exploitation". In the proposal it can't be bought, because tokens can't be transferred. | [15, Diane Elson](../Documents/towards_a_new_socialism/15_Some_Contrary_Views_Considered.md#diane-elson-the-socialised-market); [14](../Documents/towards_a_new_socialism/14_Property_Relations.md#individual-property-rights) |
| Absolute and relative surplus value | Named once, in the reply to Elson: lengthening the working day, and cheapening the means of subsistence. | [15](../Documents/towards_a_new_socialism/15_Some_Contrary_Views_Considered.md#diane-elson-the-socialised-market) |
| Use-value | Usefulness to consumers; the price-to-value ratio measures how well labour produces it. | [8](../Documents/towards_a_new_socialism/08_The_Marketing_of_Consumer_Goods.md) |
| Abstract social labour | A project's labour and materials, seen as a share of society's total labour. A council's economic power is, finally, "command over social labour". | [13, The acephalous state](../Documents/towards_a_new_socialism/13_On_Democracy.md#the-acephalous-state) |
| Reproduction schemes | Marx's model national accounts in *Capital* II, as the root of Gosplan's balances and Leontief's input–output table. | [1](../Documents/towards_a_new_socialism/01_Inequality.md#exploitation) |
| Accumulation, depreciation | Net investment in means of production; past labour "transferred" as stocks are used and machines wear out. | [7, Macro accounting](../Documents/towards_a_new_socialism/07_Macroeconomic_Planning_and_Budgetary_Policy.md#macro-accounting-in-labour-time) |
| Ground rent, differential rent | Ricardo's theory, taken over: better land earns rent because price is set on the worst land in use. The state collects it. | [14, Digression on the Ricardian theory of rent](../Documents/towards_a_new_socialism/14_Property_Relations.md#digression-on-the-ricardian-theory-of-rent) |
| Dictatorship of the proletariat | "a mass democracy unconstrained by entrenched constitutional rights defending private property", not Roman dictatorship. | [13, Democracy and parliamentarism](../Documents/towards_a_new_socialism/13_On_Democracy.md#democracy-and-parliamentarism) |
| Bourgeois right | **Not Marx's sense.** In Marx's *Critique of the Gotha Programme*, "bourgeois right" is the equal standard of the lower phase. Here it means full property: the right to use, buy, sell and inherit (15 on the scale). | [14, Encoding property rights](../Documents/towards_a_new_socialism/14_Property_Relations.md#encoding-property-rights) |
| "from each according to their ability, to each according to their need" | Applied to the NHS, "the only really communist institution introduced by the Labour Party". | [14](../Documents/towards_a_new_socialism/14_Property_Relations.md#rights-of-planning-and-economic-projects) |
| Personifications of capital, money capital | Enterprises that buy labour power to make a profit; money that can be used to exploit. Tokens are designed so that neither can form. | [15](../Documents/towards_a_new_socialism/15_Some_Contrary_Views_Considered.md#diane-elson-the-socialised-market); [10](../Documents/towards_a_new_socialism/10_Foreign_Trade.md#alternatives-to-foreign-exchange) |
| State capitalism | Nationalised firms that still buy labour power and make profits; the book's name for Elson's "socialised market". | [15](../Documents/towards_a_new_socialism/15_Some_Contrary_Views_Considered.md#diane-elson-the-socialised-market) |
| Commonwealth | The book's name for the socialist state: a translation of *res publica*, and the name of "the revolutionary dictatorship established after the overthrow of the Scottish and English monarchies in the 17th century". | [10, note 4](../Documents/towards_a_new_socialism/10_Foreign_Trade.md) |

"Historical materialism" and "dialectic" in any form never appear. "Socially necessary" appears once, about study ("a valid and socially necessary form of work"), not in Marx's sense of socially necessary labour time. The book's labour values are average values for each product, computed from the actual table of the economy.

### What the token is called

The book never settles on one name. They are all the same thing unless noted.

| Name | Where |
| --- | --- |
| labour token | the usual term (ch. 2, 7, 8, 15) |
| labour money | ch. 2 and 3, mostly when speaking of the socialist tradition |
| labour certificate | Marx's term, quoted in ch. 2 |
| labour credit, labour credit card | ch. 2 and 14, and in foreign trade (ch. 10) |
| labour voucher | ch. 2 and 10 |
| labour ticket, national labour ticket | ch. 12, to tell national tokens from commune work-units |
| work-unit | **a different unit:** a commune's internal credit, convertible into national tickets at a rate that may fall below par (ch. 12) |
| certificate of labour credit | **a different instrument:** a transferable, non-interest-bearing paper that foreign firms get for supplying imports, and may trade abroad (ch. 10) |

### The book's own vocabulary

| Term | Meaning |
| --- | --- |
| Planning | The body that owns all collectively operated means of production (except communes'), allocates them and sets labour budgets ([14](../Documents/towards_a_new_socialism/14_Property_Relations.md#rights-of-planning-and-economic-projects)). Also "the planners", "the planning agency", "the Planning Agency". |
| Project | "a coordinated set of activities designed to produce a definite useful result". A unit of work organisation with a labour budget, not a legal person; it can't buy, sell, hire or go bankrupt ([14](../Documents/towards_a_new_socialism/14_Property_Relations.md#rights-of-planning-and-economic-projects)). The book still says "enterprise" in chapters 8–9. |
| Labour budget | A project's allowance in hours. Work and materials are deducted from it and simply cancelled; nobody is paid out of it. |
| Central marketing authority (CMA) | Orders consumer goods from producers and sells them at market-clearing prices ([8](../Documents/towards_a_new_socialism/08_The_Marketing_of_Consumer_Goods.md#consumer-goods-and-the-macro-plan)). |
| Employment agency | Matches workers to projects using the Planning data-net ([14](../Documents/towards_a_new_socialism/14_Property_Relations.md#rights-of-planning-and-economic-projects)). |
| Environment Trust | Owns all natural resources; licenses their use, sets rents and surcharges, but doesn't keep the revenue ([14, Separation of control from benefit](../Documents/towards_a_new_socialism/14_Property_Relations.md#separation-of-control-from-benefit)). |
| Commune | A voluntary household of 50 to 200 adults that takes over housing, cooking, child care, some leisure and care of the old ([12](../Documents/towards_a_new_socialism/12_The_Commune.md)). |
| Social provision, Social | Goods given as a right of citizenship, paid by tax: education, health, child care, and (ch. 13) a television with a voting console. |
| Harmony | A score for each industry: zero at target, negative below, positive above. The plan-balancing algorithm equalises it across industries ([6](../Documents/towards_a_new_socialism/06_Detailed_Planning.md#the-harmony-function)). |
| Technical coefficient | The quantity of one product needed directly to make one unit of another ([6](../Documents/towards_a_new_socialism/06_Detailed_Planning.md)). |
| Transmission rate | The labour a skilled worker "passes on" per hour worked, from the labour embodied in their training ([2](../Documents/towards_a_new_socialism/02_Eliminating_Inequalities.md#skilled-labour-as-a-produced-input)). |
| Demarchy, acephalous state | Government by councils drawn by lot from those with an interest (John Burnheim's word); a state with no head of state and no government ([13](../Documents/towards_a_new_socialism/13_On_Democracy.md#the-acephalous-state)). |
| Psephonomic | The authors' coinage for election by ballot, which they call oligarchic ([13](../Documents/towards_a_new_socialism/13_On_Democracy.md#democracy-and-parliamentarism)). |

### Acronyms

| Acronym | Meaning |
| --- | --- |
| TNS | *Towards a New Socialism* (the preface quotes a reader using it) |
| CMA | Central marketing authority (ch. 8) |
| MES | Minimum economic size: the smallest scale that reaps the economies of scale (ch. 12) |
| GOSPLAN, Gosplan | The Soviet state planning agency |
| CMEA | Council for Mutual Economic Assistance (Comecon), the Soviet-bloc trade organisation |
| MITI | Japan's Ministry of International Trade and Industry, the book's example of capitalist strategic planning |
| CEGB | Central Electricity Generating Board, Britain's nationalised power utility |
| NHS | National Health Service |
| CCITT | The international telecommunications standards body of the time |
| LDC | Less developed country |
| EC, EMU | European Community; European Monetary Union |

## The equations

The book's formulas and formal rules, in order. Equation numbers in brackets are the book's own, where it gives one. "Hours" means hours of simple labour throughout. Where I've written a rule as a formula that the book gives only in words, the entry says so.

### Capitalism measured (ch. 1–3)

**E1. The rate of exploitation** ([1, Exploitation](../Documents/towards_a_new_socialism/01_Inequality.md#exploitation), Table 1.1)

rate of exploitation = *s*/*v*; gross value product = *c* + *v* + *s*; net value product = *v* + *s*

- *c*: constant capital, the value of the means of production used up (materials plus fixed capital consumption): £666,613M in Britain, 1997
- *v*: variable capital, wages in productive sectors: £324,324M
- *s*: surplus value (profits, interest, rent, taxes on production, and the costs of finance and public administration): £316,272M
- Result: *s*/*v* = 98 %, so "Each hour, workers in Britain work just over 30 minutes to produce the value of their own wages."

**E2. Value created per hour** ([2, How much would one hour's labour produce?](../Documents/towards_a_new_socialism/02_Eliminating_Inequalities.md#how-much-would-one-hours-labour-produce), Table 2.1)

*h* = *e* × *f* × *g*; *j* = *i*/*h*

- *e*: productive employment (all employment less finance, public administration and defence, and personal servants): 23,791,000
- *f*: hours per week (40.2); *g*: weeks per year (48); *h*: hours worked in a year
- *i*: net value product, *v* + *s* from E1 (£640,596M)
- *j*: value created per hour: £13.95. This is what an hour's token would have been worth in 1997, before tax.

**E3. Equality against growth** ([2, Equality more effective than growth](../Documents/towards_a_new_socialism/02_Eliminating_Inequalities.md#equality-more-effective-than-growth)). In words in the book; as a formula (*my formalisation*): the years *n* for growth at rate *r* to double an income solve (1 + *r*)<sup>*n*</sup> = 2. At 2.4 % this gives 29 years, as the book says. At 0.5 % it gives 139 years (*my calculation*); the book says 150.

**E4. Two ways of digging a ditch** ([3, Economies of time](../Documents/towards_a_new_socialism/03_Work_Time_and_Computers.md#economies-of-time), Table 3.1)

labour cost = direct hours + indirect hours; money cost = direct hours × wage + indirect hours × value created per hour

- Old method: 100 + 100 = 200 hours; £300 + £753 = £1,053
- New method (an excavator): 50 + 125 = 175 hours; £150 + £941.25 = £1,091.25
- Wage £3.00; value created £7.53 per hour (Britain, 1987). The money-cost formula is *my reconstruction* of how the table's figures were reached; they match it exactly.
- The point: low wages make the method that wastes labour look cheaper, so capitalism is "too slow to adopt labour-saving devices".

### Labour values (ch. 3)

**E5. The two-industry example** ([3, Defining labour content](../Documents/towards_a_new_socialism/03_Work_Time_and_Computers.md#defining-labour-content), Table 3.2, equations 3.1–3.3)

value of 40,000 loaves = 2,000 person-weeks + 2,000 × value of a barrel of oil (3.1)<br>
value of a loaf = (1 + value of oil)/20 (3.2)<br>
value of 3,000 barrels = 1,000 person-weeks + value of 500 barrels (3.3)

- The oil equation gives 2,500 barrels = 1,000 person-weeks, so a barrel is worth 0.4 person-weeks and a loaf (1.4)/20 = 0.07 person-weeks.
- The unit is the person-week. The prose says the oil industry produces "2000 barrels", but the table and equation (3.3) use 3,000; 3,000 is the figure that works. The slip is in the PDF too.

**E6. Labour values in general** ([3, note 3](../Documents/towards_a_new_socialism/03_Work_Time_and_Computers.md))

*L*<sub>*i*</sub> + *I*<sub>*i*1</sub>*v*<sub>1</sub> + *I*<sub>*i*2</sub>*v*<sub>2</sub> + · · · + *I*<sub>*in*</sub>*v*<sub>*n*</sub> = *Q*<sub>*i*</sub>*v*<sub>*i*</sub>, one equation for each industry *i* = 1 … *n*

- *L*<sub>*i*</sub>: direct labour used in industry *i*
- *I*<sub>*ij*</sub>: quantity of industry *j*'s product used up in industry *i*
- *v*<sub>*i*</sub>: labour value of one unit of industry *i*'s product (the unknowns)
- *Q*<sub>*i*</sub>: gross output of industry *i*
- In words: the hours in an industry's whole output equal its own labour plus the hours embodied in everything it used.

**E7. Computing it at scale** ([3, Simplifying the labour value problem](../Documents/towards_a_new_socialism/03_Work_Time_and_Computers.md#simplifying-the-labour-value-problem))

- Solving E6 directly (Gaussian elimination) takes time of order *n*<sup>3</sup>. For a million products that is 10<sup>18</sup> steps: "100 million seconds or 30 years". (10<sup>8</sup> seconds is about 3.2 years, *my calculation*; the book's "30 years" is an arithmetic slip, also in the PDF. The conclusion, "far too slow", stands.)
- Successive approximation instead (written as a formula, *my formalisation*): start with direct labour only, *v*<sub>*i*</sub><sup>(0)</sup> = *L*<sub>*i*</sub>/*Q*<sub>*i*</sub>, then repeat *v*<sub>*i*</sub><sup>(*k*+1)</sup> = (*L*<sub>*i*</sub> + Σ<sub>*j*</sub> *I*<sub>*ij*</sub>*v*<sub>*j*</sub><sup>(*k*)</sup>)/*Q*<sub>*i*</sub>. Each round adds about one binary digit of accuracy if half of a product's value is direct labour; about 15–20 rounds suffice.
- Time order: products × average inputs per product × rounds. For 10<sup>6</sup> products with 1,000 inputs each, 10<sup>9</sup> steps a round, "a couple of seconds" on a 2000-era server. The trick is that the table is mostly zeros, so it is stored as lists, not a matrix.

### Skilled labour (ch. 2)

**E8. A machine passes on its labour** ([2, Skilled labour as a 'produced input'](../Documents/towards_a_new_socialism/02_Eliminating_Inequalities.md#skilled-labour-as-a-produced-input))

labour passed on per unit = labour in the machine/units it makes over its life; per hour = that × units made per hour

- Example: 1,000/1,000,000 = 0.001 hours per unit; at 100 units an hour, 0.1 hours per hour of operation.

**E9. The skilled labour multiplier** ([2, Appendix](../Documents/towards_a_new_socialism/02_Eliminating_Inequalities.md#appendix-illustrative-calculation-of-skilled-labour-multiplier))

R<sub>0</sub> = TH<sub>0</sub>/AH.D<br>
revised total hours = (1 + R<sub>0</sub>SP)TH<sub>0</sub>, and so on in a geometric series, converging to (1 − R<sub>0</sub>SP)<sup>−1</sup>TH<sub>0</sub><br>
R<sub>*f*</sub> = TH<sub>0</sub>/(AH.D − SP.TH<sub>0</sub>); multiplier = 1 + R<sub>*f*</sub>

- TH<sub>0</sub>: first estimate of the hours embodied in training a skilled worker: the student's own 7,200 hours (4 years × 40 hours × 45 weeks) plus teaching (70), tutorials (240) and overheads (70), about 7,600
- AH: hours the qualified worker works a year (35 × 45 = 1,575)
- D: the "depreciation horizon", the years before the skill needs renewing
- SP: the share of TH<sub>0</sub> that is itself skilled labour (teachers, half of overheads): about 0.05
- R<sub>0</sub>, R<sub>*f*</sub>: first and final transmission rate, the embodied hours passed on per hour worked. The series arises because teachers' labour is skilled too, so it carries its own multiplier.
- Results: R<sub>*f*</sub> = 0.50, 0.33, 0.24 for D = 10, 15, 20 years (*my calculation* confirms all three). An engineer with D = 15 counts as 1.33 hours of simple labour per hour worked, **for planning only**: "Society has already met the 'extra third' in paying for the worker's education, so there is no justification for paying the individual any extra."

**E10. Grades of labour** ([2, Differential payment for 'personal qualities'?](../Documents/towards_a_new_socialism/02_Eliminating_Inequalities.md#differential-payment-for-personal-qualities)). In words in the book; as a formula (*my formalisation*):

*p*<sub>A</sub>*H*<sub>A</sub> + *p*<sub>B</sub>*H*<sub>B</sub> + *p*<sub>C</sub>*H*<sub>C</sub> = *H*<sub>A</sub> + *H*<sub>B</sub> + *H*<sub>C</sub>, with *p*<sub>B</sub> = 1 and *p*<sub>A</sub> > 1 > *p*<sub>C</sub>

- *H*<sub>A</sub>, *H*<sub>B</sub>, *H*<sub>C</sub>: hours worked by grade A (above-average productivity for the trade), B (average) and C (below)
- *p*: tokens paid per hour in each grade
- The rule: "keep the total issue of labour tokens equal to the total hours worked". The book doesn't say how far apart *p*<sub>A</sub> and *p*<sub>C</sub> would be; "computers" would work out the rates from the numbers in each grade.

### Strategic planning (ch. 5)

**E11. The discount rate** ([5, The time dimension of production](../Documents/towards_a_new_socialism/05_Strategic_Planning.md#the-time-dimension-of-production) and note 2)

present value = future amount/(1 + *r*)<sup>*t*</sup>

- *r*: the discount rate; *t*: years. Pure labour values amount to *r* = 0.
- Note 2's example: £1,000 a year away at 25 % is worth £800 now.
- Proposal: set *r* to the average growth rate of labour productivity (or by vote). It is "merely a parameter used in the computer programs", not interest on loans (note 5). Figure 5.1 discounts at 9 %.

### Detailed planning (ch. 6)

**E12. Gross output from final targets** ([6](../Documents/towards_a_new_socialism/06_Detailed_Planning.md) and note 2)

*G*<sub>1</sub> = *I*<sub>11</sub> + *I*<sub>12</sub> + *F*<sub>1</sub>, *G*<sub>2</sub> = *I*<sub>21</sub> + *I*<sub>22</sub> + *F*<sub>2</sub><br>
*G*<sub>1</sub> = *a*<sub>11</sub>*G*<sub>1</sub> + *a*<sub>12</sub>*G*<sub>2</sub> + *F*<sub>1</sub>, *G*<sub>2</sub> = *a*<sub>21</sub>*G*<sub>1</sub> + *a*<sub>22</sub>*G*<sub>2</sub> + *F*<sub>2</sub><br>
*g* = *Ag* + *f* ⇒ (*I* − *A*)*g* = *f* ⇒ *g* = (*I* − *A*)<sup>−1</sup>*f*

- *G*: gross output; *F*: final (net) output, for consumption or net investment; *I*<sub>*ij*</sub>: product *i* used in industry *j* (source first, destination second; note this is the reverse of E6's order)
- *a*<sub>*ij*</sub>: technical coefficient, the amount of *i* needed per unit of *j* (10 kg of steel tubing per bicycle)
- *g*, *f*: the vectors of gross and final outputs; *A*: the *n* × *n* matrix of technical coefficients; *I* (in the matrix form): the identity matrix; (*I* − *A*): the Leontief matrix
- Solved by iteration (Jacobi or Gauss–Seidel) on the sparse table, as in E7: 10 million products × 200 inputs × 100 rounds = 2 × 10<sup>11</sup> steps, "a little over half an hour" at a billion instructions a second.
- Then the stock check: each industry works out the machines and labour its gross output needs; the centre adds them up against the stocks and the labour supply, and if they don't fit, cuts "those final output targets which have the lowest social priority" and recomputes.

**E13. The harmony function** ([6, The harmony function](../Documents/towards_a_new_socialism/06_Detailed_Planning.md#the-harmony-function))

*u* = (output − goal)/goal; if *u* < 0, harmony = −*u*<sup>2</sup>, otherwise harmony = √*u*

- output: the net output of a product, after other industries' use; goal: its target
- The algorithm (nine stages) moves resources from industries with high harmony to those with low, until harmony is equal across the economy; a bias *B*, lowered each round, pushes total output up.
- A caution (*my calculation*): the formula doesn't do what the prose and Figure 6.4 say near the target. Just below target, −*u*<sup>2</sup> is almost flat (a 10 % shortfall scores −0.01), while just above, √*u* rises steeply (a 10 % surplus scores +0.32). The figure shows the opposite, steep below and gentle above, which is what "shortages are more serious than … surpluses" needs. The formula only behaves that way for misses of more than 100 %. The PDF prints the same formula, so it is the book's, not a conversion error. Something like −*u*<sup>2</sup> − *k*\|*u*\| below the target would match the figure.

### National accounts in labour time (ch. 7)

**E14. The macro identities** ([7, Macro accounting in labour-time](../Documents/towards_a_new_socialism/07_Macroeconomic_Planning_and_Budgetary_Policy.md#macro-accounting-in-labour-time))

Gross Value Product = Current Labour + Depreciation (7.1)<br>
Net Value Product = Gross Value Product − Depreciation (7.2)<br>
Current Labour Tokens = Current Labour (7.3), hence Current Labour Tokens = Net Value Product<br>
Net Value Product = Consumption + Social + Accumulation + Trade (7.4)

- Gross Value Product: the labour content of everything produced in the year
- Current Labour: hours worked this year; Depreciation: past labour passed on from stocks and wearing machines
- Current Labour Tokens: tokens issued for this year's work (one per hour, so equal to Current Labour)
- Consumption: labour in personal consumer goods; Social: labour in social provision (health, education, child care); Accumulation: net investment; Trade: lending abroad (a trade surplus)

**E15. The flow of funds** ([7](../Documents/towards_a_new_socialism/07_Macroeconomic_Planning_and_Budgetary_Policy.md#macro-accounting-in-labour-time))

households: Current Labour Tokens + Transfers = Tax + Consumption + Net Savings (7.5)<br>
state: Tax + Net Savings = Transfers + Social + Accumulation + Trade (7.6)<br>
with Net Tax = Tax − Transfers:<br>
Current Labour Tokens − Net Tax = Consumption + Net Savings (7.7)<br>
Net Tax + Net Savings = Social + Accumulation + Trade (7.8)<br>
adding: Current Labour Tokens = Consumption + Social + Accumulation + Trade (7.9)

- Transfers: tokens paid to non-workers ("retired people, the disabled, people moving between jobs"). They "cannot simply be 'printed up'"; they must be taxed from workers.
- Net Savings: what households put into state savings, net (E16)
- The point of (7.9): the accounts close, so the plan can be checked for consistency. If net tax is too low, "labour token inflation" (or queues) follows; if too high, unsold goods.
- Example in the book: if the plan gives 55 % of the Net Value Product to consumer goods and nobody saves, net tax must cancel 45 % of the tokens issued.

**E16. Net household saving** ([7, Household saving and credit](../Documents/towards_a_new_socialism/07_Macroeconomic_Planning_and_Budgetary_Policy.md#household-saving-and-credit))

Net Savings = (Retirement Asset Acquisition − Retirement Asset Disbursement) + (Saving Deposit Acquisition − Withdrawals − New Credit)

- Retirement assets: tokens exchanged for an annuity paid later; the labour freed goes to extra accumulation
- Saving deposits: short-term saving for durables and holidays, which can finance consumer credit
- Tokens can't be hoarded otherwise: they expire.

**E17. The flat tax** ([7, Tax policy](../Documents/towards_a_new_socialism/07_Macroeconomic_Planning_and_Budgetary_Policy.md#tax-policy))

flat-tax revenue = *x* − *z* million tokens, so the tax per earner = (*x* − *z*)/number of earners (*the division is my formalisation*)

- *x*: million hours the plan gives to uses other than personal consumption; *z*: forecast net household saving
- One amount per earner, whatever the hours worked: a zero marginal rate. Ground rent (assessed in tokens) and excise on goods like alcohol and tobacco are the other revenues; there is no turnover tax or VAT.

### The consumer market (ch. 8–9)

**E18. The marketing rule** ([8](../Documents/towards_a_new_socialism/08_The_Marketing_of_Consumer_Goods.md) and [Consumer goods and the macro plan](../Documents/towards_a_new_socialism/08_The_Marketing_of_Consumer_Goods.md#consumer-goods-and-the-macro-plan))

for each consumer good: if price/value > Token Consumption/Consumption, increase orders; if equal, keep them; if less, reduce them

- price: the market-clearing price in tokens, set by the CMA by trial and error; value: the labour value marked on the good
- Token Consumption: tokens actually spent on consumer goods; Consumption: the labour devoted to them (E14). Their ratio is an "aggregate price level of sorts", ideally 1.
- The weighted average of price/value across goods, each weighted by its share of Consumption, is identically Token Consumption/Consumption. The book's first statement of the rule (ratio above or below 1.0) is the case where that average is 1.
- Example: an item of 10 hours that clears at 12 tokens has a ratio of 1.2, so make more of it.

**E19. Judging producer goods** ([9, Statistical assessment for producer goods enterprises](../Documents/towards_a_new_socialism/09_Planning_and_Information.md#statistical-assessment-for-producer-goods-enterprises))

for an input used in *n* consumer goods: compare the mean of (market price − labour value) over those goods with zero; there is a 95 % chance a random sample's mean lies within 0 ± 2σ/√*n*

- σ: the standard deviation of (price − value) across all consumer goods, assumed normal with mean zero (by the Central Limit Theorem)
- A mean significantly above zero suggests the input is made with above-average social efficiency; below, a case for "further detailed study". Not proof, and not a basis for pay.

### Foreign trade (ch. 10)

**E20. Production possibilities and the trade rule** ([10](../Documents/towards_a_new_socialism/10_Foreign_Trade.md), [Alternatives to foreign exchange](../Documents/towards_a_new_socialism/10_Foreign_Trade.md#alternatives-to-foreign-exchange))

total labour = (cars × labour per car) + (blouses × labour per blouse), for each country<br>
export a good only if the labour-credit price offered > its domestic labour cost; import only if the price < the domestic cost of making it

- Ricardo's example: Germany has 100 million hours (a car takes 1,000, a blouse 1); China 400 million (5,000 and 2). Specialising (Germany all cars, China all blouses) gives 100,000 cars and 200 million blouses, more than any mixed allocation.
- Table 10.1: exporting oil that cost 1 million hours for cars that would have cost 2 million gives a "labour-time trade deficit" of 1 million hours, which is the gain. Prices are paid in labour credits, so the commonwealth never holds foreign currency.

**E21. Kalecki on trade surpluses** ([10, Advantages of trade deficits](../Documents/towards_a_new_socialism/10_Foreign_Trade.md#advantages-of-trade-deficits))

*I* = *W* + *P*; *I* = *S* = *S*<sub>*w*</sub> + *S*<sub>*p*</sub> + *S*<sub>*f*</sub>; so *P* ≤ *S*<sub>*p*</sub> + *S*<sub>*f*</sub>

- *I*: income in the capitalist sector; *W*: wages; *P*: all property income; *S*: sales, to workers (*S*<sub>*w*</sub>), proprietors (*S*<sub>*p*</sub>) and abroad, net (*S*<sub>*f*</sub>, the trade surplus)
- About capitalism, not the proposal: a trade surplus raises money profits. The book writes the assumption as "*W* < *S*<sub>*w*</sub>", but the words ("sales to workers do not exceed wages") and the conclusion need *S*<sub>*w*</sub> ≤ *W*. The PDF has the same slip.

### Communes, votes and property (ch. 12–14)

**E22. Commune accounts** ([12, Systems of payment and external trade](../Documents/towards_a_new_socialism/12_The_Commune.md#systems-of-payment-and-external-trade), Table 12.1)

distribution fund = external labour credits − tax liability − collective purchases (3,000 − 1,100 − 900 = 1,000)<br>
total work-units = external work + basic internal work + non-basic internal work (3,000 + 1,800 + 1,200 = 6,000)<br>
collective fund = tax + collective purchases + basic internal work (1,100 + 900 + 1,800 = 3,800)<br>
disposable work-units = total − collective fund (6,000 − 3,800 = 2,200) = distribution fund + non-basic internal work<br>
exchange rate = demand for national tickets/distribution fund (e.g. 1,200/1,000 = 1.2 work-units per ticket)

- External work: done for the national economy; the commune, not the member, is credited with national tickets for it
- Basic internal work: work whose product members get as of right (cleaning, child care); non-basic: work whose product members buy with work-units (meals, haircuts)
- Communard Jane: 36 hours worked, 12 assessed for the collective fund, 24 disposable work-units. Parity holds if the commune keeps correct accounts, balances its collective fund, and budgets for exactly the non-basic work members want.

**E23. Counting a budget vote** ([13, note 8](../Documents/towards_a_new_socialism/13_On_Democracy.md))

change in spending = (2*y* − 100)*x*/100 percent

- *x*: the most a budget item may change in one year (percent); *y*: percent of voters voting for the increase
- Example (*my calculation*): with *x* = 10 and 60 % for, spending rises 2 %; with 40 % for, it falls 2 %. The flat tax (E17) then adjusts to cover what was voted.

**E24. The property-right code** ([14, Encoding property rights](../Documents/towards_a_new_socialism/14_Property_Relations.md#encoding-property-rights), Table 14.1 and note 1)

code = use + 2 × sell + 4 × buy + 8 × inherit, each 1 if the right is held, 0 if not (*my formalisation* of the "binary expansion" in note 1; it reproduces every row of the table)

- 0: a slave; 2: a wage worker and their labour (sell only); 7: a capitalist firm and its factory; 15: full "bourgeois right"
- Under the proposal, Planning holds only use (allocation) over the means of production: it has nobody to buy from or sell to.

**E25. Ricardian rent** ([14, Digression](../Documents/towards_a_new_socialism/14_Property_Relations.md#digression-on-the-ricardian-theory-of-rent), Tables 14.4–14.5)

price = cost on the worst land in use; rent on grade *g* = price − cost on grade *g*

- With grade 3 (20 hours, £20 a bushel) in use, grade 1 (£10) pays £10 rent and grade 2 (£15) £5. The commonwealth collects this rent from users of land (farms, communes, home owners) and uses it to lower the flat tax.

## Commentary on work and welfare

### Unskilled labour

- **One hour is one hour, for pay.** Workers get "one labour token per hour" ([2, Inequalities of labour](../Documents/towards_a_new_socialism/02_Eliminating_Inequalities.md#inequalities-of-labour)). The book's tables say who gains: in 1997 "100% of female manual workers and 99% of male manual workers earned less than the egalitarian income of £14 per hour" ([2](../Documents/towards_a_new_socialism/02_Eliminating_Inequalities.md#how-much-would-one-hours-labour-produce)).
- **Simple labour is the unit.** Anyone educated to the baseline counts as "simple labour", the yardstick against which skilled labour is a multiple (E9). The multiplier is for costing projects, not for pay.
- **Everyone can learn almost anything:** "apart from certain extremely demanding tasks and certain impaired individuals, almost everyone can do almost anything" ([2](../Documents/towards_a_new_socialism/02_Eliminating_Inequalities.md#skilled-labour-as-a-produced-input)).
- **Cheap labour holds back technology.** Navvies, dockers and the ditch example (E4) show that low wages let employers "squander labour"; costing in hours removes the bias ([3, Economies of time](../Documents/towards_a_new_socialism/03_Work_Time_and_Computers.md#economies-of-time)).
- **Hard or dangerous jobs.** Shortages of particular skills should first be met by training and by offering "greater choice of work project"; if that fails, "either direction of labour or the payment of 'rents' over and above the regular labour tokens would be required" ([2, Specific labour shortages](../Documents/towards_a_new_socialism/02_Eliminating_Inequalities.md#specific-labour-shortages)). Any such premium is paid out of general taxation, not by printing tokens. For divers, the alternative is to wait for machines.
- **Effort, not skill, may be paid differently**, through grades A, B and C (E10). "There need be no stigma attached to being a 'C' worker; such a worker basically chooses to work at an easier pace—and correspondingly accepts a somewhat lower rate of consumption."
- **The secretary and the professional:** "Why should a secretary get paid only 30 minutes for each hour that she works, whilst professionals in the next office get paid 2 hours for each hour they put in?" ([2, Comparison with historically existing socialism](../Documents/towards_a_new_socialism/02_Eliminating_Inequalities.md#comparison-with-historically-existing-socialism)).

### Unemployment

- **Under capitalism, unemployment is policy.** "Unemployment is the regulator of exploitation and is maintained as such by government policy" ([1, Unemployment](../Documents/towards_a_new_socialism/01_Inequality.md#unemployment)). It needn't mean poverty: "If somebody is idle through no fault of his own, why should he suffer a drop in income?"
- **Under socialism it is abolished, not compensated.** "In a socialist economy the unemployment sanction is quite deliberately removed. Work is guaranteed for all" ([2](../Documents/towards_a_new_socialism/02_Eliminating_Inequalities.md#differential-payment-for-personal-qualities)). The plan "should be designed to use up the available labour resources, without either excess demand or excess supply" ([2, Specific labour shortages](../Documents/towards_a_new_socialism/02_Eliminating_Inequalities.md#specific-labour-shortages)).
- **How it is prevented:** the labour-time budget is balanced; "any shortfall in aggregate demand is compensated for by the marketing authority marking down all consumer goods prices", so there is no recessionary spiral ([14](../Documents/towards_a_new_socialism/14_Property_Relations.md#rights-of-planning-and-economic-projects)). New technology is welcome: "It is a very naive form of socialism that criticises technical change under the belief that it causes unemployment" ([3](../Documents/towards_a_new_socialism/03_Work_Time_and_Computers.md#economies-of-time)).
- **Between jobs**, people get transfers: the consumption allowance must reach "people moving between jobs" ([7](../Documents/towards_a_new_socialism/07_Macroeconomic_Planning_and_Budgetary_Policy.md#macro-accounting-in-labour-time)). The book doesn't say at what rate.
- **Against a basic income.** The Greens' guaranteed income "seems to imply an acceptance that unemployment is inevitable", and "effectively allows people to choose subsidised idleness" ([7, Tax policy](../Documents/towards_a_new_socialism/07_Macroeconomic_Planning_and_Budgetary_Policy.md#tax-policy)). The flat tax is its "mirror image": "each able-bodied person of working age is obliged to perform a basic amount of work for the commonwealth". The same verdict on Elson's minimum income in [15](../Documents/towards_a_new_socialism/15_Some_Contrary_Views_Considered.md#diane-elson-the-socialised-market): a good reform under capitalism, not socialism.
- **Communes are not employers of last resort** ([12](../Documents/towards_a_new_socialism/12_The_Commune.md#systems-of-payment-and-external-trade)).

### Firing and redeployment

- **The capitalist sanction is described and removed.** Under capitalism the employment contract is "enforced by the supervisory agents of the enterprise … backed up by the ultimate sanction of firing" ([2](../Documents/towards_a_new_socialism/02_Eliminating_Inequalities.md#differential-payment-for-personal-qualities)). Under socialism that sanction goes.
- **Projects are closed, workers are not.** "Planning must, however, be at liberty to terminate particular projects if they are deemed not to be cost-effective" ([14](../Documents/towards_a_new_socialism/14_Property_Relations.md#rights-of-planning-and-economic-projects)). "If your project is cancelled, the activity you were involved in has become redundant. That does not mean that you have become redundant; you have the right to expect society to protect your income and provide you with other work."
- **No right to your job.** "it is important that workers do not have the right to permanent employment in any particular enterprise or industry (although they do have the right to employment as such)" ([9, Rewards and sanctions?](../Documents/towards_a_new_socialism/09_Planning_and_Information.md#rewards-and-sanctions)). Enterprises doing badly "will find themselves shrinking, their workers assigned elsewhere." The book contrasts this with the Soviet enterprise, which couldn't lay workers off and so hoarded labour ([14, The enterprise as focus of contradictions](../Documents/towards_a_new_socialism/14_Property_Relations.md#the-enterprise-as-focus-of-contradictions)).
- **Finding a new project.** Mary registers her skills and hours with the employment agency, which searches the Planning data-net; she chooses a project, "has convinced those currently working on it of her suitability", and signs a contract with the agency ([14](../Documents/towards_a_new_socialism/14_Property_Relations.md#rights-of-planning-and-economic-projects)). So the workers on a project have a say in who joins.
- **The right is limited:** "A citizen has the right to be provided with work, but only with such work as she is able to perform and for which there is a need" ([14, Individual property rights](../Documents/towards_a_new_socialism/14_Property_Relations.md#individual-property-rights)).
- **Discipline without firing.** Low effort is met by regrading to C (lower pay), not dismissal (E10). No bonuses tied to enterprise performance ([9](../Documents/towards_a_new_socialism/09_Planning_and_Information.md#rewards-and-sanctions)). The rewards of a growing project are "better promotion prospects, the chance to participate in and shape a growing operation".
- **What the book leaves open** (*my reading*): whether a project can remove one worker (for misconduct, or because colleagues no longer want them), and who decides; how long someone between projects is paid, and at what rate; whether someone can refuse the agency's offers. The book's one mention of compulsion is "direction of labour" as a last resort for skill shortages ([2](../Documents/towards_a_new_socialism/02_Eliminating_Inequalities.md#specific-labour-shortages)).

### Students

- **Study is paid work.** "Not only would the education itself be free, as it has been in Britain, but in addition students could receive a regular wage during their period of study. Study is a valid and socially necessary form of work. It produces skilled labour as its 'output', and should be rewarded accordingly" ([2, Differential payment for education/skill?](../Documents/towards_a_new_socialism/02_Eliminating_Inequalities.md#differential-payment-for-educationskill)). In the multiplier (E9) the student's own hours count as simple labour.
- **So no premium for graduates.** The case for higher pay as compensation for study falls, since there is "no individual expense or earnings-loss". And study isn't much of a sacrifice anyway: "Compared to many working-class youngsters, students have an easy time. The work is clean. It is not too demanding."
- **Retraining is periodic.** The engineer's skills "depreciate" over 10–20 years, after which "she will need, or become eligible for, another period of full-time education" (E9).
- **Education is a right of citizenship,** paid from tax ([5, Rights of citizenship](../Documents/towards_a_new_socialism/05_Strategic_Planning.md#rights-of-citizenship)).
- **What the book leaves open:** who decides how many places each course has, and who gets them. The plan should "project and advertise potential shortages" ([2](../Documents/towards_a_new_socialism/02_Eliminating_Inequalities.md#specific-labour-shortages)), which implies the plan sets numbers.

### Youth and children

- **Under capitalism:** "Vulnerable groups like teenagers have their rights to benefits withdrawn"; "When youngsters are compelled to work for what are generously called training schemes at £25 per week, is it any wonder that starting rates for adults are as low as £1.70 per hour?" ([1, Unemployment](../Documents/towards_a_new_socialism/01_Inequality.md#unemployment)).
- **Aspiration.** Working-class children's "career aspirations are stunted from infancy"; equal pay, as "a moral statement", would raise them over time ([2](../Documents/towards_a_new_socialism/02_Eliminating_Inequalities.md#differential-payment-for-educationskill)).
- **Children are non-producers** supported from the surplus, with soldiers, pensioners and the sick ([2](../Documents/towards_a_new_socialism/02_Eliminating_Inequalities.md#differential-payment-for-personal-qualities)). Free compulsory schooling is counted as a gain of "socialism" over the domestic economy ([1](../Documents/towards_a_new_socialism/01_Inequality.md#womens-economic-subordination)).
- **Young adults** borrow against future income; consumer credit continues for them ([7](../Documents/towards_a_new_socialism/07_Macroeconomic_Planning_and_Budgetary_Policy.md#household-saving-and-credit)).
- **In communes:** "each adult member … should have at least one room for his or her own exclusive use", "probably" extended to all "post-pubertal members" ([12, Housing](../Documents/towards_a_new_socialism/12_The_Commune.md#housing)).
- **What the book leaves open:** the age at which the work obligation and the flat tax start, and **how a child's own consumption is paid for**. Transfers in chapter 7 go to "retired people, the disabled, people moving between jobs"; children aren't on the list. *My reading:* outside free provision, children's goods come out of their parents' (or their commune's) tokens, as now.

### Retirement

- **Under capitalism:** pensions are held low by policy, to push people into private schemes that "prolong the income differentials established during working life into retirement" ([1, Infirmity and old age](../Documents/towards_a_new_socialism/01_Inequality.md#infirmity-and-old-age)). Pensions would be higher "if there were no private pensions and if decisions on state pension levels were taken by people who expected to have to rely upon these pensions themselves."
- **The real support:** "Retired people are actually supported not by their savings, but by the work of the younger members of society … The young will still be the only support for the old" ([7](../Documents/towards_a_new_socialism/07_Macroeconomic_Planning_and_Budgetary_Policy.md#household-saving-and-credit)).
- **How they are paid:** by transfers of tokens out of the flat tax (E15), plus whatever retirement assets they bought while working (E16), which pay an annuity. "An adequate state pension would reduce the necessity for private saving."
- **Planning for an ageing population:** "faced with the prospect of an increase in the proportion of retirees in the population, the rate of accumulation should be raised" to raise productivity in time ([7](../Documents/towards_a_new_socialism/07_Macroeconomic_Planning_and_Budgetary_Policy.md#household-saving-and-credit)).
- **Implicit interest:** as productivity rises, labour values fall, so tokens saved buy more later ([7, Interest on savings?](../Documents/towards_a_new_socialism/07_Macroeconomic_Planning_and_Budgetary_Policy.md#interest-on-savings)).
- **In communes** the old get cooking, cleaning and company without "the stigma and isolation associated with entering a separate old folks' home", and fitter members can keep working "rather than suffering the enforced idleness of retirement" ([12, Helping senior citizens](../Documents/towards_a_new_socialism/12_The_Commune.md#helping-senior-citizens)).
- **What the book leaves open:** the pension age and the level of the pension, beyond the hope that ending exploitation "would create political conditions favourable to ending much of the economic privations experienced by older people" ([2](../Documents/towards_a_new_socialism/02_Eliminating_Inequalities.md)).

### Illness, disability and injury

- **Under capitalism:** "A person need not be poor just because he is old, disabled or otherwise unable to work … It is only those who lack property, and are dependent upon selling their labour, who are thrown into hardship by injury or old age" ([1, Infirmity and old age](../Documents/towards_a_new_socialism/01_Inequality.md#infirmity-and-old-age)). Chapter 1 handles disability together with old age, under "Infirmity and old age".
- **Health care is free,** a right of citizenship: "In order to function as an active, productive member of society one must be well-educated, healthy and free of the need to stay at home with dependent children all day" ([5, Rights of citizenship](../Documents/towards_a_new_socialism/05_Strategic_Planning.md#rights-of-citizenship)). The NHS is the model of "from each according to their ability, to each according to their need" ([14](../Documents/towards_a_new_socialism/14_Property_Relations.md#rights-of-planning-and-economic-projects)).
- **Income for those who can't work:** "the disabled" are among the non-workers who receive token transfers, taxed from workers ([7](../Documents/towards_a_new_socialism/07_Macroeconomic_Planning_and_Budgetary_Policy.md#macro-accounting-in-labour-time)); "the sick" are among the non-producers the surplus must support ([2](../Documents/towards_a_new_socialism/02_Eliminating_Inequalities.md#differential-payment-for-personal-qualities)).
- **Less need to save against illness:** saving "against lean times to come: unemployment, serious illness, early death of the 'breadwinner'" is one motive socialism weakens, though the book only spells out the case for unemployment ([7](../Documents/towards_a_new_socialism/07_Macroeconomic_Planning_and_Budgetary_Policy.md#household-saving-and-credit)).
- **Work for those with reduced capacity.** The right to work covers "such work as she is able to perform" ([14](../Documents/towards_a_new_socialism/14_Property_Relations.md#individual-property-rights)); "certain impaired individuals" are the exception to "almost everyone can do almost anything" ([2](../Documents/towards_a_new_socialism/02_Eliminating_Inequalities.md#skilled-labour-as-a-produced-input)). Grade C (E10) offers a slower pace for less pay, but the book presents it as a choice, not as provision for disability.
- **What the book leaves open** (*my reading*): sick pay for short illnesses (does a worker off sick for a week get tokens, or a transfer?); the level of disability transfers; who assesses inability to work; injury at work, and safety (mentioned once, as an issue for workers' control, [14](../Documents/towards_a_new_socialism/14_Property_Relations.md#rights-of-planning-and-economic-projects)); and how the flat tax applies to someone who can work only a few hours. The flat tax falls on "each able-bodied person of working age", so people with disabilities are presumably exempt, but a worker doing ten hours a week pays the same amount as one doing forty.

### Child care

- **Child care is unpaid work in "the domestic economy"**, which the book treats as a mode of production that exploits married women: "neither the results of work nor the work itself is paid for" ([1, Women's economic subordination](../Documents/towards_a_new_socialism/01_Inequality.md#womens-economic-subordination)). Its remaining fields include "the care of preschool infants" and "part of the care of school age children". Nursery provision is one of the "Areas of current conflict between the socialist and domestic modes of production".
- **The aim is to replace it, not to pay for it.** Goal 3 of planning is "real economic equality between the sexes through the progressive elimination of patriarchal forms of economy" ([4](../Documents/towards_a_new_socialism/04_Basic_Concepts_of_Planning.md#what-would-be-first-order-goals)). The book never proposes paying tokens to parents caring for their own children at home.
- **Route 1: public child care.** The macro plan has a category for "socialised child-care" ([4, Levels of planning](../Documents/towards_a_new_socialism/04_Basic_Concepts_of_Planning.md#levels-of-planning)) and a right of citizenship financed out of general taxation ([5](../Documents/towards_a_new_socialism/05_Strategic_Planning.md#rights-of-citizenship)). Its workers are paid tokens like anyone else, and it is counted in "Social" (E14).
- **Route 2: the commune.** A commune should be "large enough to support at least a kindergarten and perhaps a primary school". The gain is productivity: "It will free a significant percentage of the female population from individual child rearing, an activity with low labour productivity. These women can then participate in social labour of higher productivity … and obtain an independent income" ([12, Childcare](../Documents/towards_a_new_socialism/12_The_Commune.md#childcare)). Child-minding in the commune is paid in commune work-units at par with outside work, either as a full-time job or on a rota ([12, Distribution of tasks](../Documents/towards_a_new_socialism/12_The_Commune.md#distribution-of-tasks)). If it counts as "basic" internal work (the book doesn't classify it), it is paid for out of the commune's collective fund, which members' outside work finances (E22) (*my reading*).
- **Economies of scale** are the whole justification: "It is because communal childcare saves labour that it is progressive … if the contrary were true, and communal life resulted in a greater number of person-hours spent looking after children, one would need other very compelling reasons to justify it" ([12, Basic rationale](../Documents/towards_a_new_socialism/12_The_Commune.md#basic-rationale-in-terms-of-efficiency)).
- **Communes are voluntary:** "we do not envisage compulsory collectivisation" ([12](../Documents/towards_a_new_socialism/12_The_Commune.md#the-activities-of-urban-communes)), though public policy may favour them for a transitional period ([12, Public policy](../Documents/towards_a_new_socialism/12_The_Commune.md#public-policy)).
- **Fertility.** Under the domestic mode of production, "control over fertility is essential to women who wish to control their own labour time"; abortion rights are named as the most important issue in women's political struggle so far ([1](../Documents/towards_a_new_socialism/01_Inequality.md#womens-economic-subordination)).
- **What the book leaves open** (*my reading*): a family that stays a nuclear household and doesn't use public care does its child care unpaid, exactly as now. There is no parental leave, no child allowance (see [Youth and children](#youth-and-children)), and no rule for how the flat-tax obligation applies to a parent caring full time. The book's answer to all of these is to make the unpaid option unattractive, not to pay it.

## A back door to Leninism?

Patrick's question is whether the computational justification and state central planning hide a back door to Leninism, Trotskyism or Stalinism, bearing in mind that central planning also happens under capitalism: in huge corporations, public corporations, the military–industrial complex and states themselves.

### Central planning is not the test, and the book agrees

The book itself leans on capitalist planning for its evidence:

- **Corporations:** a car company's projects "do not own the office or factory space they use, nor do they employ the people who work on them—the company does"; that is the model for Planning and its projects ([14](../Documents/towards_a_new_socialism/14_Property_Relations.md#rights-of-planning-and-economic-projects)). Divisions of a large firm "integrated through internal corporate planning, rather than via the market" face the same problems of honest information as socialist planning ([9](../Documents/towards_a_new_socialism/09_Planning_and_Information.md#information-performance-measures-and-incentives)). "Ford, for example, coordinates its car production on a world-wide basis" ([11](../Documents/towards_a_new_socialism/11_Trade_Between_Socialist_Countries.md#less-developed-countries)).
- **States:** MITI's strategic planning in Japan ([4](../Documents/towards_a_new_socialism/04_Basic_Concepts_of_Planning.md#levels-of-planning)); wartime state control of the British and American economies ([1](../Documents/towards_a_new_socialism/01_Inequality.md#exploitation)); NASA and the CEGB as "special state agencies that mimic socialist planning" ([5](../Documents/towards_a_new_socialism/05_Strategic_Planning.md#the-environment-and-natural-resources)).
- **The military–industrial complex:** the only Western sector where public research led through to production was arms; "an absolute priority would be to create a collection of civil institutions to replace those of the military-industrial complex" ([5](../Documents/towards_a_new_socialism/05_Strategic_Planning.md#planning-the-industrial-structure)).
- **Public corporations:** the Coal, Gas and Electricity Boards and the NHS ([14](../Documents/towards_a_new_socialism/14_Property_Relations.md#rights-of-planning-and-economic-projects)).
- **Retail:** the bar codes of the retail trade are the basis of its product coding ([3](../Documents/towards_a_new_socialism/03_Work_Time_and_Computers.md#the-internet-and-labour-values); [9](../Documents/towards_a_new_socialism/09_Planning_and_Information.md#product-coding)).

So a large planned economy in itself proves nothing either way. The questions that tell a Leninist design from another are *who controls the plan*, *whether workers have any power of their own against it*, and *how the system comes into being*. On each, the book gives a mixed answer.

### What the book takes from the Soviet model

It says so openly, not cryptically:

- **The USSR was socialist.** "(1) Soviet society was indeed socialist." The test is the mode of extracting the surplus: under Stalin's plans the split between necessary and surplus product "was the result of political decisions", which "is entirely in line with what Marx had hoped for", except that Marx imagined the decision as democratic ([Introduction](../Documents/towards_a_new_socialism/00b_Introduction.md#in-what-sense-was-the-ussr-socialist)). This defines socialism by state planning, not by workers' control.
- **Stalin's industrialisation is praised for its results:** the 1930s built "a heavy industrial base at unprecedented speed" ([Introduction](../Documents/towards_a_new_socialism/00b_Introduction.md#in-what-sense-was-the-ussr-socialist)); "it is rather remarkable that the Soviets should have been so successful" ([6](../Documents/towards_a_new_socialism/06_Detailed_Planning.md#planning-in-the-ussr)). Militarisation is put down to the arms race, "no more an essential feature of socialism than is the militarisation of the economy of Israel an essential feature of capitalism" ([4](../Documents/towards_a_new_socialism/04_Basic_Concepts_of_Planning.md)). The Soviet fusion and space programmes are held up as long-term planning the market can't do ([5](../Documents/towards_a_new_socialism/05_Strategic_Planning.md#the-environment-and-natural-resources)). "Whatever one might say against the economic system that used to operate in the USSR before Gorbachev, prices were stable and there were no recessions" ([15](../Documents/towards_a_new_socialism/15_Some_Contrary_Views_Considered.md#diane-elson-the-socialised-market)).
- **The Soviet property core is kept and tightened.** One body, Planning, owns all collectively worked means of production; producer goods are allocated, never sold; projects have no legal personality; finance is a "unified state-run 'financial system'" that can ration withdrawals from saving deposits ([7](../Documents/towards_a_new_socialism/07_Macroeconomic_Planning_and_Budgetary_Policy.md#household-saving-and-credit)); the state has a monopoly of foreign trade, and bringing in foreign currency is outlawed ([10](../Documents/towards_a_new_socialism/10_Foreign_Trade.md#alternatives-to-foreign-exchange)). The book defends "the Marxist idea of planning the economy like one vast enterprise" and argues that "centralised ownership and planning are preconditions for democratic working-class control" ([14](../Documents/towards_a_new_socialism/14_Property_Relations.md#rights-of-planning-and-economic-projects)). In one respect (*my reading*) it is more centralised than the Soviet system, which split the power to dispose of property between Gosplan, the ministries and the enterprises.
- **Internationally, Gosplan is the model.** The USSR's state property "corresponded to reality", and GOSPLAN was "an international planning organisation". Socialist countries should "subordinate their economies to an international planning system", which "involves a surrender of national sovereignty". Had the Communist International survived, "The existence of a single international political party would at the very least have acted as a brake on nationalist pressures" ([11](../Documents/towards_a_new_socialism/11_Trade_Between_Socialist_Countries.md#what-we-advocate)).
- **On Trotsky and Stalin,** the book is even-handed about socialism in one country ("each side of this argument had some force"), and calls the collapse of the USSR a "counter-revolution" ([11](../Documents/towards_a_new_socialism/11_Trade_Between_Socialist_Countries.md#less-developed-countries); [10, note 4](../Documents/towards_a_new_socialism/10_Foreign_Trade.md)). It praises "Mao and the Left in China" for opposing wage differentials in the Cultural Revolution ([2](../Documents/towards_a_new_socialism/02_Eliminating_Inequalities.md#comparison-with-historically-existing-socialism)).

### What the book rejects

Also openly, and this is where it parts from Lenin, Trotsky and Stalin alike:

- **Terror and the cult.** The Stalin cult was "central to the Soviet mode of extraction of a surplus product" *because* the system was undemocratic; "the stern and utterly ruthless liquidator" is not excused ([Introduction](../Documents/towards_a_new_socialism/00b_Introduction.md#in-what-sense-was-the-ussr-socialist)). "Without democracy … the leaders of a socialist society will be driven to coercion" ([Introduction](../Documents/towards_a_new_socialism/00b_Introduction.md#what-is-the-theoretical-basis-for-a-new-socialism)). "Lenin and Stalin were dictators in this Roman sense" ([13](../Documents/towards_a_new_socialism/13_On_Democracy.md#democracy-and-parliamentarism)).
- **The party-state:** "communist party dictatorship" has collapsed, and "few people in the West have ever openly advocated it" ([13](../Documents/towards_a_new_socialism/13_On_Democracy.md#direct-democracy-or-soviet-democracy)). No party appears anywhere in the book's constitution.
- **Democratic centralism and elections:** "Lenin's notion of 'democratic centralism' … is fundamentally flawed. It seeks to build a democracy on an instrument of lass rule: elections" ([13](../Documents/towards_a_new_socialism/13_On_Democracy.md#democratic-centralisma-dead-end); "lass" is the PDF's misprint for "class"). The right of recall is "laughable".
- **Soviets and workers' councils:** attachment to them is "sentimental", "an unthinking nostalgia", and soviets "provide the ideal medium for the establishment of a one-party state" ([13](../Documents/towards_a_new_socialism/13_On_Democracy.md#direct-democracy-or-soviet-democracy)). This sets the book against Trotskyism as much as against council communism: both hold up the soviets of 1917 as the democratic form that was betrayed.
- **Government itself:** "Planning, for example, is not under government control but under a supervisory committee of ordinary citizens, who, since they are drawn by lot, will be predominantly working people" ([13, The acephalous state](../Documents/towards_a_new_socialism/13_On_Democracy.md#the-acephalous-state)). The big shares of the budget, the rate of accumulation and major environmental questions go to popular vote ([7](../Documents/towards_a_new_socialism/07_Macroeconomic_Planning_and_Budgetary_Policy.md#taxation-and-accumulation); [5](../Documents/towards_a_new_socialism/05_Strategic_Planning.md#the-environment-and-natural-resources)).
- **Information control:** "Our planning proposals absolutely require a free flow of information and universal access to computer systems, and this was politically impossible in the USSR under Brezhnev" ([6](../Documents/towards_a_new_socialism/06_Detailed_Planning.md#planning-in-the-ussr)). Commercial confidentiality is to be abolished, not state secrecy extended ([9](../Documents/towards_a_new_socialism/09_Planning_and_Information.md#information-and-property)).
- **Forced labour and forced collectivisation:** direction of labour on Soviet construction projects is recalled as "draconian" and "unpopular" ([2](../Documents/towards_a_new_socialism/02_Eliminating_Inequalities.md#specific-labour-shortages)); communes are voluntary ([12](../Documents/towards_a_new_socialism/12_The_Commune.md#the-activities-of-urban-communes)); workers choose their own projects and hours ([14](../Documents/towards_a_new_socialism/14_Property_Relations.md#rights-of-planning-and-economic-projects); [7](../Documents/towards_a_new_socialism/07_Macroeconomic_Planning_and_Budgetary_Policy.md#tax-policy)).

### What the computation argument does and doesn't do

*My reading.* The computing chapters answer one objection: the claim, from von Mises (named in [ch. 5](../Documents/towards_a_new_socialism/05_Strategic_Planning.md#the-environment-and-natural-resources)) to Nove, that a planned economy can't calculate (Nove's "10 million year" estimate, [3](../Documents/towards_a_new_socialism/03_Work_Time_and_Computers.md#the-problem-of-scale)). If the book is right, the main technical case against Gosplan falls, and the Soviet failure becomes a failure of tools and politics, not of planning. That is the sense in which computation rehabilitates the Soviet economic model.

But the computation doesn't itself require a single centre. The book says values can be computed by "a large distributed network of much more modest personal computers" ([6](../Documents/towards_a_new_socialism/06_Detailed_Planning.md#planning-in-the-ussr)); each project models its own process in a spreadsheet and exchanges values by email ([3](../Documents/towards_a_new_socialism/03_Work_Time_and_Computers.md#the-internet-and-labour-values)); its Chilean precedent is "real time decentralised control", in which a problem passes up to the next level only if the local Opsroom fails to act ([6](../Documents/towards_a_new_socialism/06_Detailed_Planning.md#economic-cybernetics-in-chile)). The decision to make Planning the *sole owner* is argued on other grounds entirely: that separate public bodies (the Coal, Gas and Electricity Boards) pursue "sectional interests", and that workers in one industry may not share the interest of the class as a whole ([14](../Documents/towards_a_new_socialism/14_Property_Relations.md#rights-of-planning-and-economic-projects)). So if there is a back door, it isn't the algorithms. It is the property design.

### Where power concentrates

*My reading.* These are the points where the design, as written, would let a small group gain control, whatever the authors intend:

1. **The economy is specified in detail; its democratic control in outline.** Chapters 4–12 speak repeatedly of "a socialist government", "the state", "the planners" and "the central planning agency" that "issue instructions". The government only disappears in chapter 13, which says nothing about how the juries would control the hundreds of decisions those chapters give to planners. Chapter 14 sets aside "the constitutional mechanisms required to bring Planning under democratic control" entirely.
2. **Agenda-setting stays with experts.** "Teams of professional economists draw up alternative plans to put before a planning jury which would then choose between them" ([13](../Documents/towards_a_new_socialism/13_On_Democracy.md#democracy-and-planning)). For 10–15-year strategic plans, "It is not clear to what extent this level of planning can be democratic"; they would be drawn up by "small committees of economists with research scientists" ([5](../Documents/towards_a_new_socialism/05_Strategic_Planning.md#planning-the-industrial-structure)). Whoever writes the options sets the bounds of the choice.
3. **One owner, and no counterweight.** Workers own nothing they work with, projects can't hold property or make contracts, and Planning can close any project. The book offers workers no organisation of their own against Planning: no trade unions, no right to strike, no workers' councils, no political parties are mentioned for the new society. Unions and strikes appear only under capitalism; parties only in the British property table. Juries drawn by lot are individuals for a term, not organised interests.
4. **Law gives way to the majority.** "For a democracy to be of any use to the proletariat, the masses must be sovereign, unchained by the rule of law, able to issue decrees that violate well established rights to property in land or capital" ([13](../Documents/towards_a_new_socialism/13_On_Democracy.md#democracy-and-parliamentarism)). The target is property rights, but the book names no rights that *would* be entrenched (speech, association, movement, privacy). Its "positive rights" are economic: to work, to the full value of one's labour, and to spend it ([14](../Documents/towards_a_new_socialism/14_Property_Relations.md#individual-property-rights)).
5. **Coercive options are kept in reserve.** Direction of labour as a last resort for skill shortages; "policing" as one of "only two methods for ensuring that skilled workers continue to work as intended", against emigration among other things ([2](../Documents/towards_a_new_socialism/02_Eliminating_Inequalities.md#specific-labour-shortages)); all purchases by plastic card, with the import of foreign currency outlawed ([10](../Documents/towards_a_new_socialism/10_Foreign_Trade.md#exchange-rates-tourism-and-black-markets)); a complete register of every product and its location ([9](../Documents/towards_a_new_socialism/09_Planning_and_Information.md#unified-stock-control)). Each has an economic reason in the book. Together they give whoever controls Planning a great deal of information about, and leverage over, every citizen.
6. **The transition is missing, and the hints point to a party.** The preface admits the book has no answer to how to get there ("Good question"). The only hints are in chapters 11 and 13: soviets overthrow a state only "if they are led by a cohesive group of determined revolutionists", "Such communist domination is probably a precondition for the overthrow of the bourgeois state in any case", and a "single international political party" would have helped unify socialist states. The book's democratic constitution is for after the revolution; for the revolution itself, its few remarks describe a vanguard.

### Verdict

*My reading.* There is no hidden Leninist party in *Towards a New Socialism*; its rejection of the party-state, soviets, democratic centralism and elected rulers is explicit and argued. What it does carry over, in plain sight, is the Soviet economic architecture: a single public owner, central allocation of producer goods, state monopolies of finance and foreign trade, and a definition of socialism (state planning of the surplus) under which the USSR qualifies. Computation is offered to show that this architecture can work efficiently. Athenian sortition is offered, in place of the Communist Party, as what keeps it democratic.

Whether that substitution holds is the real question, and the book doesn't settle it: the economic machinery is designed in detail, the democratic controls only in sketch, with no independent workers' organisations and no entrenched civil rights between the citizen and the single owner, and with a transition that, on the book's own hints, needs a disciplined communist party to start. Read that way, the book isn't Stalinist (it condemns terror and the cult and demands democracy), and it isn't Trotskyist (it dismisses the soviet democracy Trotsky defended). It is closest to a democratised Gosplan, and its exposure is the one Patrick's question points at: if the sortition layer were captured, sidelined or never built, what would remain is the Soviet economic model with better computers.

On the capitalist side, *my reading*: corporations, the military–industrial complex and states already plan on this scale without democratic control of the plan, and the book's own examples show it. What separates the book's design from them is not the planning but two things: there is no wage labour (tokens can't be transferred, so no one can hire anyone), and the plan's owner is meant to answer to a public chosen by lot. The first is built into the token. The second rests on the chapter the book develops least.

## The conceptual model

A summary of the proposal for someone who won't read the book. Section links point to where each element is argued.

### Actors

| Actor | Role |
| --- | --- |
| Citizens | Work on projects, communes or (if allowed) self-employment; receive tokens; pay the flat tax; buy consumer goods; vote on budget shares in hours a week; serve on juries when drawn by lot |
| Non-workers | Children, retired people, people with disabilities, people between projects: receive token transfers or are supported by their families and communes |
| Projects | Units of work with a labour budget (a factory line, a hospital, a film); no property, no legal personality, can't hire or go bankrupt ([14](../Documents/towards_a_new_socialism/14_Property_Relations.md#rights-of-planning-and-economic-projects)) |
| Planning | Owns all collectively worked means of production; computes labour values and the plan; allocates producer goods and labour budgets; closes and opens projects |
| Central marketing authority | Orders consumer goods, sells them at market-clearing prices, reports price/value ratios ([8](../Documents/towards_a_new_socialism/08_The_Marketing_of_Consumer_Goods.md#consumer-goods-and-the-macro-plan)) |
| Employment agency | Matches people to projects ([14](../Documents/towards_a_new_socialism/14_Property_Relations.md#rights-of-planning-and-economic-projects)) |
| State financial system | Saving deposits, consumer credit, retirement assets ([7](../Documents/towards_a_new_socialism/07_Macroeconomic_Planning_and_Budgetary_Policy.md#household-saving-and-credit)) |
| Ministry of foreign trade | Pays foreign suppliers in labour credits; decides imports and exports by labour cost ([10](../Documents/towards_a_new_socialism/10_Foreign_Trade.md#alternatives-to-foreign-exchange)) |
| Environment Trust | Owns natural resources; licenses use, sets land rents and pollution surcharges; keeps none of the revenue ([14](../Documents/towards_a_new_socialism/14_Property_Relations.md#separation-of-control-from-benefit)) |
| Communes | Voluntary households of 50–200 adults with their own internal credit ([12](../Documents/towards_a_new_socialism/12_The_Commune.md)) |
| Juries and councils | Chosen by lot from users and workers of each public body; a planning jury chooses between plans drafted by economists ([13](../Documents/towards_a_new_socialism/13_On_Democracy.md#the-acephalous-state)) |
| The electorate | Votes by television console on budget shares, the rate of accumulation and major environmental questions |

### Units

- **The hour of simple labour** is the unit of account for everything: costs, the national accounts, the budget.
- **The labour token**: one per hour worked (adjusted by grade A, B or C), non-transferable, cancelled when spent, expires after a set date.
- **The labour value** of a product: direct plus indirect hours, from the input–output table (E6–E7). Marked on every consumer good.
- **The price** of a consumer good: in tokens, set to clear the market; it may differ from the value.
- **The skilled-labour multiplier** (E9): for costing projects only, never for pay.

### Rules

1. One token per hour, for all work, including study (ch. 2).
2. No one can hire anyone; tokens can't be transferred between people (ch. 14).
3. Producer goods are allocated by Planning, never bought or sold (ch. 8, 14).
4. Projects spend labour budgets; deductions are cancelled, not paid to anyone (ch. 2, 14).
5. Consumer goods are sold at market-clearing prices; production follows the price-to-value ratio (E18).
6. Education, health care and child care are free by right of citizenship (ch. 5).
7. A flat tax per earner, set to cover what the vote has allocated to social provision, accumulation and transfers (E17, E23).
8. Ground rent on all land in use and surcharges on polluting goods go to the public budget (ch. 7, 14).
9. Everyone has a right to work, but not to a particular job; Planning may close projects (ch. 9, 14).
10. Saving only through state accounts; tokens otherwise expire (ch. 7).
11. Foreign trade only by the state, paid in labour credits; no foreign currency at home (ch. 10).

### Flows in one period

1. **The vote** sets the shares of labour time: so many hours a week for health, education, child care, accumulation (E23, [13](../Documents/towards_a_new_socialism/13_On_Democracy.md#democracy-and-planning)).
2. **The macro plan** splits the Net Value Product into Consumption, Social, Accumulation and Trade (E14) and sets the flat tax (E17).
3. **The strategic plan** decides which industries grow or shrink, which technologies to use, what to import ([5](../Documents/towards_a_new_socialism/05_Strategic_Planning.md)).
4. **The detailed plan** turns final targets into gross outputs (E12), checks them against machines and labour, and adjusts targets with the harmony algorithm (E13).
5. **Projects work.** Their hours are credited as tokens to the workers and deducted from their labour budgets.
6. **Households pay the flat tax**, receive transfers if they don't work, save or borrow, and spend tokens on consumer goods.
7. **The CMA** records each good's price/value ratio and the total Token Consumption, then raises or cuts orders (E18).
8. **Values are recomputed** as technology and output change; projects register new methods (E7, [9](../Documents/towards_a_new_socialism/09_Planning_and_Information.md#information-social-problems)).

### A worked period (*my illustration*)

An economy of 100 workers, each working 40 hours, and 10 retired people. Current Labour = 4,000 hours, so 4,000 tokens are issued (E14). The vote gives 25 % of the Net Value Product to social provision and 20 % to accumulation; consumption gets 55 %, that is 2,200 hours of consumer goods. Nobody saves.

- Consumption tokens must total 2,200. The retired get transfers of 20 tokens each, 200 in all, so workers must keep 2,000.
- Net Tax = 4,000 − 2,200 = 1,800 (E15). Tax = Net Tax + Transfers = 2,000, so the flat tax is 20 tokens per worker (E17).
- Each worker keeps 40 − 20 = 20 tokens. One who works 50 hours pays the same 20 and keeps 30: the zero marginal rate.
- In the shops, a shirt with a labour value of 2 hours clears at 2.4 tokens: a ratio of 1.2, above the average of 1.0, so the CMA orders more shirts next period (E18).

### Control loops

| Loop | Signal | Response |
| --- | --- | --- |
| Consumer demand | Price/value ratio of each good against the average | More or less of that good next period (E18) |
| Macro balance | Token Consumption/Consumption away from 1 | Change the tax, encourage saving, or shift labour to consumer goods (ch. 8) |
| Plan consistency | Gross outputs exceed machines or labour | Cut the lowest-priority targets and recompute (E12–E13) |
| Producer efficiency | Mean price − value of the consumer goods an input feeds; labour values of rival producers of one good | Further study; shrink or close high-cost projects (E19, [9](../Documents/towards_a_new_socialism/09_Planning_and_Information.md#against-monopoly)) |
| Honest data | Engineers who propose a method must then use it | Accurate estimates of inputs (ch. 9) |
| Democracy | Votes on budget shares | Flat tax adjusts automatically (E23) |
| Environment | Scientific investigation, referendum | Licences, rents, surcharges by the Environment Trust (ch. 5, 14) |

### What the book leaves open

- How to get from capitalism to this system (the preface says so).
- How the juries control Planning in practice, and who drafts the plans they choose between.
- Workers' own organisations: unions, strikes, workplace councils (*my reading*: absent).
- Sick pay, the level of transfers to people who can't work, the pension age, children's income, parental leave.
- How individual workers are disciplined or removed from a project.
- How strict "approximately market-clearing" pricing is, and how fast output follows the ratio.
- The harmony formula's mismatch with its own figure (E13).
- Whether self-employed tradespeople (allowed in [14, Self-employment](../Documents/towards_a_new_socialism/14_Property_Relations.md#self-employment)) pay the flat tax.

## Corrections and slips

Found while writing this note, and checked against the PDF:

- **Fixed (conversion errors):** in chapter 3, "Assume 10[^6] products" had turned the exponent of 10<sup>6</sup> into a footnote marker; in chapter 7, the Net Savings equation had been split across two paragraphs by a page break. Both are corrected in the single file, in the chapter files (regenerated with `split_chapters_tns.py`) and in the converter's `TEXT_FIXES`.
- **Left as printed (slips in the source):** "2000 barrels" for 3,000 in chapter 3 (E5); "30 years" for about 3 years (E7); 150 years for about 139 (E3); the harmony formula against its figure (E13); "*W* < *S*<sub>*w*</sub>" for *S*<sub>*w*</sub> ≤ *W* (E21); and "lass rule" for "class rule" in chapter 13.

## Sources

- W. Paul Cockshott and Allin Cottrell, *Towards a New Socialism* (Nottingham: Spokesman, 1993), the 2000 Swedish edition text: [by chapter](../Documents/towards_a_new_socialism/README.md), [single file](../Documents/towards_a_new_socialism.md), [PDF](../PDFs/TOWARDS%20A%20NEW%20SOCIALISM.pdf). Every quotation in this note is from that text.
- Leigh Phillips and Michal Rozworski, *The People's Republic of Walmart* (Verso, 2019), argues from corporate planning (Walmart, Amazon) to democratic economic planning, a later version of the point Patrick raises. Not used for any claim above.

## Patrick's brief

> Get the economic model of TNS. Do not compare with the "fundamental princples" book. Create as a new "Notes and research"
>
> - Identify the Marxist terms.
> - Find commentary on unskilled labour, unemployment, firing, students, youth and retirement.
> - How is child care work handled
> - Find the use of equations. Reference them in the research document and define their terms.
> - Investigate a backdoor to Leninism/Trotskyism/Stalinism hidden cryptically via computation justifications and state central planning. Note that central planning occurs in capitalist states these days too via huge corporations, public owned corporations, the military industrial complex, and states themselves.
>
> The goal is to be able to create a conceptual model from this document to explain their proposal without having to read all of the historical context.

Added while the note was being written:

> Also: illness, disability and injury
