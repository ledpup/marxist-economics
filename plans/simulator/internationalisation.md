[↑ Plans](README.md)

---

# Internationalisation

*Stub.* English and Spanish from the start, switchable without a reload. Terms are in the [glossary](glossary.md). Translation keys, Spanish role names and number formats were decided on 2026-11-11 ([gaps 39 to 42](gaps-in-the-brief.md#decided)).

## Rules

- **No text in code or data.** Every string on screen comes from a language file by key: `ui.panel.workers`, `role.cordwainer`, `prod.upper-leather`.
- **Scenario files hold keys, not names.** A scenario made by a user can carry its own names per language. People's names, and units' proper names, are not translated.
- **Messages use ICU MessageFormat**, so a sentence can vary by number: `{count, plural, one {# pair} other {# pairs}}`.
- **Numbers and dates** are formatted by the browser's `Intl` for the current language: 3.18 in English, 3,18 in Spanish; 9 November 2026 / 9 de noviembre de 2026.
- English is British (`en-GB`). *To decide:* which Spanish (`es-ES`, or a Latin American variety).

## Job titles

The model holds no gender ([gap 31](gaps-in-the-brief.md#decided)), but Spanish job titles have one (*zapatero* / *zapatera*). So in Spanish a role is named by its trade or activity, not by the person: *Zapatería*, *Docencia*, *Cuidado infantil*. Sentences about a person avoid the job noun ("Ana · Zapatería · corte", "trabaja en el corte"). The labels are in the [glossary](glossary.md#roles).

## Layout

- Spanish runs about a quarter longer than English. Panels must allow it; no fixed-width buttons.
- No text inside images or map sprites.
- Use logical CSS properties (start/end, not left/right), so a right-to-left language could be added later.

## Tooling

- FormatJS: `react-intl` for the panels, `@formatjs/intl` for anything outside React ([Technology](technology.md#decision)). Its CLI extracts message keys and precompiles messages, so the browser does not download the ICU parser.
- The chosen language is remembered in the browser.
- A test fails the build if a key is missing in either language ([Testing](testing.md)).
- Pseudo-localisation (lengthened, accented text) to find untranslated strings and cramped layouts.

---

[↑ Plans](README.md)
