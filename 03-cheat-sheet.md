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
