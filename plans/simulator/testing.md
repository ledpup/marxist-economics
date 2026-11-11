[↑ Plans](README.md)

---

# Testing

*Stub.* The book's own figures are the first test oracle.

## Formulas against the book

| Test | Expected |
| --- | --- |
| Production equation ([E1](../../notes-opus5_5/fundamental-principles-economic-model.md#e1-the-production-equation-one-unit)) | 1,250 + 61,250 + 62,500 = 125,000 hours; 3.125 a pair |
| Social average ([E3](../../notes-opus5_5/fundamental-principles-economic-model.md#e3-the-social-average-production-time)) | 652,500 ÷ 205,000 = 3.18 a pair; overs and unders sum to zero |
| Payout factor ([E7](../../notes-opus5_5/fundamental-principles-economic-model.md#e7-the-payout-factor-fic)) | (600 − 58) ÷ (600 + 50) = 0.83 |
| Payout factor with expansion ([E10](../../notes-opus5_5/fundamental-principles-economic-model.md#e10-the-payout-factor-with-expansion)) | (600 − 58 − 75.8) ÷ 650 = 0.717 |
| By-product method | Hides at 2,000 instead of 14,000: leather 18,000; shoes 113,000 hours for 40,000 pairs |

## The scenario

- The [book check](shoe-scenario.md#two-versions) version of the shoe scenario, run for a year with no random variation, gives the shoe factory 125,000 hours for 40,000 pairs.
- The [invariants](accounting.md#invariants) hold after every tick.
- A crew with a slower pace gives a higher production time per pair on hand work, about the same on machine work, and the same certificates per hour worked.
- With child care and students switched off, the payout factor rises by what their hours took.
- With retirement and sick pay switched off (H = 0), the payout factor rises, and total claims (factor × (L + L<sub>p</sub> + H)) still equal the product left for consumption.

## Determinism

Within one build ([gap 35](gaps-in-the-brief.md#decided)):

- The same scenario and seed give the same hash of the state and books after a simulated year.
- Saving and loading mid-run, then continuing, gives the same hash as running straight through.
- Running at a different play speed gives the same hash.
- Replaying a run with commands given mid-run gives the same hash.
- With dishonesty off, what happened and what the books say agree after every tick ([gap 45](gaps-in-the-brief.md#decided)).

## Other

- Performance: ticks per second at 100, 1,000 and 10,000 people.
- Every translation key exists in both languages.

---

[↑ Plans](README.md)
