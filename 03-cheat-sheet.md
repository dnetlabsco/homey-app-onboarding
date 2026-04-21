# Homey Developer Cheat Sheet

## CLI commands you'll run every day

| Command                                      | What it does                                                      |
| -------------------------------------------- | ----------------------------------------------------------------- |
| `homey app create`                           | Scaffold a new app                                                |
| `homey app run`                              | Run on a dev Homey with live logs + hot reload                    |
| `homey app install`                          | Install persistently (no hot reload) — use for final testing only |
| `homey app validate --level publish`         | Run this before every PR                                          |
| `homey app driver create`                    | Interactively add a driver                                        |
| `homey app flow create`                      | Interactively add a Flow card                                     |
| `homey app widget create`                    | Interactively add a widget                                        |
| `homey login`                                | Re-auth with your Athom account                                   |

## File structure reminders

```
com.example.app/
├─ .homeycompose/          ← edit these JSONs, not app.json
│  └─ app.json             ← app-level manifest bits
├─ assets/                 ← app-wide icons & images
├─ drivers/
│  └─ my_driver/
│     ├─ driver.compose.json   ← driver manifest
│     ├─ driver.js             ← Driver class
│     ├─ device.js             ← Device class
│     ├─ pair/                 ← custom pairing HTML
│     └─ assets/               ← driver-specific icons
├─ flow/                   ← Flow card JSON (compose)
├─ widgets/
│  └─ my_widget/
│     ├─ widget.compose.json
│     ├─ public/           ← index.html, CSS, JS
│     └─ api.js            ← widget backend
├─ locales/                ← en.json, nl.json, ...
├─ settings/index.html     ← app settings UI (optional)
├─ api.js                  ← app-level REST API (optional)
├─ app.js                  ← your App class
├─ app.json                ← GENERATED — don't edit
└─ env.json                ← gitignored secrets
```

## Capability patterns (memorize)

```js
// Homey → physical device (user toggles something)
this.registerCapabilityListener('onoff', async (value) => {
  await this.api.setState({ on: value });
});

// Physical device → Homey (state changed externally)
this.api.on('state-changed', (isOn) => {
  this.setCapabilityValue('onoff', isOn).catch(this.error);
});
```

## Flow card patterns

```js
// In app.js → onInit()
const card = this.homey.flow.getActionCard('my_action');
card.registerRunListener(async (args, state) => {
  // args.device → the device the user picked
  // args.<n> → each other arg you declared
  await args.device.setCapabilityValue('my_capability', args.value);
});
```

## Widget quick reference

```html
<!-- widgets/my_widget/public/index.html -->
<body class="homey-widget">
  <h2 class="homey-text-title-large">Loading…</h2>

  <script>
    // `Homey` here is the widget-side shim, NOT the app-side Homey
    Homey.ready({ height: 180 });

    const deviceIds = Homey.getDeviceIds();   // from settings type "devices"
    const settings  = Homey.getSettings();    // your other widget settings

    Homey.api('GET', `/state?deviceId=${deviceIds[0]}`, (err, res) => {
      if (err) return Homey.showError(err);
      document.querySelector('h2').textContent = `${res.temperature} °C`;
    });
  </script>
</body>
```

## When in doubt

1. `apps.developer.homey.app` — the narrative docs
2. `apps-sdk-v3.developer.homey.app` — the class reference
3. `community.homey.app` — search before you post
4. Your buddy
5. The team chat

Never:

- Edit `app.json` by hand
- Commit `env.json`
- Use `console.log` in production code
- Read `apps-sdk-v2.*` docs (deprecated)
- `@channel` in chat




# `.homeycompose/` vs everything else

Homey apps (SDK v3) split into two worlds:

- **`.homeycompose/`** — declarative config. The CLI merges these JSON files into a single `app.json` at the project root when you run `homey app build` / `homey app run`.
- **Everything else** — runtime TypeScript, assets, pair views, and tooling.

The root `app.json` is **generated output**. Don't hand-edit it — your changes get overwritten on the next build.

---

## Edit inside `.homeycompose/`

| Path | What it defines |
|---|---|
| `.homeycompose/app.json` | Base manifest: `id`, `version`, `name`, `permissions`, `platforms`, `brandColor`, etc. |
| `.homeycompose/capabilities/<cap>.json` | Custom capabilities (e.g. `sb_mode`, `sb_target_power`). One file per capability. |
| `.homeycompose/flow/actions/<card>.json` | Flow **Then** cards. |
| `.homeycompose/flow/triggers/<card>.json` | Flow **When** cards. |
| `.homeycompose/flow/conditions/<card>.json` | Flow **And** cards. |
| `.homeycompose/signals/` | 433/868 MHz / IR signal definitions (if any). |
| `.homeycompose/discovery/` | mDNS / SSDP discovery strategies (if any). |

> Rule: if the value ends up in the final merged `app.json`, it belongs under `.homeycompose/`.

## Edit outside `.homeycompose/`

| Path | What it is |
|---|---|
| `app.ts` | Runtime entry point (app-level init, webhook registration). |
| `drivers/<id>/driver.compose.json` | Driver manifest. By convention lives next to the driver, **not** under `.homeycompose/`, but is still merged into `app.json` at build. |
| `drivers/<id>/driver.ts` | Pairing flow, `onPair` session handlers. |
| `drivers/<id>/device.ts` | Per-device runtime: capability listeners, polling, flow action handlers. |
| `drivers/<id>/pair/*.html` | Pairing UI views (HTML + inline JS using the `Homey.*` client API). |
| `drivers/<id>/assets/images/` | Driver icons (small / large / xlarge PNGs). |
| `drivers/<id>/locales/*.json` | Per-driver translations referenced from `driver.compose.json`. |
| `locales/*.json` | App-level translations. |
| `assets/` | App icons (`icon.svg`, PNGs). |
| `env.json` | Local environment for `homey app run` (`BACKEND_URL`, `WIDGET_URL`, webhook secrets). Not bundled into the store build. |
| `package.json`, `tsconfig.json`, `.homeyignore` | Tooling. |

## Do not edit

- **Root `app.json`** — regenerated on every build from `.homeycompose/` + each `driver.compose.json`.
- **`.homeybuild/`** — transpiled TS output. Auto-generated.

## Adding a new capability (example)

1. Create `.homeycompose/capabilities/sb_foo.json` with type/title/uiComponent/etc.
2. Add `"sb_foo"` to the `capabilities` array in `drivers/<id>/driver.compose.json`.
3. Add `capabilitiesOptions.sb_foo` in the same `driver.compose.json` if you need a custom title or visibility.
4. In `drivers/<id>/device.ts`, register a listener with `this.registerCapabilityListener('sb_foo', ...)`.
5. Run `npm run build` — the TS compiles and the Homey CLI regenerates `app.json`.

## Quick sanity checks

- Edited a capability or flow card and nothing changed? You probably edited the root `app.json` instead of `.homeycompose/`.
- `homey app validate` errors about a missing capability? It exists in code but not in `.homeycompose/capabilities/` or not listed in `driver.compose.json`.
- Existing paired devices don't get a newly added capability automatically — add `await this.addCapability('sb_foo')` in `onInit` as a migration.

