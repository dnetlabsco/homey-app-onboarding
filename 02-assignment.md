# Assignment — `com.<yourname>.weatherbuddy`

> **When:** Week 4 of your onboarding.
> **Time budget:** ~5 working days, ~6h/day.
> **Review:** Pull request against this repo + live demo on the last day.

---

## TL;DR

Build a small, standalone Homey app with a virtual weather-station device, three Flow cards, and a dashboard widget. This assignment exercises every fundamental primitive of Homey app development. You're not shipping a real product — you're proving you can use the SDK end-to-end.

---

## What you're building

An app `com.<yourname>.weatherbuddy` that:

1. Adds a **virtual driver** you can pair any number of times (no real hardware)
2. Exposes **three Flow cards**: a trigger, a condition, and an action
3. Renders one **dashboard widget** that displays the device's current state
4. Provides an **app settings page** with one toggle

---

## Functional requirements

### 1. Driver: `weather_station`

- Virtual pairing (use the `list_devices` pair template — no wireless discovery)
- Capabilities:

  | Capability            | Type                          | Behavior                                      |
  | --------------------- | ----------------------------- | --------------------------------------------- |
  | `measure_temperature` | system (°C)                   | Random 15–25, ticks every 10 s                |
  | `measure_humidity`    | system (%)                    | Random 30–70, ticks every 10 s                |
  | `measure_pressure`    | system (mbar)                 | Random 1000–1025, ticks every 10 s            |
  | `mode`                | custom, enum: `sunny`/`cloudy`/`rainy` | Random choice every 60 s             |

### 2. Flow trigger card: `weather_changed`

- Arguments:
  - `device` (type `device`, filter `driver_id=weather_station`)
  - `mode` (type `dropdown`: `sunny`, `cloudy`, `rainy`)
- Fires when the device's `mode` capability changes **to** the selected value
- Provides a `temperature` token (number) so users can pipe it into downstream Flow cards

### 3. Flow condition card: `is_it_raining`

- Argument: `device` (filter `driver_id=weather_station`)
- Returns `true` when `mode === 'rainy'`, `false` otherwise
- Must support the inverted form ("it is not raining") via Homey's built-in inversion

### 4. Flow action card: `set_weather_mode`

- Arguments:
  - `device` (filter `driver_id=weather_station`)
  - `mode` (dropdown)
- Writes the `mode` capability on the selected device — useful for manual testing from the Flow editor

### 5. Widget: `weather_widget`

- Settings:
  - `device` (type `devices`, filter `driver_id=weather_station`, single-select)
  - `unit` (type `dropdown`: `celsius` or `fahrenheit`) — affects only the displayed temperature
- UI:
  - Temperature (large)
  - Humidity and pressure on a second row
  - An emoji matching the mode: `☀️` / `☁️` / `🌧️`
- Data flow:
  - Widget `index.html` calls your app-side `api.js` endpoint on load
  - Refreshes on a 10-second interval
- Styling:
  - **Only** Homey CSS variables (see [Widgets → Styling docs](https://apps.developer.homey.app/the-basics/widgets/styling))
  - Must look correct in both light and dark mode
  - **Zero hex color codes** in your stylesheet

### 6. App-side API (`api.js`)

One endpoint:

```
GET /state?deviceId=<id>
→ 200 { "temperature": 21.3, "humidity": 55, "pressure": 1013, "mode": "sunny" }
```

Reads values straight from the device's capabilities.

### 7. App settings page

One toggle in `settings/index.html`: **"Freeze values"**. When ON, the periodic capability updates pause on every paired device. Useful for demos and screenshots. Uses `ManagerSettings` under the hood.

---

## Non-functional requirements

- [ ] `homey app validate --level publish` passes with **zero** warnings
- [ ] SDK v3 TypeScript types installed as a devDep:
      `npm install --save-dev @types/homey@npm:homey-apps-sdk-v3-types`
- [ ] All user-facing strings in `locales/en.json` **and** `locales/nl.json` (actually translated)
- [ ] `README.md` inside your submission folder with: what the app does, how to dev-install, screenshots
- [ ] Use `this.log` / `this.error` — no `console.log`
- [ ] No external HTTP calls, no secrets, no hardcoded IDs
- [ ] Light and dark mode screenshots committed to `docs/screenshots/` inside your submission folder

---

## Acceptance criteria (reviewer's checklist)

### Code review

- [ ] [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `docs:`, ...)
- [ ] `app.json` is generated, never hand-edited
- [ ] No dead code, no commented-out blocks
- [ ] Standard Homey file layout (drivers, flow, widgets, locales)

### Functional demo

- [ ] Two `weather_station` devices can be paired
- [ ] Flow trigger fires on the correct device, not on siblings (test with two devices paired)
- [ ] Condition card evaluates correctly in both direct and inverted form
- [ ] Action card updates only the selected device
- [ ] Widget shows live values that change over time
- [ ] Unit toggle (°C ↔ °F) works
- [ ] "Freeze values" toggle actually pauses ticks on every device
- [ ] Widget renders correctly in light and dark mode — demo both

### Quality gates

- [ ] `homey app validate --level publish` is green
- [ ] No console errors in widget DevTools
- [ ] App starts cold in under 3 seconds
- [ ] `nl.json` is actually translated (use DeepL + spot check by a Dutch speaker on the team)
- [ ] App is published to Homey App Store as **Test** (not Draft, not submitted for Certification)
- [ ] Test URL works — reviewer can open it

---

## How to submit

Your submission lives on a branch of this repo, named after your GitHub username. You open a PR against `main`. The PR is where code review happens.

### Step-by-step

1. **Clone this repo** and create a branch named after your GitHub username:

   ```bash
   git clone git@github.com:dnetlabsco/homey-app-onboarding.git
   cd homey-app-onboarding
   git checkout -b <your-github-username>
   ```

2. **Put your Homey app** inside a folder matching your username:

   ```
   submissions/<your-github-username>/
   ├── .homeycompose/
   ├── drivers/
   │   └── weather_station/
   ├── flow/
   ├── widgets/
   │   └── weather_widget/
   ├── locales/
   │   ├── en.json
   │   └── nl.json
   ├── settings/
   │   └── index.html
   ├── docs/
   │   └── screenshots/
   │       ├── light-mode.png
   │       └── dark-mode.png
   ├── api.js
   ├── app.js
   ├── app.json            ← generated, don't hand-edit
   ├── package.json
   ├── README.md           ← what the app does + how to run
   └── RETRO.md            ← see below
   ```

   Do **not** commit `node_modules/`, `env.json`, or the `.homeybuild/` folder. Add them to `.gitignore`.

3. **Commit and push** your branch. Use conventional commits:

   ```bash
   git add submissions/<your-github-username>
   git commit -m "feat: weatherbuddy submission"
   git push -u origin <your-github-username>
   ```

4. **Publish your app to the Homey App Store as a Test release.** This teaches you the publishing pipeline without polluting the public App Store.

   The Homey release pipeline is **Draft → Test → Certification → Live**. You will go only as far as **Test**.

   a. From your submission folder, publish:

      ```bash
      cd submissions/<your-github-username>
      homey app publish
      ```

      This uploads your app to the Homey App Store as a **Draft** (not visible to the public).

   b. Go to https://tools.developer.homey.app → **Apps SDK** → **My Apps**, find your app, and **promote the Draft to Test**.

   c. A test URL is generated, of the form:

      ```
      https://homey.app/en-us/app/com.<yourname>.weatherbuddy/test/
      ```

      Copy this URL — you'll paste it in your PR description.

   > **⚠️ DO NOT submit for certification.**
   > The certification button sends your app to Athom's review team for inclusion in the public Homey App Store. This is a training assignment — submitting it wastes a reviewer's time at Athom and looks unprofessional on our team's behalf. **Stop at Test. Never click "Submit for Certification".**

5. **Open a pull request** against `main`:
   - **Title:** `[<your-github-username>] weatherbuddy submission`
   - **Description template:**
     ```
     ## What
     Weatherbuddy assignment submission.

     ## Test URL (hidden / Test release, NOT certified)
     https://homey.app/en-us/app/com.<yourname>.weatherbuddy/test/

     ## How to test locally
     1. cd submissions/<your-github-username>
     2. npm install
     3. homey app run
     4. Pair two weather_station devices, add the widget to a dashboard

     ## Screenshots
     See docs/screenshots/ — light and dark mode.

     ## Validation
     homey app validate --level publish → passes

     ## RETRO
     See RETRO.md.
     ```
   - Request review from your buddy.

6. **Iterate** — push more commits to the same branch in response to review comments. The PR will update automatically. Don't force-push after review has started; your reviewer wants commit-by-commit history.

7. **Do not merge to `main`.** Your branch is your submission. Main stays clean with only the onboarding docs. Once your PR is approved, it gets marked approved and stays as a record.

### `RETRO.md` — what to write

A short markdown file at the root of your submission folder:

- **Three things that took longer than expected.** Be specific — "widget styling" is vague; "figuring out how to differentiate light vs dark mode backgrounds without hex codes" is useful.
- **Three things that were clearer than expected.** Helps us know what the docs + this kit got right.
- **Three questions you still have.** No filler. These drive the next version of this kit.

---

## Deliverables (summary)

1. **Branch** `<your-github-username>` pushed to this repo with your submission under `submissions/<your-github-username>/`
2. **App published to Homey App Store as Test** (Draft → Test, **not** Certification)
3. **Test URL** (e.g. `https://homey.app/en-us/app/com.<yourname>.weatherbuddy/test/`) included in the PR description
4. **PR** titled `[<your-github-username>] weatherbuddy submission`, approved by your buddy
5. **5-minute demo recording** (Loom or screen capture) linked in the PR description:
   - Pair two devices
   - Build a Flow using the trigger, condition, and action cards
   - Add the widget to a dashboard
   - Toggle "Freeze values"
   - Switch light ⇄ dark mode
6. **`RETRO.md`** inside your submission folder

---

## Hints (use only if stuck > 1 hour)

- For the Flow trigger on a capability change, look at `registerRunListener` and Homey's "Device" Flow cards documentation.
- For the widget device setting, `type: "devices"` with a `filter` scopes the picker. See Widgets → Settings.
- `Homey.ready({ height: 200 })` in your widget JS removes the loading state.
- Inside a widget's `index.html`, the `Homey` global is a thin shim that talks to your `api.js` — it's **not** the same as `Homey` in `app.js`.
- Custom capabilities with type `enum` auto-generate a `<cap>_changed` Flow trigger. If you also define your own `weather_changed` trigger card with that same ID, you'll see duplicates in the Flow editor. Use a distinct ID.

---

## Explicitly out of scope

- Talking to any real weather service / API
- OAuth or cloud integrations
- Persistent history or charts
- Any language beyond `en` + `nl`
- Real push notifications

If you find yourself building any of the above, **stop and ask** — you're overbuilding.
