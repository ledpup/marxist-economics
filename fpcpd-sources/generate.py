"""Generate the Markdown files in fpcpd-sources/ from the quote data below.

The data (authors, bios, works, quotes) lives in this file; the .md files are
output. To change a table, edit the data here and re-run:

    python fpcpd-sources/generate.py

Section titles and anchors are read from the chapter files of the book, so the
"This book" links always match the real headings. A quote that names a section
letter the chapter doesn't have stops the script with a KeyError.

To reuse for another book: point BOOKDIR and CH at its chapter files, replace
the author data, and change OUT.
"""
import re, sys
from pathlib import Path

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
BOOKDIR = ROOT / "Documents" / "fundamental_principles_of_communist_production_and_distribution"
OUT = ROOT / "fpcpd-sources"
BOOKREL = "../Documents/fundamental_principles_of_communist_production_and_distribution/"

CH = {
    "00b": "00b_Foreword_by_the_Editor.md",
    "01": "01_Starting_Points.md",
    "02": "02_The_Social_Democratic_Revision_of_Marxism.md",
    "03": "03_The_Unit_of_Account_in_Communism.md",
    "04": "04_Progress_in_the_Formulation_of_the_Problem.md",
    "05": "05_Libertarian_Communism.md",
    "06": "06_The_Social_Production_Process_in_General.md",
    "07": "07_The_Communist_Production.md",
    "08": "08_Average_Working_Hour_as_Basis_of_Production.md",
    "09": "09_Average_Working_Hour_as_Basis_of_Consumption.md",
    "10": "10_The_General_Social_Work.md",
    "11": "11_Accounting_as_Summary_of_Production_and_Distribution.md",
    "12": "12_The_Abolition_of_the_Market.md",
    "13": "13_The_Expansion_of_Production.md",
    "14a": "14a_The_Control_of_Operational_Life.md",
    "14b": "14b_The_Control_of_Operational_Life_II.md",
    "15": "15_The_Introduction_of_Communism_in_Agriculture.md",
    "17": "17_Final_Considerations.md",
}
CH_LABEL = {"00b": "Foreword (editor)", "14a": "14", "14b": "14 (II)"}


def anchor(text):
    a = text.strip().lower()
    a = re.sub(r"[^\w\- ]", "", a)
    return a.replace(" ", "-")


SECTIONS = {}
for key, fn in CH.items():
    for line in (BOOKDIR / fn).read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            raw = line[3:].strip()
            letter = raw.split(".")[0]
            title = re.sub(r"\[\^\d+\]", "", raw).strip()
            SECTIONS[(key, letter)] = (title, anchor(raw))


def chlabel(ch):
    return CH_LABEL.get(ch, ch.lstrip("0"))


def chsec(ch, sec):
    return chlabel(ch) + (sec or "") if ch != "00b" else "Foreword"


def section_title(ch, sec, short=False):
    if not sec:
        return "–"
    t = SECTIONS[(ch, sec)][0]
    if len(t) > 70:
        t = t[:66].rstrip() + " …"
    return t


def booklink(ch, sec):
    url = BOOKREL + CH[ch]
    if sec:
        url += "#" + SECTIONS[(ch, sec)][1]
    return url


def cell(s):
    return s.replace("|", "\\|").replace("\n", " ").strip()


# ---------------------------------------------------------------- data
# Each author: slug, name, life, bio, bio_src [(label,url)], role, use (how the GIC uses them),
# works {id: dict(title, orig, first, cited, url, refs)}, quotes [dict]
# Quote fields: by, ch, sec, text, work, page, fn, notes, url

MIA = "https://www.marxists.org/archive/"

AUTHORS = []


def author(**kw):
    kw.setdefault("quotes", [])
    kw.setdefault("by_column", False)
    AUTHORS.append(kw)
    return kw


def q(a, ch, sec, text, work, page="", fn="", notes="", url=None, by=""):
    a["quotes"].append(dict(ch=ch, sec=sec, text=text.strip(), work=work, page=page,
                            fn=fn, notes=notes, url=url, by=by))


# ---------------- Marx & Engels
me = author(
    slug="marx-engels", name="Karl Marx and Friedrich Engels", sort="Marx",
    life="Marx 1818–1883 · Engels 1820–1895",
    role="Founders of the theory the GIC builds on",
    bio=("**Karl Marx** (5 May 1818, Trier – 14 March 1883, London) was a German philosopher, social and political "
         "theorist, journalist and revolutionary socialist. He developed historical materialism, and his critique of "
         "political economy, *Das Kapital*, was his major work. "
         "[Wikipedia](https://en.wikipedia.org/wiki/Karl_Marx)\n\n"
         "**Friedrich Engels** (28 November 1820, Barmen – 5 August 1895, London) was a German philosopher, social and "
         "political theorist and revolutionary socialist. He collaborated with Marx for life, co-wrote *The Communist "
         "Manifesto* (1848) with him, and after Marx's death edited and completed the second and third volumes of "
         "*Das Kapital*. [Wikipedia](https://en.wikipedia.org/wiki/Friedrich_Engels)"),
    use=("The GIC's authority throughout. Marx and Engels are quoted to show that the socially average working "
         "hour as unit of account, and labour certificates as the measure of individual consumption, were already "
         "their position. Most works are Marx's alone; *Anti-Dühring*, *The Origin of the Family* and the 1891 "
         "introduction to *The Civil War in France* are Engels's alone; the *Manifesto* is joint. The **By** column "
         "says which."),
    by_column=True,
    works={
        "cap1": dict(by="Marx", title="Capital, Volume I", orig="Das Kapital, Band I", first="1867",
                     cited="pp. 51, 67 (fn. 1), 91, 92, 401 (edition not stated)", url=MIA + "marx/works/1867-c1/index.htm"),
        "cap2": dict(by="Marx (ed. Engels)", title="Capital, Volume II", orig="Das Kapital, Band II", first="1885",
                     cited="pp. 18, 218; ch. 16 III", url=MIA + "marx/works/1885-c2/index.htm"),
        "tsv": dict(by="Marx", title="Theories of Surplus Value, Vol. II", orig="Theorien über den Mehrwert",
                    first="written 1862–63; published 1905–10 (ed. Kautsky)", cited="p. 376, taken from Varga, p. 49",
                    url=MIA + "marx/works/1863/theories-surplus-value/index.htm"),
        "wlc": dict(by="Marx", title="Wage Labour and Capital", orig="Lohnarbeit und Kapital",
                    first="1849 (Engels's revised edition 1891)", cited="p. 12", url=MIA + "marx/works/1847/wage-labour/index.htm"),
        "cwf": dict(by="Marx", title="The Civil War in France", orig="Der Bürgerkrieg in Frankreich", first="1871",
                    cited="p. 40", url=MIA + "marx/works/1871/civil-war-france/index.htm"),
        "gotha": dict(by="Marx", title="Critique of the Gotha Programme", orig="Kritik des Gothaer Programms",
                      first="written 1875; published 1891", cited="part I", url=MIA + "marx/works/1875/gotha/ch01.htm"),
        "manifesto": dict(by="Marx & Engels", title="Manifesto of the Communist Party", orig="Manifest der Kommunistischen Partei",
                          first="1848 (the GIC dates it 1847, when it was written)", cited="p. 26f",
                          url=MIA + "marx/works/1848/communist-manifesto/ch02.htm"),
        "antid": dict(by="Engels", title="Anti-Dühring, Part III, ch. IV “Distribution”",
                      orig="Herrn Eugen Dührings Umwälzung der Wissenschaft", first="1878 (serialised 1877–78)",
                      cited="Part III: Socialism, IV. Distribution", url=MIA + "marx/works/1877/anti-duhring/ch26.htm"),
        "origin": dict(by="Engels", title="The Origin of the Family, Private Property and the State",
                       orig="Der Ursprung der Familie, des Privateigenthums und des Staats", first="1884", cited="p. 94",
                       url=MIA + "marx/works/1884/origin-family/ch09.htm"),
        "cwfintro": dict(by="Engels", title="Introduction to The Civil War in France", orig="Einleitung zu Der Bürgerkrieg in Frankreich",
                         first="1891", cited="", url=MIA + "marx/works/1871/civil-war-france/postscript.htm"),
    },
)
C1 = MIA + "marx/works/1867-c1/"
q(me, "03", "b", "Society can simply calculate how many hours of labor are contained in a steam-engine, a bushel of wheat of the last harvest, or a hundred square yards of cloth of a certain quality. […] Hence, on the assumptions we made above, society will not assign values to products.",
  "antid", "", "22", by="Engels")
q(me, "03", "b", "His inventory contains a list of all the utensils he possesses, the various tasks he has been called upon to perform in order to produce them, and, finally, the working time that certain Quanta of these various products cost him on average. All the relations between Robinson and the things that make up his self-created wealth are so simple and transparent here that even Mr. M. Wirth should be able to understand them without any particular mental effort.",
  "cap1", "91", "23", "Robinson Crusoe passage, ch. 1 §4 (fetishism of commodities).", C1 + "ch01.htm#S4", by="Marx")
q(me, "03", "b", "Let us finally, for a change, imagine an association of free people who work with social means of production and self-confidently spend their many individual labor power as a social labor power. All the provisions of Robinson's work are repeated here, only socially instead of individually.",
  "cap1", "92", "24", "", C1 + "ch01.htm#S4", by="Marx")
q(me, "03", "b", "We will assume, but merely for the sake of a parallel with the production of commodities, that the share of each individual producer in the means of subsistence is determined by his labor time. […] On the other hand, it also serves as a measure of the portion of the common labor borne by each individual, and of his share in the part of the total product destined for individual consumption.",
  "cap1", "51", "25", "Emphasis by the GIC. Quoted again in ch. 10h.", C1 + "ch01.htm#S4", by="Marx")
q(me, "03", "b", "Society distributes labor-power and means of production to the different branches of production. The producers may, for all it matters, receive paper vouchers entitling them to withdraw from the social supplies of consumer goods a quantity corresponding to their labor-time.",
  "cap2", "218", "26", "Capital II, ch. 18 §II.", MIA + "marx/works/1885-c2/ch18.htm", by="Marx")
q(me, "03", "b", "The producers may, for all it matters, receive paper vouchers …",
  "cap2", "218", "", "Repeated to stress that Marx left other methods of distribution open.", MIA + "marx/works/1885-c2/ch18.htm", by="Marx")
q(me, "03", "b", "merely for the sake of a parallel with the production of commodities.",
  "cap1", "51", "", "Repeated for the same reason.", C1 + "ch01.htm#S4", by="Marx")
q(me, "03", "b", "What we have to deal with here is a communist society, not as it has developed on its own foundations, but, on the contrary, just as it emerges from capitalist society […]. He receives a certificate from society that he has furnished such-and-such an amount of labor (after deducting his labor for the common funds); and with this certificate, he draws from the social stock of means of consumption as much as the same amount of labor cost.",
  "gotha", "", "27", "The labour-certificate passage. Emphasis by Marx. Quoted again in ch. 9i.", by="Marx")
q(me, "03", "b", "In a higher phase of communist society, after the enslaving subordination of the individual to the division of labor […] has vanished; […] only then can the narrow horizon of bourgeois right be crossed in its entirety and society inscribe on its banners: From each according to his ability, to each according to his needs!",
  "gotha", "", "28", by="Marx")
q(me, "04", "a", "The money disappears in communist production.",
  "", "", "", "Introduced with “Marx taught it:”. No source given; reads as the GIC's summary of the received view, not a verbatim quotation.", "", by="Marx")
q(me, "04", "a", "… a given quantity of work cannot have a value expressed in its price, in its equivalence with a given quantity of money.",
  "cap2", "18", "29", "Not found in the opening chapters of Capital II on marxists.org; location not verified.", by="Marx")
q(me, "04", "d", "necessary for society to know how much labor each article of consumption requires for its production.",
  "antid", "", "38", "Quoted again in ch. 7b.", by="Engels")
q(me, "06", "a", "Whatever the form of the process of production in a society, it must be a continuous process, must continue to go periodically through the same phases … When viewed, therefore, as a connected whole, and as flowing on with incessant renewal, every social process of production is, at the same time, a process of reproduction.",
  "cap1", "401", "41", "Opening of Capital I, ch. 23 (Simple Reproduction).", C1 + "ch23.htm", by="Marx")
q(me, "07", "a", "… because under the altered circumstances no one can give anything except his labor, and because, on the other hand, nothing can pass to the ownership of individuals, except individual means of consumption.",
  "gotha", "", "42", "Quoted again in ch. 7b and 12e.", by="Marx")
q(me, "07", "b", "to know how much labor each article of consumption requires for its production",
  "antid", "", "43", "Repeats ch. 4d.", by="Engels")
q(me, "07", "b", "Within the co-operative society based on common ownership of the means of production, the producers do not exchange their products; just as little does the labor employed on the products appear here as the value of these products, as a material quality possessed by them, since now, in contrast to capitalist society, individual labor no longer exists in an indirect fashion […] but directly as a component part of total labor.",
  "gotha", "", "44", "The GIC emphasises “co-operative” and inserts the gloss “(the detour of private property - GIC)”.", by="Marx")
q(me, "07", "b", "Here, obviously, the same principle prevails as that which regulates the exchange of commodities, as far as this is exchange of equal values. Content and form are changed, because under the altered circumstances no one can give anything except his labor, and because, on the other hand, nothing can pass to the ownership of individuals, except individual means of consumption.",
  "gotha", "", "45", by="Marx")
q(me, "07", "g", "What, then, is the cost of production of labor-power? […] Thus, the cost of production of simple labor-power amounts to the cost of the existence and propagation of the worker.",
  "wlc", "12", "50", "Long passage, emphasis by the GIC. Footnote 49 adds that Marx assumes price equals value here. Used to show that “life-circumstances communism” keeps capitalist wage laws.",
  MIA + "marx/works/1847/wage-labour/ch04.htm", by="Marx")
q(me, "09", "c", "On this point, I will only say further, that Owen’s “labor-money,” for instance, is no more “money” than a ticket for the theatre. ... the certificate of labor is merely evidence of the part taken by the individual in the common labor, and of his right to a certain portion of the common produce destined for consumption.",
  "cap1", "67, fn. 1", "63", "Footnote in Capital I, ch. 3 §1.", C1 + "ch03.htm", by="Marx")
q(me, "09", "i", "He receives a certificate from society that he has furnished such-and-such an amount of labor (after deducting his labor for the common funds); and with this certificate, he draws from the social stock of means of consumption as much as the same amount of labor cost. The same amount of labor which he has given to society in one form, he receives back in another.",
  "gotha", "", "71", "Repeats ch. 3b.", by="Marx")
q(me, "10", "c", "how much work each product requires to make it.",
  "antid", "", "", "Loose re-quotation of Engels, citing ch. 7b.", by="Engels")
q(me, "10", "g", "… take its place in the museum of antiquities, next to the spinning wheel and the bronze ax.",
  "origin", "94", "75", "Not marked as a quotation: the GIC borrows Engels's image of the state put into the museum of antiquities (Origin, ch. IX).", by="Engels")
q(me, "10", "h", "The mode of this distribution will vary with the productive organization of the community, and the degree of historical development attained by the producers. We will assume, but merely for the sake of a parallel with the production of commodities, that the share of each individual producer in the means of subsistence is determined by his labor time.",
  "cap1", "51", "76", "Repeats ch. 3b.", C1 + "ch01.htm#S4", by="Marx")
q(me, "12", "e", "under the altered circumstances, no one can give anything except his labor, and because, on the other hand, nothing can pass to the ownership of individuals, except individual means of consumption.",
  "gotha", "", "84", "Repeats ch. 7a.", by="Marx")
q(me, "12", "e", "obviously, the same principle prevails as that which regulates the exchange of commodities, as far as this is exchange of equal values, […] content and form are changed …",
  "gotha", "", "85", "Two phrases quoted inline. Repeats ch. 7b.", by="Marx")
q(me, "12", "f", "Of the workers who are involved in the production of consumer goods, a greater part will produce those articles which serve the consumption of the capitalists, landowners and their retinue […]. If the working class is at the helm, if it has the power to produce for itself, it will very quickly and without much effort raise capital (to speak with the vulgar economists) to the level of its own needs.",
  "tsv", "376", "86", "Second-hand: taken from Varga, p. 49.", by="Marx")
q(me, "13", "f", "If we conceive society as being not capitalistic but communistic, there will be no money-capital at all in the first place, not the disguises cloaking the transactions arising on account of it. The question then comes down to the need of society to calculate beforehand how much labor, means of production, and means of subsistence it can invest, without detriment, in such lines of business as for instance the building of railways […].",
  "cap2", "ch. 16 III", "87", "", MIA + "marx/works/1885-c2/ch16.htm#3", by="Marx")
q(me, "14a", "b", "“gradually snatches all capital” … “heavy progressive taxes”",
  "manifesto", "26f", "90", "Phrases inside the GIC's summary of the Manifesto's ten measures, which it reads as a programme of state capitalism.", by="Marx & Engels")
q(me, "14a", "b", "“destroy”, “smash” [the state]",
  "cwf", "", "", "The GIC's summary of Marx's lesson from the Paris Commune. “Smash” is the word Marx used in his letter to Kugelmann of 12 April 1871, as Lenin quotes it in *State and Revolution*.", by="Marx")
q(me, "14a", "b", "in this first place, it filled all posts – administrative, judicial, and educational – by election on the basis of universal suffrage of all concerned, with the right of the same electors to recall their delegate at any time. And in the second place, all officials, high or low, were paid only the wages received by other workers..",
  "cwfintro", "", "91", "Engels's 1891 introduction, not Marx's text.", by="Engels")
q(me, "14a", "e", "The right to appoint and dismiss the members of the commune themselves placed all the officials under the control of the masses, they became the real executive organs of the masses...",
  "cwf", "40", "98", "Used as the section heading. The editor notes it cannot be found in the MEW and points to a fragment in MEW vol. 17, p. 339 (Marx's drafts for The Civil War in France).", by="Marx")

# ---------------- Lenin
L = MIA + "lenin/works/"
lenin = author(
    slug="lenin", name="Vladimir Lenin", sort="Lenin", life="1870–1924",
    role="Bolshevik leader; head of the Soviet government",
    bio=("**Vladimir Lenin** (born Vladimir Ilyich Ulyanov; 22 April 1870, Simbirsk – 21 January 1924, Gorki) was a "
         "Russian revolutionary, politician and Marxist theorist who founded and led the Soviet government, first over "
         "Soviet Russia and then the Soviet Union, until his death. His ideas formed the basis of Leninism. "
         "[Wikipedia](https://en.wikipedia.org/wiki/Vladimir_Lenin)"),
    use=("The main example of state communism. The GIC credits *State and Revolution* for recovering Marx's lessons "
         "from the Paris Commune, but quotes Lenin to show the Bolsheviks aiming at state capitalism (“the postal "
         "service”) and admitting that the state machine ran them."),
    works={
        "staterev": dict(title="The State and Revolution", orig="Государство и революция",
                         first="written Aug–Sep 1917; published 1918", cited="Works vol. 25, p. 432", url=L + "1917/staterev/ch03.htm",
                         refs=["14a b"]),
        "conceal": dict(title="How the Capitalists Conceal Their Profits (Concerning the Issue of Control)", orig="",
                        first="July 1917", cited="Collected Works vol. 25, pp. 140–141", url=L + "1917/jul/12a.htm", refs=["14a a"]),
        "shop": dict(title="Speech at the First Petrograd Conference of Shop Committees", orig="",
                     first="31 May (13 June) 1917", cited="Collected Works vol. 24", url=L + "1917/may/31d.htm"),
        "catastrophe": dict(title="The Impending Catastrophe and How to Combat It", orig="",
                            first="written Sept 1917; published Oct 1917", cited="Collected Works vol. 25", url=L + "1917/ichtci/04.htm"),
        "cec": dict(title="Report on the Immediate Tasks of the Soviet Government (Session of the All-Russia C.E.C.)", orig="",
                    first="29 April 1918", cited="Collected Works vol. 27", url=L + "1918/apr/29.htm"),
        "tasks": dict(title="The Immediate Tasks of the Soviet Government", orig="", first="April 1918",
                      cited="Collected Works vol. 27 (Literature list only)", url=L + "1918/mar/x03.htm", refs=["Literature"]),
        "eleventh": dict(title="Eleventh Congress of the R.C.P.(B.): Political Report of the Central Committee", orig="",
                         first="27 March 1922", cited="Works vol. 33, pp. 279, 288", url=L + "1922/mar/27.htm"),
        "ci4": dict(title="Fourth Congress of the Communist International: report", orig="",
                    first="13 November 1922", cited="Collected Works vol. 33, p. 415f", url=L + "1922/nov/04b.htm"),
    },
)
q(lenin, "02", "a", "To organize the whole economy on the lines of the postal service … that is our immediate aim.",
  "staterev", "432", "4", "Quoted again in ch. 3a.")
q(lenin, "02", "e", "The machine refused to obey the hand that guided it. […] To tell the truth, they are not directing, they are being directed.",
  "eleventh", "279/288", "16")
q(lenin, "02", "e", "I doubt very much whether it can truthfully be said that the Communists are directing that heap. To tell the truth, they are not directing, they are being directed.",
  "eleventh", "288", "20", "Repeated to close the chapter.")
q(lenin, "03", "a", "To organize the whole economy on the lines of the postal service … that is our immediate aim",
  "staterev", "432", "21", "Repeats ch. 2a.")
q(lenin, "14a", "c", "We see a sample of state capitalism in Germany. … But if you reflect even slightly on what it would mean if the foundations of such state capitalism were established in Russia, Soviet Russia, everyone who is not out of his senses … would have to say that state capitalism would be our salvation.",
  "cec", "", "92")
q(lenin, "14a", "c", "If nationalization of the banks is so often confused with the confiscation of private property, it is the bourgeois press, which has an interest in deceiving the public, that is to blame for this widespread confusion. […] Whoever owned fifteen rubles on a savings account would continue to be the owner of fifteen rubles after the nationalization of the banks; and whoever had fifteen million rubles would continue after the nationalization of the banks to have fifteen million rubles in the form of shares, bonds, bills, commercial certificates and so on.",
  "catastrophe", "", "93", "The GIC calls the pamphlet “The Imminent Catastrophe”.")
q(lenin, "14a", "c", "For control over the industry to be effectively carried out, it must be a workers’ control with a workers’ majority in all the leading bodies, and the management must give an account of its actions to all the authoritative workers’ organizations.",
  "shop", "", "94", "Emphasis by Lenin.")
q(lenin, "14a", "e", "We took over the old machinery of state, and that was our misfortune. […] They all came back, but that was our misfortune.",
  "ci4", "415f", "99", "Emphasis by the GIC.")

# ---------------- Trotsky
trotsky = author(
    slug="trotsky", name="Leon Trotsky", sort="Trotsky", life="1879–1940",
    role="Bolshevik leader; head of the Red Army",
    bio=("**Leon Trotsky** (born Lev Davidovich Bronstein; 7 November 1879, Yanovka – 21 August 1940, Mexico City) was a "
         "revolutionary and Soviet leader who played a central role in the 1905 Revolution, the October Revolution and "
         "the Russian Civil War, and built the Red Army. After falling out with Stalin he was exiled in 1929 and later "
         "assassinated in Mexico. [Wikipedia](https://en.wikipedia.org/wiki/Leon_Trotsky)"),
    use=("Quoted on the militarisation of labour in 1920, as proof that a central authority that distributes the "
         "social product must also distribute labour power."),
    works={
        "rk": dict(title="Speeches and decisions on labour duty, printed in *Russische Korrespondenz*", orig="",
                   first="1920", cited="Russische Korrespondenz 1920, No. 10, p. 12 and No. 8/9, p. 39; figures from Pollock, pp. 57–58",
                   url=""),
    },
)
q(trotsky, "12", "b", "If we are to speak seriously of a planned economy, if labor is to be distributed in accordance with the economic plan at the given stage of development, the working class must not lead a nomadic life. It must be moved, distributed, and detached, just like the soldiers.",
  "rk", "No. 10, p. 12", "80")
q(trotsky, "12", "b", "that the skilled worker leaving the army, with the workbook in hand, in the name of the country's production plan, must go where his presence is required.",
  "rk", "No. 8/9, p. 39", "81", "A decision of the Central Committee for General Labour Duty, December 1919, chaired by Trotsky.")
q(trotsky, "12", "b", "the transfer of labor from one operational unit to another can be carried out in accordance with the production plan...",
  "rk", "as above", "", "Decision of the Committee on Labour Duty (same source).")
q(trotsky, "12", "b", "In the major industries, we have 1,150,000 workers, but in reality, only 850,000 workers... […] They have left.",
  "rk", "No. 10, p. 12", "82")

# ---------------- Zinoviev
zin = author(
    slug="zinoviev", name="Grigory Zinoviev", sort="Zinoviev", life="1883–1936",
    role="Bolshevik leader; chairman of the Comintern",
    bio=("**Grigory Zinoviev** (23 September 1883, Yelizavetgrad – 25 August 1936, Moscow) was a Russian revolutionary "
         "and Soviet politician, a close associate of Lenin before 1917, chairman of the Communist International from "
         "1919 to 1926, and a Politburo member for much of the 1920s. He was executed after a show trial. "
         "[Wikipedia](https://en.wikipedia.org/wiki/Grigory_Zinoviev)"),
    use="Quoted second-hand (via Pollock) on the Bolshevik hope of abolishing money during war communism.",
    works={
        "zwoelf": dict(title="Twelve Days in Germany", orig="Zwölf Tage in Deutschland",
                       first="1920 (Moscow); Hamburg edition 1921", cited="p. 74, taken from Pollock, p. 73", url=""),
    },
)
q(zin, "12", "a", "If the value of money is falling in Russia, it is certainly very difficult for us to bear... […] We're heading for the complete abolition of money.",
  "zwoelf", "74", "79", "Second-hand: quoted from Pollock, *Die planwirtschaftlichen Versuche*, p. 73. Written after the USPD's Halle congress of October 1920.")

# ---------------- Tomsky
tomsky = author(
    slug="tomsky", name="Mikhail Tomsky", sort="Tomsky", life="1880–1936",
    role="Head of the Soviet trade unions",
    bio=("**Mikhail Tomsky** (born Mikhail Pavlovich Yefremov; 31 October 1880, Kolpino – 22 August 1936, Bolshevo) was "
         "a factory worker, trade unionist and Bolshevik politician who chaired the All-Union Central Council of Trade "
         "Unions in the 1920s and sat on the Politburo. Associated with the Right Opposition, he fell in 1928 and took "
         "his own life in 1936 to avoid arrest. [Wikipedia](https://en.wikipedia.org/wiki/Mikhail_Tomsky)"),
    use="Quoted as the voice of the Soviet unions: wage differences, the refusal to back wage demands, and compulsory union membership.",
    works={
        "7th": dict(title="Speech at the 7th Congress of Trade Unions", orig="", first="December 1926",
                    cited="Protokol, p. 49 (translated from Dutch; English version unknown)", url=""),
        "prinz": dict(title="Principles of the union", orig="Prinzipien der Gewerkschaft", first="not given",
                      cited="p. 69", url=""),
    },
)
q(tomsky, "02", "e", "The foreign visitors are amazed at nothing as much as at the wage differences between educated and unskilled workers that in Russia … are bigger as nowhere else in Western Europe.",
  "7th", "", "17", "Footnote 17 also points to the GIC brochure *De Beweging van het kapitalistisch Bedrijfsleven*, ch. 2 “The Marxist wage laws”.")
q(tomsky, "02", "e", "While the communist in the capitalist countries must support the wage demands, he cannot do so under the proletarian dictatorship. ... Here the economic demands of the workers must be reconciled with the development of the productive forces and socialist accumulation.",
  "7th", "49", "18", "About the wage demands of July 1926.")
q(tomsky, "14a", "d", "The workers accepted the withholding of contributions as an order from above, completely independent of their will.",
  "prinz", "69", "97")
q(tomsky, "14a", "d", "official obligation",
  "prinz", "", "", "Tomsky's phrase for union membership, used twice by the GIC.")

# ---------------- Larin & Kritsman
larin = author(
    slug="larin-kritsman", name="Yuri Larin and Lev Kritsman", sort="Larin", life="Larin 1882–1932 · Kritsman 1890–c. 1937",
    role="Soviet economists of war communism",
    bio=("**Yuri Larin** (17 June 1882, Simferopol – 14 January 1932, Moscow) was a founding member of the Supreme "
         "Council of the National Economy (Vesenkha) in December 1917, and in March 1918 drafted the decree on the "
         "management of nationalised industry. [Wikipedia](https://en.wikipedia.org/wiki/Yuri_Larin)\n\n"
         "**Lev Kritsman** (also Kritzman; 1890 – c. 1937) was a Soviet economist and agrarian expert, a Menshevik from "
         "1905 who joined the Bolsheviks in 1918, author of *The Heroic Period of the Great Russian Revolution*, a "
         "defence of war communism, and head of the Agrarian Institute of the Communist Academy. He died in the purges. "
         "No Wikipedia article; see [Marxists Internet Archive glossary](https://www.marxists.org/glossary/people/k/r.htm) "
         "and [Encyclopedia.com](https://www.encyclopedia.com/history/encyclopedias-almanacs-transcripts-and-maps/kritzman-lev-natanovich).\n\n"
         "The GIC takes the quote from **Arthur Rosenberg** (19 December 1889, Berlin – 7 February 1943, New York), a "
         "Marxist historian and Reichstag member 1924–28, whose *A History of Bolshevism* appeared in 1932. "
         "[Wikipedia](https://en.wikipedia.org/wiki/Arthur_Rosenberg)"),
    use="Quoted second-hand on why workers' control under the Bolsheviks was a half-measure.",
    works={
        "wl": dict(title="Economic life and the economic construction in Soviet Russia, 1917 to 1920",
                   orig="Wirtschaftsleben und wirtschaftlicher Aufbau in Sowjet-Russland 1917–1920", first="1921",
                   cited="taken from A. Rosenberg, *Geschichte des Bolschewismus* (1932), p. 114", url=""),
    },
)
q(larin, "14a", "c", "However, workers' control proved to be a half-measure and, therefore, not feasible. As a slogan, workers' control signified the growing and at the same time still insufficient power of the proletariat, that is, it was an expression of the movement's weakness, which has not yet been overcome.",
  "wl", "", "95", "Second-hand: quoted from Rosenberg, p. 114.")

# ---------------- Kautsky
kautsky = author(
    slug="kautsky", name="Karl Kautsky", sort="Kautsky", life="1854–1938",
    role="Chief theorist of German Social Democracy",
    bio=("**Karl Kautsky** (16 October 1854, Prague – 17 October 1938, Amsterdam) was a leading theorist of orthodox "
         "Marxism and for decades the chief intellectual voice of the SPD and the Second International. He drafted the "
         "theoretical part of the SPD's 1891 Erfurt Programme and edited *Die Neue Zeit*. "
         "[Wikipedia](https://en.wikipedia.org/wiki/Karl_Kautsky)"),
    use=("The GIC's main opponent on the working-time calculation. Kautsky describes labour money accurately, then "
         "declares it impossible in practice; the GIC answers his objections one by one in chapter 8."),
    works={
        "doctrines": dict(title="The Economic Doctrines of Karl Marx", orig="Karl Marx' ökonomische Lehren", first="1887",
                          cited="p. 20", url=MIA + "kautsky/1903/economic/index.htm"),
        "prolrev": dict(title="The Proletarian Revolution and its Programme", orig="Die proletarische Revolution und ihr Programm",
                        first="1922", cited="Dietz, 2nd ed. 1922, pp. 317–321", url="https://archive.org/details/dieproletarische00kaut/"),
    },
)
q(kautsky, "04", "a", "Value is the historical category that applies only to the production of commodities.", "doctrines", "20", "30")
q(kautsky, "04", "c", "indispensable as a measure of value for bookkeeping and the calculation of exchange ratios in a socialist society […] as a means of circulation",
  "prolrev", "318", "36", "Two phrases quoted inline. The same passage is quoted in full in ch. 8a.")
q(kautsky, "04", "c", "whether it will ever be more than a pious wish, similar to the Millennial Kingdom", "prolrev", "317", "37",
  "On the “second phase” of communism.")
q(kautsky, "07", "e", "higher wages should be paid for unpleasant or heavy work than for pleasant and light work.", "prolrev", "318", "46")
q(kautsky, "08", "a", "The continuity of money is indispensable as a measure of value for accounting and the calculation of exchange ratios in a socialist society.",
  "prolrev", "318", "52", "Same passage as ch. 4c, translated differently.")
q(kautsky, "08", "a", "[…] could one not directly define human labor itself as a measure of value and create labor money that directly certifies work done? […] But could it also be done in practice?",
  "prolrev", "318", "53", "Kautsky's own sketch of labour money. The GIC emphasises his admission that with it “any exploitation would be impossible”.")
q(kautsky, "08", "a", "to calculate for each product the amount of work it has cost from its first beginnings until its completion, including transport and other ancillary works.",
  "prolrev", "318", "54")
q(kautsky, "08", "a", "...the estimation of the goods according to work contained in them, (even) the most tremendous and perfect statistical apparatus cannot ... achieve.",
  "prolrev", "321", "55")
q(kautsky, "08", "d", "The different copies of the same type would have different prices, those produced under less favorable conditions higher than the others. […] They would all have to have the same price, and that would have to be calculated, not according to work really spent, but according to the socially necessary work.",
  "prolrev", "319", "61", "Emphasis by the GIC.")
q(kautsky, "08", "e", "And if you were finished, you would have to start all over again, since the technical conditions in some industries have changed in the meantime.",
  "prolrev", "318f", "62")

# ---------------- Hilferding
hilf = author(
    slug="hilferding", name="Rudolf Hilferding", sort="Hilferding", life="1877–1941",
    role="SPD theorist; German Finance Minister",
    bio=("**Rudolf Hilferding** (10 August 1877, Vienna – 11 February 1941, Paris) was an Austrian-born Marxist economist "
         "and the chief theoretician of the SPD in the Weimar Republic. He was German Finance Minister in 1923 and "
         "1928–29; his major work, *Das Finanzkapital*, appeared in 1910. "
         "[Wikipedia](https://en.wikipedia.org/wiki/Rudolf_Hilferding)"),
    use=("Source of the “General Cartel”, which the GIC treats as the generally accepted picture of communism: a "
         "central authority that distributes the product without money or a unit of account."),
    works={
        "fincap": dict(title="Finance Capital", orig="Das Finanzkapital", first="1910", cited="2nd ed., Vienna 1920; ch. 1 and p. 314",
                       url=MIA + "hilferding/1910/finkap/index.htm"),
        "kiel": dict(title="The tasks of Social Democracy in the Republic (speech at the SPD party congress, Kiel)",
                     orig="Die Aufgaben der Sozialdemokratie in der Republik", first="May 1927", cited="p. 6", url=""),
    },
)
q(hilf, "02", "a", "That means nothing other than that our generation is faced with the problem of transforming, with the help of the state, with the help of conscious social regulation, this economy organized and led by the capitalists into an economy led by the democratic state.",
  "kiel", "6", "6")
q(hilf, "04", "b", "All capitalist production is consciously regulated by an authority that determines the extent of production in all spheres. […] The cartel distributes the product.",
  "fincap", "314", "33", "The “General Cartel”. The GIC inserts “(here: arbitrary - G.I.C.)”.", MIA + "hilferding/1910/finkap/ch15.htm")
q(hilf, "04", "b", "How, where, how much, by what means, will new products be made from the available natural and artificial production conditions ... the communal, district and national commissioners of socialist society decide […].",
  "fincap", "1", "35", "Quoted again in ch. 5d in another translation.", MIA + "hilferding/1910/finkap/ch01.htm")
q(hilf, "05", "d", "… all decisions as to method, place, quantity, and available tools involved in the production of new goods are made by … the local regional or national commissars of the socialist society. […]",
  "fincap", "ch. 1", "40", "Same passage as ch. 4b (English marxists.org translation). Set beside Faure to show that his plan is the same.", MIA + "hilferding/1910/finkap/ch01.htm")

# ---------------- Cunow
cunow = author(
    slug="cunow", name="Heinrich Cunow", sort="Cunow", life="1862–1936",
    role="SPD theorist; editor of *Die Neue Zeit*",
    bio=("**Heinrich Cunow** (11 April 1862, Schwerin – 20 August 1936) was an SPD politician and prominent Marxist "
         "theorist. Having first opposed the First World War, he came to argue that German imperialism was progressive, "
         "and edited the theoretical journal *Die Neue Zeit*. [Wikipedia](https://en.wikipedia.org/wiki/Heinrich_Cunow)"),
    use="Quoted, as a reformist, to show that Marx wanted production regulated by free associations, not the state.",
    works={
        "theorie": dict(title="Marx's theory of history, society and the state, vol. 1",
                        orig="Die Marxsche Geschichts-, Gesellschafts- und Staatstheorie, Band 1", first="1920",
                        cited="Vorwärts, Berlin 1920, pp. 309, 340", url=""),
    },
)
q(cunow, "02", "b", "not by the state, but through the connection of the free associations of a socialist society.",
  "theorie", "309", "7", "Cunow's account of Marx's view. Emphasis in the book.")
q(cunow, "02", "b", "Accordingly, the party congress declared itself against nationalization; for social democracy and state socialism are “irreconcilable opposites”.",
  "theorie", "340", "8", "Follows the Liebknecht quote, which Cunow also supplies.")

# ---------------- Liebknecht
lieb = author(
    slug="liebknecht", name="Wilhelm Liebknecht", sort="Liebknecht", life="1826–1900",
    role="Founder of the SPD",
    bio=("**Wilhelm Liebknecht** (29 March 1826, Giessen – 7 August 1900, Berlin) was a principal founder of the SPD. "
         "He co-founded the Social Democratic Workers' Party with August Bebel in 1869 and was the main architect of the "
         "1875 Gotha congress that merged it with the Lassalleans. "
         "[Wikipedia](https://en.wikipedia.org/wiki/Wilhelm_Liebknecht)"),
    use="“The old Liebknecht” stands for the early SPD's rejection of state socialism.",
    works={
        "speech": dict(title="Speech on bringing railways, coal mines and large industry into state administration",
                       orig="", first="1880s–1890s (date not given)", cited="via Cunow (see that note)", url=""),
    },
)
q(lieb, "02", "b", "The more bourgeois society realizes that in the long run, it cannot defend itself against the onslaught of socialist ideas, the closer we are to the moment when state socialism will be proclaimed in full earnestness, and the last struggle that social democracy will have to fight will be fought out under the battle cry: “Here social democracy-- There state socialism”.",
  "speech", "", "", "No footnote of its own; the next footnote (8) cites Cunow, p. 340. See [Cunow](cunow.md).")

# ---------------- Parvus
parvus = author(
    slug="parvus", name="Alexander Parvus", sort="Parvus", life="1867–1924",
    role="Russian-German Marxist in the SPD",
    bio=("**Alexander Parvus** (born Israel Lazarevich Gelfand; 27 August 1867, Berezino – 12 December 1924, Berlin) was "
         "a Russian-born Marxist theorist, journalist and activist, prominent in the SPD. He co-developed the theory of "
         "permanent revolution with Trotsky and in 1917 helped arrange Lenin's return to Russia. "
         "[Wikipedia](https://en.wikipedia.org/wiki/Alexander_Parvus)"),
    use="“The well-known left-wing Marxist”, quoted to show the left of social democracy also saw socialism as state production.",
    works={
        "staat": dict(title="The State, Industry and Socialism", orig="Der Staat, die Industrie und der Sozialismus",
                      first="1910 (Wikipedia; the GIC's footnote says 1919)", cited="p. 112", url=""),
    },
)
q(parvus, "02", "a", "how easy the transition from large-scale industry to state production can be.", "staat", "112", "5")

# ---------------- Oppenheimer
opp = author(
    slug="oppenheimer", name="Franz Oppenheimer", sort="Oppenheimer", life="1864–1943",
    role="Sociologist and economist; liberal socialist",
    bio=("**Franz Oppenheimer** (30 March 1864, Berlin – 30 September 1943, Los Angeles) was a social theorist and "
         "economist whose work centred on the sociology of the state. He is best known for *Der Staat* (1907) and is "
         "associated with liberal socialism. [Wikipedia](https://en.wikipedia.org/wiki/Franz_Oppenheimer)"),
    use="A non-Marxist the GIC agrees with: for Marx, society is “ripe” for socialism only as a whole.",
    works={
        "beck": dict(title="Contribution to the anthology *Ways and goals of socialisation*, ed. H. Beck",
                     orig="Wege und Ziele der Sozialisierung", first="c. 1919 (not verified)", cited="pp. 16–17", url=""),
    },
)
q(opp, "02", "b", "From Marx's point of view, this is ... pure nonsense. For him, a socialist society can only be “ripe” as a whole.",
  "beck", "16/17", "", "No footnote; the source is named in the text. On the Bolshevik idea of “ripe” enterprises.")

# ---------------- Goldschmidt
gold = author(
    slug="goldschmidt", name="Alfons Goldschmidt", sort="Goldschmidt", life="1879–1940",
    role="German journalist and economist; visited Soviet Russia in 1920",
    bio=("**Alfons Goldschmidt** (28 November 1879, Gelsenkirchen – January 1940, Mexico City) was a German journalist, "
         "economist and university lecturer. He co-founded the League for Proletarian Culture in 1919, co-edited the "
         "*Räte-Zeitung*, and arrived in Moscow on 1 May 1920. [Wikipedia](https://en.wikipedia.org/wiki/Alfons_Goldschmidt)"),
    use="An eyewitness source for early Soviet economic policy: the printing of money and congress resolutions on nationalisation.",
    works={
        "wo": dict(title="The Economic Organization of Soviet Russia", orig="Die Wirtschaftsorganisation Sowjet-Russlands",
                   first="1920", cited="Rowohlt, Berlin 1920, pp. 42, 133, 138", url="",
                   refs=["2b (congress resolution)", "2d (2nd Economic Congress)"]),
    },
)
q(gold, "02", "d", "Notes are fabricated ... You can't print enough notes. […]", "wo", "138", "11",
  "On the deliberate inflation meant to abolish money. Goldschmidt is also the source for two congress quotes: see [Organisations and periodicals](organisations-and-periodicals.md).")

# ---------------- Varga
varga = author(
    slug="varga", name="Eugen Varga", sort="Varga", life="1879–1964",
    role="Finance commissar of the Hungarian Soviet Republic; later Soviet economist",
    bio=("**Eugen Varga** (born Eugen Weiss; 6 November 1879, Budapest – 7 October 1964, Moscow) was a Hungarian "
         "communist revolutionary and Soviet economist. He was People's Commissar of Finance in the Hungarian Soviet "
         "Republic in 1919, then fled to the Soviet Union and became an economic adviser to Stalin. "
         "[Wikipedia](https://en.wikipedia.org/wiki/Eugen_Varga)"),
    use=("The GIC's main source on Soviet Hungary, where state communism was put into practice. Quoted on the "
         "economy in kind, pricing policy and state control."),
    works={
        "probleme": dict(title="The economic problems of the proletarian dictatorship",
                         orig="Die wirtschaftspolitischen Probleme der proletarischen Diktatur", first="1920",
                         cited="Carl Hoym; pp. 42, 49, 67/68, 78, 122, 126, 138, 147", url="",
                         refs=["9f (p. 122)", "9h (p. 126)", "12f (p. 49)"]),
        "kommunismus": dict(title="Article in *Kommunismus*, 2nd year, no. 9/10", orig="", first="1921",
                            cited="", url="", refs=["4c"]),
    },
)
q(varga, "02", "d", "With the expansion of the state economy, first of all, the money disappears from the traffic between public enterprises. […] Money also dies off as a means of circulation.",
  "probleme", "138", "12")
q(varga, "02", "d", "The rapid and continued devaluation of money is disadvantageous in so far as it prevents the stabilization of wage levels, causes wage movements and conflicts between the workers of the state and the proletarian state itself, forces them to constant wage increases, makes the calculation very difficult, makes it impossible to draw up a proper state budget, and especially to adhere to it.",
  "probleme", "138", "14")
q(varga, "09", "f", "transformation and organizational restructuring in Hungary were faster and more vigorous than in Russia.", "probleme", "78", "66")
q(varga, "09", "f", "a lot of things could be organized centrally that have to be decentralized due to the huge expansion of Russia.", "probleme", "78", "67")
q(varga, "09", "h", "generation of workers corrupted by capitalism and educated in a greedy egoistic ideology.", "probleme", "42", "68")
q(varga, "09", "h", "But since for the time being there are still wages and prices of money […] the state fixing of prices",
  "probleme", "147", "", "Two phrases quoted inline.")
q(varga, "09", "h", "In principle, therefore, all state goods must be sold at “social cost price”. By this, we mean the cost price plus a supplement sufficient to cover the maintenance costs of the non-working people, plus a supplement to enable real accumulation.",
  "probleme", "147", "69", "Emphasis by Varga.")
q(varga, "14b", "a", "The proletarians who administer the expropriated operational units fall too easily into the belief that the units are their property, not that of the whole society. This makes a well-functioning control particularly important since it is also an excellent means of education ...",
  "probleme", "67/68", "100", "Long passage on the Hungarian system of state auditors.")

# ---------------- Neurath
neurath = author(
    slug="neurath", name="Otto Neurath", sort="Neurath", life="1882–1945",
    role="Philosopher and economist; advocate of calculation in kind",
    bio=("**Otto Neurath** (10 December 1882, Vienna – 22 December 1945, Oxford) was an Austrian philosopher of "
         "science, sociologist and political economist, a leading figure of the Vienna Circle, an advocate of economic "
         "calculation in kind rather than in money, and inventor of the ISOTYPE pictorial statistics. He ran a central "
         "planning office in Munich and was imprisoned after the Bavarian Soviet Republic fell. "
         "[Wikipedia](https://en.wikipedia.org/wiki/Otto_Neurath)"),
    use="The leading theorist of the “natural economy” without a unit of account, which the GIC rejects.",
    works={
        "wpnr": dict(title="Economic Plan and Calculation in Kind", orig="Wirtschaftsplan und Naturalrechnung", first="1925",
                     cited="Berlin 1925, p. 84", url="", refs=["4c", "7e (“life circumstances”)"]),
    },
)
q(neurath, "02", "d", "The doctrine of the socialist economy knows only one single producer-distributor-society - who, without profit or loss account, without circulation of money - be it metal money or labor money - organizes production based on an economic plan, and distributes the standard of living according to socialist rules, without foundation of any unit of account.",
  "wpnr", "84", "13", "Emphasis on “without … any unit of account” in the book.")

# ---------------- Leichter
leichter = author(
    slug="leichter", name="Otto Leichter", sort="Leichter", life="1897–1973",
    role="Austrian Social Democrat; theorist of socialist accounting",
    bio=("**Otto Leichter** (22 February 1897, Vienna – 14 February 1973, New York) was an Austrian socialist, "
         "journalist and author who worked for the Social Democratic Workers' Party (SDAP) and its *Arbeiter-Zeitung*. "
         "He went into exile after 1934 and 1938, and from 1957 to 1971 was UN correspondent for the Deutsche "
         "Presse-Agentur. His first wife was the social scientist Käthe Leichter, murdered by the Nazis in 1942. "
         "[Wikipedia (German)](https://de.wikipedia.org/wiki/Otto_Leichter); no English article."),
    use=("The most-quoted author after Marx. The GIC praises him as “the first fruit of Weber's criticism”: he bases "
         "production on working-time accounting and describes cost accounting between plants. But he keeps wage "
         "differences and central price policy, so the GIC concludes his scheme leads to state capitalism."),
    works={
        "wr": dict(title="The economic account in the socialist society", orig="Die Wirtschaftsrechnung in der sozialistischen Gesellschaft",
                   first="1923", cited="Vienna 1923, pp. 22f, 31, 52f, 54, 61, 64, 65f, 66, 68, 75, 76, 100f, 101", url=""),
    },
)
q(leichter, "04", "c", "almost exactly match", "wr", "", "", "Leichter's words on how far Maurice Bourguin's ideas (c. 1900) match his own.")
q(leichter, "07", "e", "All that remains is the purely technical difficulty, also present in capitalism, of setting the wages for the individual jobs, but that does not mean any complication in comparison with the capitalist method.",
  "wr", "76", "47")
q(leichter, "07", "f", "Differently qualified workers […] need a different amount of effort to reproduce their labor power. […] All this must be included in the various assessments of the labor power.",
  "wr", "61", "48", "Emphasis and the gloss “(port workers, civil servants, engineers - GIC)” by the GIC.")
q(leichter, "08", "b", "... there are relations between the individual production sites, and this relationship will continue to exist in the world as long as there is a division of labor, and the division of labor in this higher sense will continue to develop with the progress of technology.",
  "wr", "54", "56")
q(leichter, "08", "b", "All material conditions of production, all semi-finished materials, all raw materials, all auxiliary materials, which are delivered from other production sites to the processing plant, will be debited, invoiced to it.",
  "wr", "68", "57", "Quoted again in ch. 11b.")
q(leichter, "08", "b", "For this, however, it is necessary to record the results of all operations separately and to do so - no matter whether in capitalist or socialist economy - as if each operation had its own entrepreneur who wants to become clear about the economic result of production. Therefore, there is very strict accounting within the cartel […].",
  "wr", "52f", "58", "Emphasis by the GIC.")
q(leichter, "08", "b", "Capitalist accounting, when carried out perfectly and smoothly in a factory, can at any time accurately determine the value of a semi-finished product, a piece of work in production, the costs of each individual operation. […] It is also one of the great achievements of the capitalist accounting method to have made possible these subtleties in the economic accounts.",
  "wr", "22f", "59")
q(leichter, "08", "c", "At first sight, one might think that each individual production plant is quite independent. Still, if one looks closer, one will clearly see the umbilical cord through which the individual plant is connected with the rest of the economy and its management.",
  "wr", "100f", "60")
q(leichter, "09", "d", "In truth... the image of society presented here is based on the idea of the allocation of goods “in natura” in proportion to the work done by each individual. Labor money is only a form of assignment of the share of the national product chosen for economic-technical reasons.",
  "wr", "75", "64", "Emphasis by the GIC.")
q(leichter, "09", "d", "the work done by each individual", "wr", "75", "", "Repeated: the GIC calls this phrase “a poisonous snake in the grass”.")
q(leichter, "09", "d", "in a way represent the subsistence minimum […] the normal, scientifically calculated and balanced life ration",
  "wr", "64", "", "Two phrases quoted inline, on the “nutrition physiologists”.")
q(leichter, "09", "d", "any appointed manager of the operational unit bears personal responsibility for him ; he can be removed without further ado, just like a capitalist manager who does not meet the demands placed on him. He will then only receive the minimum income guaranteed by society if he is “unemployed”, or he will be used in a correspondingly lower and therefore, worse paid position. […]",
  "wr", "101", "65")
q(leichter, "10", "d", "They will then make a differential rent - or, capitalistically speaking, a surplus profit, which of course cannot be given to this factory alone, but - again, capitalistically speaking - must be taxed away.",
  "wr", "31", "72")
q(leichter, "10", "d", "Each production plant will, therefore, have to reckon with a rate for general administrative costs of the entire factory, to be determined annually when the overall balance sheet, or - in socialist terms - the business plan, is drawn up. ... The total sum of the administrative costs […] will be related to some variable, probably best of all to the total number of hours worked in production and distribution, and the resulting ratio will be added to the wage totals spent when calculating the production costs so that the cost price of the commodity also includes the costs of society.",
  "wr", "65f", "73", "Emphasis by the GIC.")
q(leichter, "10", "e", "It would, of course, be an injustice and would have almost the effect of an indirect tax if one wanted to add the same general expense rate to all goods […]. It will be one of the most important tasks of the economic parliament or the supreme economic management to set the general rate of expenses for each industry or product, but always in such a way that the entire expenses of society are brought in.",
  "wr", "66", "74")
q(leichter, "11", "b", "All material conditions of production […] supplied by other production plants to the processing plant are charged, invoiced to it. The question of whether this will result in cash payment with working hours or accounting charges, i.e., “cashless” transactions, will be best solved by practice.",
  "wr", "68", "77", "Same passage as ch. 8b, translated differently.")

# ---------------- Horn
horn = author(
    slug="horn", name="Erich Horn", sort="Horn", life="dates not found",
    role="“Bourgeois writer” on the communal economy",
    bio=("**Erich Horn** wrote *Die ökonomischen Grenzen der Gemeinwirtschaft* (Halberstadt, 1928). No Wikipedia "
         "article or other biography was found."),
    use="Quoted for calling communism, as Marxists had described it, “a negative system”: no money, no value, no market, no price.",
    works={
        "grenzen": dict(title="The economic limits of the communal economy", orig="Die ökonomischen Grenzen der Gemeinwirtschaft",
                        first="1928", cited="Halberstadt 1928, pp. 3, 51–52", url="",
                        refs=["4a (pp. 51–52, paraphrased)"]),
    },
)
q(horn, "04", "a", "a negative system", "grenzen", "3", "31")

# ---------------- Block
block = author(
    slug="block", name="Herbert Block", sort="Block", life="dates not found",
    role="Economist; author of a study of Marx's theory of money",
    bio=("**H. Block** is Herbert Block, whose *Die Marxsche Geldtheorie* (Jena: Gustav Fischer, 1926) began as a "
         "doctoral thesis at the University of Freiburg ([KIT library record](https://katalog.bibliothek.kit.edu/bib/479808)). "
         "No Wikipedia article or other biography was found."),
    use=("“The economist H. Block” stands for the bourgeois case that without the market there can be no economic "
         "calculation. In ch. 4c the GIC spells him “Bloch”."),
    works={
        "geld": dict(title="The Marxian theory of money", orig="Die Marxsche Geldtheorie", first="1926",
                     cited="Jena 1926, pp. 121–122, 125", url="", refs=["4c (p. 125)"]),
    },
)
q(block, "12", "d", "If the individual exchange is abolished, the production is necessarily social, so the products are necessarily social as well. […] As long as it cannot be shown how the market mechanism is to be replaced, an economic calculation in the common economy, i.e., rational socialism, is unthinkable.",
  "geld", "121–122", "83")

# ---------------- Faure
faure = author(
    slug="faure", name="Sébastien Faure", sort="Faure", life="1858–1942",
    role="French anarcho-communist",
    bio=("**Sébastien Faure** (6 January 1858, Loire – 14 July 1942, Royan) was a French anarcho-communist and "
         "freethought activist, a leading proponent of the “anarchist synthesis” for organising anarchist federations. "
         "Wikipedia's lead also notes that he was a convicted sex offender. "
         "[Wikipedia](https://en.wikipedia.org/wiki/S%C3%A9bastien_Faure)"),
    use=("The GIC's example of libertarian communism. It argues that Faure's “free agreement” ends in a main "
         "administration that assigns production and consumption, the same as Hilferding's General Cartel."),
    works={
        "mc": dict(title="My Communism (Universal Happiness)", orig="Mon communisme (Le bonheur universel)", first="1921",
                   cited="Dutch translation *Het universele geluk*, Roode Bibliotheek, Zandvoort 1927; pp. 5, 6, 213, 215, 216, 218, 334",
                   url=""),
    },
)
q(faure, "05", "b", "This work describes the life of a great nation under libertarian communist rule in a simple, clear and attractive form and is intended to show that the anarchists have a richly studied social plan.", "mc", "5", "39")
q(faure, "05", "b", "the free and fraternal agreement", "mc", "6", "")
q(faure, "05", "b", "This whole organization is based on the animating principle of free cooperation", "mc", "213", "", "Page of the Dutch translation.")
q(faure, "05", "c", "People search, grope, summarize and try out the results of the various methods. The agreement appears, offers itself, pushes itself through its results and wins.", "mc", "334", "")
q(faure, "05", "c", "Nature's example is there: clear and obvious. Everything is there connected by free and spontaneous agreement . . . […]", "mc", "334", "")
q(faure, "05", "d", "it is, therefore, necessary above all to determine the total of the need and the quantity of each need.", "mc", "215", "")
q(faure, "05", "d", "what part of the production they can keep for themselves.", "mc", "216", "")
q(faure, "05", "d", "The main administration knows how large the total production and the total demand is and must, therefore, inform each district committee how much product it can dispose of and how much means of production it must procure.", "mc", "218", "")

# ---------------- Müller-Lehning
lehning = author(
    slug="muller-lehning", name="Arthur Müller-Lehning", sort="Lehning", life="1899–2000",
    role="Dutch anarcho-syndicalist writer and historian",
    bio=("**Arthur Lehning** (Paul Arthur Müller-Lehning; 23 October 1899, Utrecht – 1 January 2000, Lys-Saint-Georges) "
         "was a Dutch writer and historian associated with anarchist politics. He received the P. C. Hooft Award. "
         "[Wikipedia](https://en.wikipedia.org/wiki/Arthur_Lehning)"),
    use=("The GIC agrees with his demand that anarchism answer “what to do the day after the revolution”, but argues "
         "that his syndicalist programme gives the unions, not the workers' councils, control of production."),
    works={
        "as": dict(title="Anarcho-syndicalism", orig="Anarcho-syndicalisme", first="1927",
                   cited="Gem. Synd. Verb. 1927, pp. 4–11, 18", url="", refs=["5e (p. 4, paraphrased)"]),
    },
)
q(lehning, "05", "e", "how the realization of anarcho-syndicalism comes about after the revolution.", "as", "5", "")
q(lehning, "05", "e", "but one must also examine how it must be carried out.", "as", "6", "")
q(lehning, "05", "e", "but what this initiative had to be, what the masses had to do, today and tomorrow, everything remained blurred and little positive.", "as", "7", "")
q(lehning, "05", "e", "Many manifestos may have appeared, but few could give a clear and unambiguous answer to the question of daily practice.", "as", "8", "")
q(lehning, "05", "e", "We may say that the Russian Revolution once and forever asked the question: What are the practical and economic foundations of a society without a wage system? […] The old anarchist slogans, however much truth they contain and however often they are repeated, do not solve any of the problems posed by real life.",
  "as", "10", "", "Emphasis by the GIC.")
q(lehning, "05", "e", "Without these practical realities, all propaganda remains negative, and all ideals remain utopias. This is the lesson anarchism has to learn from history, and it cannot be sufficiently repeated by the tragic development of the Russian revolution.", "as", "11", "")
q(lehning, "05", "e", "The economic organizations have the goal of expropriating the state and capitalism. […] The basis must be the operation; the operating organization must form the nucleus for the new economic social organization.", "as", "18", "", "Emphasis by the GIC.")
q(lehning, "05", "e", "The purpose of economic organizations is to expropriate the state and capitalism.", "as", "18", "", "Repeats the previous quote in another wording.")
q(lehning, "05", "e", "The economic organizations have as their goal the expropriation of the state and capitalism.", "as", "18", "", "Repeated a second time.")

# ---------------- Struik
struik = author(
    slug="struik", name="Dirk Jan Struik", sort="Struik", life="1894–2000",
    role="Dutch mathematician and communist",
    bio=("**Dirk Jan Struik** (30 September 1894, Rotterdam – 21 October 2000, Belmont, Massachusetts) was a Dutch-born "
         "mathematician and historian of mathematics who settled in the United States in 1934. A committed Marxist, he "
         "joined the Communist Party of the Netherlands in 1919 and stayed a member for life. "
         "[Wikipedia](https://en.wikipedia.org/wiki/Dirk_Jan_Struik)"),
    use="Quoted at the start of the book to show how new the idea of the workers' councils was in 1919.",
    works={
        "nt": dict(title="Overview of the K.P.H. resolution on the councils, in *De Nieuwe Tijd*", orig="", first="1919",
                   cited="De Nieuwe Tijd, vol. 1919, p. 466", url=""),
    },
)
q(struik, "01", "a", "Nothing shows more clearly the progress we have made in recognizing the laws of the social revolution than our explanation of the council system. […] If ever Mehring's word that the “intuition of the acting masses can be more ingenious than the greatest genius,” is true, it is in this case.",
  "nt", "466", "", "The GIC presents this as from Struik's overview of the resolution adopted by the K.P.H. (Communist Party of Holland), so the words may be the party's rather than Struik's own. It quotes [Franz Mehring](https://en.wikipedia.org/wiki/Franz_Mehring) and mentions Rosa Luxemburg's mass-strike pamphlet and Trotsky's book on 1905.")

# ---------------- Canne Meijer
canne = author(
    slug="canne-meijer", name="Henk Canne Meijer", sort="Canne Meijer", life="1890–1962",
    role="Co-founder of the GIC; editor of the *Fundamental Principles*",
    bio=("**Henk Canne Meijer** (30 December 1890 – 28 December 1962) was a Dutch metalworker who left party communism "
         "after the Russian Revolution for the council communist opposition. He co-founded the GIC in September 1927 "
         "and edited the *Fundamental Principles* before publication. There is no Wikipedia article on him; see the "
         "[Group of International Communists](https://en.wikipedia.org/wiki/Group_of_International_Communists) article, "
         "the [libcom.org biography](https://libcom.org/article/henk-canne-meijer) and his writings at the "
         "[Marxists Internet Archive](https://www.marxists.org/archive/canne-meijer/index.htm)."),
    use="Quoted by the editor, Hermann Lueer, in his 2020 foreword; not by the GIC itself.",
    works={
        "origins": dict(title="The Origins of the Movement for Workers' Councils in Germany",
                        orig="German edition: Die Arbeiterrätebewegung in Deutschland (1918–1933), Edition Soziale Revolution 1985",
                        first="1938", cited="German edition, 1985", url=MIA + "canne-meijer/index.htm"),
    },
)
q(canne, "00b", "", "the last message that the revolutionary movements of the 1st half of the 20th century have left us.",
  "origins", "", "1", "Canne Meijer on the *Fundamental Principles*.")
q(canne, "00b", "", "There is no point in discussing “federalism or centralism” if you don't first show what the economic basis of this “federalism” or this “centralism” will be. […] If one proceeds in this way, it is very likely that the alternative “federalism or centralism” appears to be the wrong question.",
  "origins", "", "2", "The editor introduces this as “the words of the GIC”; the footnote gives Canne Meijer's book as the source.")

# ---------------- Organisations and periodicals
orgs = author(
    slug="organisations-and-periodicals", name="Organisations, congresses and periodicals", sort="~",
    life="", role="Resolutions and reports without a single author",
    bio=("Quotations whose source is a congress, party, union or newspaper rather than a named person. Links go to "
         "Wikipedia where an article exists: the [Supreme Council of the National Economy](https://en.wikipedia.org/wiki/Supreme_Soviet_of_the_National_Economy) "
         "(Vesenkha), [Trud](https://en.wikipedia.org/wiki/Trud), the Soviet trade-union newspaper, and the Spanish "
         "anarcho-syndicalist union [CNT](https://en.wikipedia.org/wiki/Confederaci%C3%B3n_Nacional_del_Trabajo)."),
    use="Used as documentary evidence on Soviet Russia (chapters 2, 14) and on Spanish anarcho-syndicalism (chapter 5).",
    by_column=True,
    works={
        "ec1": dict(by="1st All-Russian Congress of Economic Councils", title="Resolution on nationalisation", orig="",
                    first="1918", cited="via Goldschmidt, p. 42", url=""),
        "ec2": dict(by="2nd Economic Congress", title="Decision on calculating state expenditure by value", orig="",
                    first="1919", cited="via Goldschmidt, p. 133", url=""),
        "rcp11": dict(by="Russian Communist Party (B.), 11th Congress", title="The role and tasks of trade unions under the conditions of the New Economic Policy",
                      orig="", first="March–April 1922", cited="German edition, *Die KPdSU in Resolutionen und Beschlüssen*, vol. 2",
                      url="http://www.verlag-benariobaum.de/WebRoot/Store/Shops/es151175/MediaGallery/PDF-Dateien/Die_KPdSU_in_Resolutionen_und_Beschluessen_Band_2.pdf"),
        "trud": dict(by="Central Council of Trade Unions", title="Statement in *Trud*", orig="", first="1928",
                     cited="Trud 1928, No. 31 (also Nos. 32, 159, 280 for statistics in ch. 2e)", url=""),
        "tu1918": dict(by="Trade union congress", title="Resolution of 20 April 1918", orig="", first="1918",
                       cited="Courier of the People's Commissariat for Labour, 1918, No. 5/7", url=""),
        "synd": dict(by="*De Syndicalist* (Dutch syndicalist paper)", title="Reports", orig="", first="1931",
                     cited="19 September 1931; 29 August 1931", url=""),
        "rp": dict(by="*La Révolution prolétarienne* (French syndicalist magazine)", title="Report on the C.N.T. congress of June 1931",
                   orig="", first="July 1931", cited="", url=""),
        "rk": dict(by="*Russische Korrespondenz*", title="Report on the 1919 decree on consumer cooperatives", orig="",
                   first="20 January 1920", cited="via Varga, p. 126", url="", refs=["9h (fn 70)"]),
        "gic1": dict(by="GIC", title="Lines of development in farming", orig="Ontwikkelingslijnen in het boerenbedrijf",
                     first="1930", cited="De Nieuwe Weg, 1930",
                     url="https://www.aaap.be/Pages/Pamphlets-GIC-1930-De-Ontwikkeling-Van-Het-Boerenbedrijf.html",
                     refs=["1 (intro)", "15a (fn 101)"]),
        "gic2": dict(by="GIC", title="The movement of capitalist business life", orig="De Beweging van het kapitalistisch Bedrijfsleven",
                     first="not given", cited="ch. 2, “The Marxist wage laws”", url="", refs=["2e (fn 17)"]),
    },
)
q(orgs, "02", "b", "It is necessary to move from the nationalization of individual enterprises (so far 304) to the consequential nationalization of the industry. Nationalization may not be an “occasional” nationalization.",
  "ec1", "42", "9", "Emphasis by the GIC.", by="1st Congress of Economic Councils")
q(orgs, "02", "d", "the calculation of the value of the product becomes more necessary every day […] calculate the most important state expenditures according to the value of the products",
  "ec2", "133", "", "Two phrases quoted inline.", by="2nd Economic Congress")
q(orgs, "02", "e", "... with the urgent necessity to increase labor productivity, to work lossless, and to achieve profitability of each enterprise ... inevitably leads to a certain contradiction of interests between the working masses and the directors […]. Therefore, concerning socialized enterprises, trade unions have an unconditional duty to defend the interests of the workers ...",
  "rcp11", "", "19", "", by="RCP(B), 11th Congress")
q(orgs, "02", "e", "not guided by the interests of workers, but by the financial interests of industry",
  "trud", "No. 31", "", "On the Supreme Economic Council and occupational safety.", by="Central Council of Trade Unions")
q(orgs, "05", "e", "...the union's control over production.", "synd", "19 Sept 1931", "", "", by="De Syndicalist")
q(orgs, "05", "e", "The Congress shows that the C.N.T. is an enormous force. The only thing that remains is to specify and put into practice its measures for the takeover of the industry.",
  "rp", "", "", "", by="La Révolution prolétarienne")
q(orgs, "05", "e", "The Congress has decided to demand the expropriation of all domains over 50 hectares by handing over land, livestock, and equipment to the farmworkers' unions.",
  "rp", "", "", "", by="La Révolution prolétarienne")
q(orgs, "05", "e", "There are several militants in the National Committee of the C.N.T. who do not believe that the C.N.T. in its present condition is ready to take over production.",
  "synd", "29 Aug 1931", "", "", by="De Syndicalist")
q(orgs, "14a", "d", "Conflicts between workers and management must be immediately submitted to the central administration of the Federation of Trade Unions for decision. If the workers refuse to submit to the decisions of the trade union bodies, they must be immediately expelled from the union and bear all the consequences resulting from it.",
  "tu1918", "", "96", "The footnote adds that expulsion meant dismissal and loss of food ration cards.", by="Trade union congress, 1918")

# ---------------- Referenced, not quoted
MENTIONED = [
    ("Max Weber", "1864–1920",
     "German sociologist, historian, jurist and political economist who helped found sociology. [Wikipedia](https://en.wikipedia.org/wiki/Max_Weber)",
     "*Economy and Society* (*Wirtschaft und Gesellschaft*), 1921–22", "4c, 8a",
     "With Mises, the bourgeois critic whose case that an economy needs a unit of account “defeated” calculation in kind."),
    ("Ludwig von Mises", "1881–1973",
     "Austrian-American economist of the Austrian school and advocate of classical liberalism. [Wikipedia](https://en.wikipedia.org/wiki/Ludwig_von_Mises)",
     "*Economic Calculation in the Socialist Commonwealth*, 1920; *Socialism* (*Die Gemeinwirtschaft*), 1922 (Literature list: 2nd ed., Jena 1932)", "4c, 8a, Literature",
     "As for Weber."),
    ("Henryk Grossman", "1881–1950",
     "Polish-German Marxist economist of the Frankfurt School who revived Marx's theory of crisis and breakdown. [Wikipedia](https://en.wikipedia.org/wiki/Henryk_Grossman)",
     "*The Law of Accumulation and Breakdown of the Capitalist System* (*Das Akkumulations- und Zusammenbruchsgesetz des kapitalistischen Systems*), 1929, p. 603", "4b (fn 34)",
     "Recommended as “a very good critique” of the General Cartel based on value theory."),
    ("Friedrich Pollock", "1894–1970",
     "German social scientist, co-founder of the Frankfurt Institute for Social Research, known for his theory of state capitalism. [Wikipedia](https://en.wikipedia.org/wiki/Friedrich_Pollock)",
     "*Die planwirtschaftlichen Versuche in der Sowjetunion 1917–1927* (*Attempts at Planned Economy in the Soviet Union*), 1929", "7c, 12a–b (fn 79, 82), 14a (fn 89), Literature",
     "Source for Soviet facts and for the Zinoviev quote. Footnote 89 was added by the editor."),
    ("Maurice Bourguin", "1856–1910",
     "French professor of law at Douai and Lille. [Wikipedia](https://en.wikipedia.org/wiki/Maurice_Bourguin)",
     "*Les systèmes socialistes et l'évolution économique*, 1904", "4c",
     "Named (as “Bourquin”) as working out labour-time accounting around 1900, according to Leichter."),
    ("G. D. H. Cole", "1889–1959",
     "English political theorist, economist and historian who developed guild socialism. [Wikipedia](https://en.wikipedia.org/wiki/G._D._H._Cole)",
     "*Self-Government in Industry*, 1917 (German ed. Berlin 1921); *Guild Socialism Restated*, 1920", "17d, Literature",
     "Cole's guild socialism is an example of utopian “constructions” of socialism."),
    ("Maurice Dobb", "1900–1976",
     "English Marxist economist at Cambridge. [Wikipedia](https://en.wikipedia.org/wiki/Maurice_Dobb)",
     "*Russian Economic Development since the Revolution* (the Literature list gives London, 1929)", "Literature",
     "Listed only."),
    ("Rosa Luxemburg", "1871–1919",
     "Polish-born German Marxist theorist and revolutionary, co-founder of the Spartacus League and the KPD. [Wikipedia](https://en.wikipedia.org/wiki/Rosa_Luxemburg)",
     "*The Accumulation of Capital*, 1913; *The Mass Strike*, 1906 (inside the Struik quote)", "1a, 15a",
     "Cited for the break-up of the closed peasant economy."),
    ("Herman Gorter", "1864–1927",
     "Dutch poet and council communist theorist, a key figure in the KAPD. [Wikipedia](https://en.wikipedia.org/wiki/Herman_Gorter)",
     "Poem *De Arbeidersraad* (The Workers' Council)", "1a (fn 3)",
     "The poem ends this section in the Dutch edition; the translator left it out."),
]


# ---------------------------------------------------------------- output
def work_label(a, wid):
    if not wid:
        return "no source given"
    w = a["works"][wid]
    t = w["title"]
    return f"*{t}*" if "*" not in t else t


def used_in(a, wid):
    items = []
    for qq in a["quotes"]:
        if qq["work"] == wid:
            s = chsec(qq["ch"], qq["sec"])
            if s not in items:
                items.append(s)
    items += a["works"][wid].get("refs", [])
    return ", ".join(items)


def quote_row(a, qq):
    w = a["works"].get(qq["work"], {}) if qq["work"] else {}
    url = qq["url"] if qq["url"] is not None else w.get("url", "")
    links = f"[This book]({booklink(qq['ch'], qq['sec'])})"
    if url:
        links += f" · [Original]({url})"
    src = work_label(a, qq["work"])
    if qq["page"]:
        p = qq["page"]
        src += f", {p}" if not p[0].isdigit() else f", p. {p}"
    if qq["fn"]:
        src += f" (fn {qq['fn']})"
    cols = []
    if a["by_column"]:
        cols.append(qq["by"])
    cols += [chlabel(qq["ch"]), section_title(qq["ch"], qq["sec"]), links, qq["text"], src, qq["notes"]]
    return "| " + " | ".join(cell(c) for c in cols) + " |"


def write_author(a):
    lines = [f"# {a['name']}", "", "[↑ Sources quoted in the *Fundamental Principles*](README.md)", "", a["bio"], "",
             f"**In the *Fundamental Principles*:** {a['use']}", "", "## Works cited", ""]
    by = a["by_column"]
    head = (["By"] if by else []) + ["Work", "Original title", "First published", "Cited by the GIC as", "Used in", "Online"]
    lines.append("| " + " | ".join(head) + " |")
    lines.append("| " + " | ".join("---" for _ in head) + " |")
    for wid, w in a["works"].items():
        online = f"[Link]({w['url']})" if w.get("url") else "–"
        row = ([w.get("by", "")] if by else []) + [w["title"], f"*{w['orig']}*" if w["orig"] and "*" not in w["orig"] and not w["orig"].startswith("German") else (w["orig"] or "–"),
                                                   w["first"], w["cited"] or "–", used_in(a, wid) or "–", online]
        lines.append("| " + " | ".join(cell(c) for c in row) + " |")
    lines += ["", "## Quotes", "",
              "Quotes longer than two sentences are shortened; `[…]` marks a cut made here, while `...` and `…` are the book's own. "
              "Wording follows the book's English translation, which may differ from the linked original translation.", ""]
    head = (["By"] if by else []) + ["Chapter", "Section", "Links", "Quote", "Source", "Notes"]
    lines.append("| " + " | ".join(head) + " |")
    lines.append("| " + " | ".join("---" for _ in head) + " |")
    order = list(CH)
    for qq in sorted(a["quotes"], key=lambda x: order.index(x["ch"])):
        lines.append(quote_row(a, qq))
    lines += ["", "---", "", "[↑ Sources quoted in the *Fundamental Principles*](README.md)", ""]
    (OUT / f"{a['slug']}.md").write_text("\n".join(lines), encoding="utf-8")


def write_readme():
    people = [a for a in AUTHORS if a["slug"] != "organisations-and-periodicals"]
    people.sort(key=lambda a: (-len(a["quotes"]), a["sort"]))
    total = sum(len(a["quotes"]) for a in AUTHORS)
    L = ["# Sources quoted in the *Fundamental Principles*", "",
         "Who the Group of International Communists (GIC) quotes in *[Fundamental Principles of Communist Production and Distribution]"
         "(../Documents/fundamental_principles_of_communist_production_and_distribution/README.md)*, and where. "
         "The book was written collectively by the GIC (first draft by Jan Appel, edited by Henk Canne Meijer), published in German in 1930, "
         "and revised for the Dutch second edition of 1935. The English text in this repository is Hermann Lueer's 2020 translation.", "",
         "Each author has a file with a short biography (from Wikipedia, linked), a table of the works the GIC cites with their "
         "original publication dates, and a table of every quotation with links to its place in this book and to the original "
         "text online where one exists. Marx and Engels share one file, with a **By** column saying which of them wrote each work.", "",
         f"The book contains {total} quotations: from {len(people)} authors (two of them pairs: Marx and Engels, Larin and Kritsman) "
         "and from a number of congresses and periodicals.", "",
         "## Authors", "",
         "| Author | Life | Who | Quotes | Chapters |", "| --- | --- | --- | --- | --- |"]
    order = list(CH)
    for a in people + [orgs]:
        chs = []
        for qq in sorted(a["quotes"], key=lambda x: order.index(x["ch"])):
            c = chlabel(qq["ch"]) if qq["ch"] != "00b" else "Foreword"
            if c not in chs:
                chs.append(c)
        L.append(f"| [{a['name']}]({a['slug']}.md) | {a['life'] or '–'} | {a['role']} | {len(a['quotes'])} | {', '.join(chs)} |")
    L += ["", "## Mentioned or listed but not quoted", "",
          "Authors the GIC names, cites in a footnote or lists under Literature without quoting them.", "",
          "| Author | Life | Who | Work and date | Where | How the GIC uses them |", "| --- | --- | --- | --- | --- | --- |"]
    for m in MENTIONED:
        L.append("| " + " | ".join(cell(c) for c in m[:1]) + " | " + " | ".join(cell(c) for c in m[1:]) + " |")
    L += ["", "## Quotes in reading order", "",
          "Every quotation in the order it appears in the book. Follow the author link for the text of the quote.", "",
          "| Chapter | Section | Author | Work | Opening words | In the book |", "| --- | --- | --- | --- | --- | --- |"]
    allq = []
    for a in AUTHORS:
        for qq in a["quotes"]:
            allq.append((a, qq))
    allq.sort(key=lambda t: order.index(t[1]["ch"]) + (ord(t[1]["sec"]) / 1000 if t[1]["sec"] else 0))
    for a, qq in allq:
        who = qq["by"] if qq["by"] else a["name"]
        words = re.sub(r"^[\W_]+", "", qq["text"]).split()
        opening = " ".join(words[:7]) + " …"
        L.append("| " + " | ".join(cell(c) for c in [
            chlabel(qq["ch"]), section_title(qq["ch"], qq["sec"]), f"[{who}]({a['slug']}.md)",
            work_label(a, qq["work"]), opening, f"[Go]({booklink(qq['ch'], qq['sec'])})"]) + " |")
    L += ["", "## Method and caveats", "",
          "- Quotes were collected from the chapter files: block quotes, `»…«` guillemets, and inline quoted phrases with a source. "
          "Statistics tables, the Appendix's chronology, and quotation marks used only for irony are left out.",
          "- Pages and editions are those the GIC (or the editor) cites; they are not checked against the originals unless a note says so.",
          "- Publication dates are first publication in the original language. Where the book's date differs, the note says so.",
          "- “Original” links go to the Marxists Internet Archive or another free copy. Each Marx, Engels, Lenin and Hilferding link was "
          "checked to contain the quoted passage, except where a note says otherwise.",
          "- Biographies summarise the lead of each person's Wikipedia article (read October 2026). Where there is no article, the note says "
          "so and links another source.",
          "- These files are generated by [generate.py](generate.py), which holds all the data. Edit the data there and run "
          "`python fpcpd-sources/generate.py` rather than editing the tables by hand.", "",
          "---", "", "[↑ Back to the collection](../README.md)", ""]
    (OUT / "README.md").write_text("\n".join(L), encoding="utf-8")


OUT.mkdir(exist_ok=True)
for a in AUTHORS:
    write_author(a)
write_readme()
print(len(AUTHORS), "files +README;", sum(len(a["quotes"]) for a in AUTHORS), "quotes")
