# Homey App Development — Onboarding Kit

> **Goal:** By the end of week 4, you can read the Homey Apps SDK fluently, scaffold an app from scratch, build drivers, Flow cards and widgets, validate and publish — and explain what you built.
> **Time budget:** ~4 weeks at ~6 focused learning hours per day. Understanding beats speed.

---

## 0. What is Homey?

Homey is a **smart home platform** built by Athom. It comes in two flavors:

- **Homey Pro** — a physical hub that runs locally in the user's home
- **Homey Cloud** — a cloud-hosted version for users without the hub

Either way, Homey connects devices from many brands and protocols (Wi-Fi, Zigbee, Z-Wave, Bluetooth, Matter, Thread, 433 MHz, Infrared), and lets users automate them using a visual "Flow" editor.

A **Homey App** is a Node.js (or Python) bundle that:

- Adds support for new devices (drivers)
- Exposes Flow cards (triggers, conditions, actions) to the automation editor
- Can include dashboard widgets, settings pages, OAuth flows, etc.

Apps are distributed through the **Homey App Store**, or installed directly via the Homey CLI during development.

**Visualize it like this:**

```
┌──────────────────────────────┐
│        Homey Hub             │
│                              │
│  ┌────────────────────────┐  │
│  │     Your Homey App     │  │
│  │                        │  │
│  │  ┌──────────────────┐  │  │       ┌────────────────┐
│  │  │ Drivers          │──┼──┼───────│ Physical device│
│  │  │  (one per        │  │  │       │ (light, lock,  │
│  │  │   product type)  │  │  │       │  sensor, ...)  │
│  │  └──────────────────┘  │  │       └────────────────┘
│  │  ┌──────────────────┐  │  │
│  │  │ Flow cards       │──┼──┼───► Flow editor (user)
│  │  └──────────────────┘  │  │
│  │  ┌──────────────────┐  │  │
│  │  │ Widget (web UI)  │──┼──┼───► Dashboard (user)
│  │  └──────────────────┘  │  │
│  │  ┌──────────────────┐  │  │
│  │  │ App settings     │──┼──┼───► Settings page (user)
│  │  └──────────────────┘  │  │
│  └────────────────────────┘  │
└──────────────────────────────┘
```

---

## 1. Prerequisites & Day-1 setup

Install these **in this order**. If something breaks, ask before googling for an hour.

1. **Node.js 22.x** via [nvm](https://github.com/nvm-sh/nvm) — not brew, not the installer from nodejs.org. Homey Pro runs Node 22.
   ```bash
   nvm install 22
   nvm use 22
   node --version   # should print v22.x
   ```
2. **Docker Desktop**
3. **Homey CLI** — your daily driver:
   ```bash
   npm install -g homey
   homey --version
   ```
4. **An Athom account** — sign up at https://my.homey.app.
5. **A Homey (physical or virtual)** linked to your account. Start with cloud only.
6. **Git** + SSH key linked to GitHub.
7. **VS Code** with the ESLint and Prettier extensions. Optional: Homey extension

### Verify your setup

You're ready when all of these succeed:

- [ ] `node --version` prints `v22.x`
- [ ] `homey --version` prints a version string >= 4.2.0
- [ ] `homey login` succeeds (opens a browser, you log in)
- [ ] `homey app create` scaffolds a new app without errors
- [ ] `homey app run` on that scaffold shows the app on your Homey and streams logs. (You'll need running docker engine on the background)

---

## 2. The 4-week learning path

Each week has **reading**, **videos**, a short **exercise**, and a **demo** to your buddy.

### Week 1 — Homey as a platform, SDK fundamentals

**Read, in order:**

1. [Welcome to the Homey Apps SDK](https://apps.developer.homey.app) — bookmark the landing page
2. [Getting Started](https://apps.developer.homey.app/the-basics/getting-started) — do it end-to-end, don't just read it
3. [App](https://apps.developer.homey.app/the-basics/app) — what every file in a Homey app folder is for
4. [App Manifest](https://apps.developer.homey.app/the-basics/app/manifest) — every field explained
5. [Homey Compose](https://apps.developer.homey.app/homey-compose) — how `app.json` gets generated. **Don't hand-edit `app.json`**.
6. [Permissions](https://apps.developer.homey.app/the-basics/app/permissions) — what your app can and can't do
7. [Internationalization](https://apps.developer.homey.app/the-basics/app/internationalization) — how to localize

**Watch:**

- [Homey Developer Series — Getting Started](https://www.youtube.com/watch?v=v_RUamZzby8) — official, chaptered, ~20 min. Note: recorded for SDK v2, so some syntax differs from v3, but the concepts all transfer.
- [ULTIMATE Homey Pro Beginner's Guide](https://www.youtube.com/watch?v=nMIpy3zuwPA) — watch at 1.5×. This is the **user's** perspective. You need to understand what a Flow looks like to non-developers before you build cards for them.
- The [Homey YouTube channel](https://www.youtube.com/@homey) — browse for any recent uploads tagged "Developer".

**Exercise W1:**
Scaffold an app `com.<yourname>.hello`. No drivers. Make it install, show a valid app icon, and print `"Hello from MyApp"` in `app.js → onInit()`. Confirm the log line appears in the terminal while `homey app run` is active.

**Demo:** Record a screenshot recording and share as demo.

---

### Week 2 — Drivers, Devices, Capabilities

This is the core abstraction. Learn it until you can draw it on a whiteboard.

**Read:**

1. [Drivers & Devices](https://apps.developer.homey.app/the-basics/devices) — full page
2. [Pairing](https://apps.developer.homey.app/the-basics/pairing) — including custom pairing views
3. [Capabilities](https://apps.developer.homey.app/the-basics/devices/capabilities) — system, custom, and sub-capabilities
4. [Device Capabilities reference](https://apps-sdk-v3.developer.homey.app/tutorial-device-capabilities.html) — skim, it's a reference
5. [Device class (SDK v3 reference)](https://apps-sdk-v3.developer.homey.app/Device.html) — bookmark; you'll come back daily
6. [Driver class (SDK v3 reference)](https://apps-sdk-v3.developer.homey.app/Driver.html)

**Key concepts to lock down:**

- **Driver** (one per product *type*) vs **Device** (one per paired physical thing) — one driver, many devices
- `registerCapabilityListener` (Homey → device: user toggles something) vs `setCapabilityValue` (device → Homey: state changed externally)
- **System capabilities** (`onoff`, `measure_power`, `dim`, `measure_temperature`, ...) vs **custom capabilities** (you define)
- When to store what: **device settings** (user-editable), **device store** (internal, persistent), **device data** (immutable identity)

**Exercise W2:**
Add a virtual driver `mock_sensor` to your `com.<yourname>.hello` app. It should:

- Use a virtual pair template (`list_devices`), no real wireless discovery
- Expose the capabilities `measure_temperature` and `measure_humidity`
- In `device.js → onInit()`, start a timer that updates both values every 10 seconds with random realistic readings (15–25 °C, 30–70 %)

**Demo:** Pair two instances in the Homey app, open Homey Insights, show both devices producing live graphs. Record a screenshot recording and share as demo.

---

### Week 3 — Flow, Widgets, and the Web API

**Read:**

1. [Flow](https://apps.developer.homey.app/the-basics/flow) — triggers, conditions, actions
2. [Flow Arguments](https://apps.developer.homey.app/the-basics/flow/arguments) — especially `autocomplete` and `device` argument types
3. [Flow — Device cards](https://apps.developer.homey.app/the-basics/flow/devices) — cards scoped to a specific device
4. [Widgets](https://apps.developer.homey.app/the-basics/widgets) — what they are and the file layout
5. [Widgets → Settings](https://apps.developer.homey.app/the-basics/widgets/settings) — how users configure a widget
6. [Widgets → Styling](https://apps.developer.homey.app/the-basics/widgets/styling) — **required**. Learn the CSS variables; no hardcoded hex colors.
7. [Widgets → Debugging](https://apps.developer.homey.app/the-basics/widgets/debugging) — Chrome DevTools for widgets

**Also useful:**

- [Web API reference](https://api.developer.homey.app) — for talking to Homey from outside the app
- [SDK v3 TypeScript definitions](https://github.com/athombv/node-homey-apps-sdk-v3-types) — install as a devDep for VS Code autocomplete:
  ```bash
  npm install --save-dev @types/homey@npm:homey-apps-sdk-v3-types
  ```
- [Homey Developer Tools](https://tools.developer.homey.app) — system info, API explorer, logs

**Exercise W3:**

Extend your `com.<yourname>.hello` app with:

1. A **Flow trigger card** `temperature_out_of_range` that fires when a `mock_sensor`'s temperature goes above or below a user-configured threshold (two arguments: a `device` and a `number`).
2. A **widget** `sensor_summary` that:
   - Has a `devices` setting filtered to `driver_id=mock_sensor`
   - Displays the latest temperature and humidity from that device
   - Fetches values from your app's `api.js`
   - Uses Homey's CSS variables — correct in both light and dark mode

**Demo:** Add the widget to your Homey dashboard. Create a Flow using the trigger card. Watch the Flow fire and the widget update live. Record a screenshot recording and share as demo.

---

### Week 4 — Assignment + PR

Use this week for the [assignment](./02-assignment.md). Reserve the last day for code review, fixes, and demo.

---

## 3. Curated reference list

Pin these in your browser.

**Official docs (primary):**

- https://apps.developer.homey.app — Apps SDK guide (narrative, start here)
- https://apps-sdk-v3.developer.homey.app — SDK v3 API reference (grep this)
- https://api.developer.homey.app — Web API (Homey from outside)
- https://tools.developer.homey.app — Developer Tools (live system info, API explorer)

**Support:**

- https://homey.app/en-us/developer/ — high-level developer landing
- https://community.homey.app — developer forum. **Search before you post.** Athom staff read it.
- Stack Overflow tag [`homey`](https://stackoverflow.com/questions/tagged/homey)

**Code:**

- https://github.com/athombv/node-homey-apps-sdk-v3-types — TypeScript types
- https://github.com/athombv — Athom's GitHub org with several example apps to read

---

## 4. Glossary (Homey-specific terms)

| Term                 | Means                                                                                                         |
| -------------------- | ------------------------------------------------------------------------------------------------------------- |
| **Homey**            | The platform. Also the hub hardware (Homey Pro) and the cloud service (Homey Cloud).                          |
| **App**              | A Node.js or Python bundle that runs on Homey and adds devices, Flow cards, widgets, etc.                     |
| **Driver**           | A class representing a *type* of device. Handles pairing, defines capabilities and Flow cards.                |
| **Device**           | An instance of a driver — a specific physical thing the user paired. One driver → many devices.               |
| **Capability**       | A single piece of device state (`onoff`, `measure_power`, ...). System or custom.                             |
| **Flow**             | Homey's user-facing automation, in the form `When ... And ... Then ...`.                                      |
| **Flow card**        | A reusable block your app contributes to the Flow editor. Trigger, condition, or action.                      |
| **Widget**           | A custom webview your app adds to a user dashboard. HTML/CSS/JS + an `api.js` backend.                        |
| **Homey Insights**   | Built-in historical charts. Capability values are auto-logged and plottable.                                  |
| **Homey Compose**    | The build step that merges `.homeycompose/`, `drivers/*/driver.compose.json`, `flow/*.compose.json` → `app.json`. |
| **Pairing**          | The flow for adding a device to Homey. Auto-discovery, manual, or custom HTML views.                          |
| **SDK v3**           | The current Apps SDK version. Don't read v2 docs by accident.                                                 |
| **Zone**             | A room / area in the user's home. Devices belong to zones.                                                    |

---

## 5. The assignment

Full spec in [`assignment.md`](./02-assignment.md). Short version: you'll build a standalone Homey app called `weatherbuddy` with a virtual driver, Flow cards, a widget, and an app settings page. You'll submit it as a PR against this repo on a branch named after your GitHub username.

---

## 6. Gotchas that will cost you half a day if you don't know them

1. **Never hand-edit `app.json`.** It's generated by Homey Compose from `.homeycompose/` and `*.compose.json` files. Your next `homey app run` will overwrite your edits silently.
2. **`homey app run` vs `homey app install`:** use `run` in development — hot reload + live logs. `install` is persistent and doesn't reload.
3. **The CLI caches your logged-in Homey.** When you switch Homeys, run `homey login` again.
4. **Capabilities are case-sensitive and namespaced.** `measure_temperature.inside` vs `measure_temperature.outside` are two different sub-capabilities. Typos don't error — they silently create a new custom capability.
5. **Custom capabilities auto-generate Flow triggers** with IDs like `<cap>_changed` (number/string/enum) or `<cap>_true` / `<cap>_false` (boolean). If you also declare your own Flow card with the same ID, you'll see duplicates.
6. **Widgets have no `localStorage`.** Persistent state lives in widget settings, or in your app via `api.js`.
7. **SDK v2 docs are a trap.** `apps-sdk-v2.developer.athom.com` still resolves — don't land there by accident. Always use `apps.developer.homey.app` and `apps-sdk-v3.developer.homey.app`.
8. **Python apps need Docker.** If you create a Python app, Docker Desktop must be running before `homey app run`.
9. **Validation has levels.** `debug` is the default for `run`. Always run `homey app validate --level publish` before a PR.
10. **The Homey mobile app caches widget HTML aggressively.** If your widget changes aren't showing, fully quit the mobile app — don't just pull to refresh.

---

## 7. Development workflow conventions

- **Branches:** `feature/<short-name>` off `main`. Rebase before PR, no merge commits.
- **Commits:** [Conventional Commits](https://www.conventionalcommits.org/). Imperative mood, ≤ 72 chars.
- **Running locally:** `homey app run`, never `install` during dev.
- **Before PR:** `homey app validate --level publish` must pass.
- **PR description:** What / Why / How to test / Screenshots (for widget changes).
- **Do not:** hand-edit `app.json`, commit `env.json`, log user data, add a dependency without discussing, push to `main` directly.

---

## 9. First-week checklist

Print it. Tick it off.

- [ ] Day 1 AM: laptop set up, all prerequisites installed
- [ ] Day 1 PM: Hello-World Homey app running on your own Homey, log line visible
- [ ] Day 2: read Getting Started, App, Manifest, Homey Compose
- [ ] Day 3: Exercise W1 demo
- [ ] Day 4: read Drivers & Devices, Pairing, Capabilities
- [ ] Day 5: virtual driver paired, Exercise W2 demo

If you're behind on Friday, **say so**. Better to hear on day 5 than day 25.

---

*Welcome. Ask stupid questions early — it gets awkward later.*
