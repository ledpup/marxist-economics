[↑ Plans](README.md)

---

# Technology

Options for running the simulation in a browser, judged on what the brief asks: animate many simple objects, zoom, click anything, stay efficient at scale, and fit Patrick's languages (C#, Blazor, Vue, React, JavaScript).

## What any choice must allow

- The [simulation engine](simulation-engine.md) runs **apart from the drawing**: in a Web Worker in the browser, and on its own for tests and batch runs.
- The map draws thousands of sprites at 60 frames a second with zoom, pan and picking (knowing what was clicked).
- Panels, forms and tables (books, selection, settings) are ordinary web UI, where an SPA framework is better than a game engine.
- Text comes from translation files ([Internationalisation](internationalisation.md)).
- It can be hosted as a static site.

## Options

| Option | Simulation | Map | Panels | For | Against |
| --- | --- | --- | --- | --- | --- |
| **A. TypeScript + PixiJS** | TypeScript in a Web Worker | PixiJS (WebGL/WebGPU 2D), with a viewport plug-in for zoom and pan | Vue or React | Fastest 2D drawing on the web for the effort; one language throughout; small download; huge ecosystem | Sim speed limited by JavaScript, though fine to tens of thousands of agents with typed arrays |
| **B. C# core + PixiJS** | C# library, compiled to WebAssembly (Blazor WebAssembly) | PixiJS via JavaScript interop | Blazor | Patrick's main language; the core also runs in .NET for tests and server batch runs | Two languages; each frame's positions must cross the interop boundary (batch them into one array); several MB of .NET runtime to download |
| **C. Blazor + canvas only** | C# | HTML canvas via interop, or SkiaSharp for Blazor | Blazor | All C# | Drawing through interop is slow past a few thousand objects; zoom and picking written by hand |
| **D. Godot** | GDScript or C# | Godot 2D | Godot UI | A real engine: camera, input, tile maps, animation | Panels and tables are clumsier than web UI. For much of Godot 4's life, C# projects could not be exported to the web; check the current state before choosing C# here |
| **E. Bevy (Rust)** | Rust, ECS | Bevy 2D, WebGL2/WebGPU | Bevy UI or an HTML overlay | ECS suits many agents; Rust in WebAssembly is fast and deterministic | A new language; UI panels are hard; long compile times |
| **F. Unity WebGL** | C# | Unity 2D | Unity UI | C#; mature engine | Large download and slow start in the browser; poor on mobile; licensing; overkill for 2D |
| **G. deck.gl** | Any, in a worker | deck.gl layers (WebGL) | Vue or React | Built for drawing and picking millions of points and lines on a zoomable map; strong if the town becomes a region | A data-visualisation library, not a game one: animation and sprites take more work |

## Decision

**Option A**: TypeScript, Vite, PixiJS for the map, the engine in a Web Worker, React for panels, FormatJS (`react-intl`) for translations, Vitest for tests.

- It gets a clickable, zoomable map with moving crates on screen soonest, which is what tests the idea.
- It handles the target scale, about 10,000 people, every one an agent ([gap 36](gaps-in-the-brief.md#decided)): TypeScript holds that many in typed arrays, and PixiJS draws that many sprites at 60 frames a second.
- The engine is plain TypeScript with no browser dependencies, behind a message interface. If it later needs more speed, it can be ported to Rust or C# compiled to WebAssembly without touching the map or the panels. The fixed random algorithm and integer books ([Simulation engine](simulation-engine.md#random-numbers-and-determinism)) make two ports checkable against each other: same seed, same books.
- **React** rather than Vue because LLMs write it most reliably: the most training data, and hooks have been stable since 2019. The map stays in plain PixiJS, not `@pixi/react`; React draws only the panels.
- **FormatJS** rather than i18next because ICU MessageFormat is its native syntax ([Internationalisation](internationalisation.md#rules)). i18next needs a plug-in for ICU, and its own `{{count}}` and `_one`/`_other` syntax would creep in. FormatJS formats numbers and dates with the browser's `Intl`, and its core (`@formatjs/intl`) also works outside React, for any text the PixiJS map needs.
- Pin versions in the app's `AGENTS.md` (React 19, PixiJS 8, and so on). PixiJS 8 changed its API (async `Application.init()`, a new Graphics API), and LLMs often write version 7 code.
- **Option B** would be the choice if a C# core mattered more than a single language. It would keep the same split: core in C#, map in PixiJS.
- **Option G** is worth revisiting if the map grows to a region with hundreds of thousands of people.

## Notes

- **Code:** the app lives in this repository, in a `simulator/` folder at the root.
- **Hosting:** GitHub Pages, at `ledpup.github.io/marxist-economics/`. A GitHub Actions workflow builds the app with Vite and publishes it on each push to `main`. Vite's `base` is set to `/marxist-economics/`, and the Pages source to "GitHub Actions".
- Sharing memory between the worker and the map (SharedArrayBuffer) needs the page to be served with cross-origin isolation headers. GitHub Pages does not let you set headers. Until it is needed, the worker posts a snapshot each frame. When it is needed, either a service worker adds the headers (`coi-serviceworker`), or the site moves to a host that sets them (Cloudflare Pages, Netlify).

---

[↑ Plans](README.md)
