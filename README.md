# BlackVine

A lightweight HTTP server for Raspberry Pi that controls WiZ smart bulbs in response to events pushed from any backend.

Send an event → a bulb lights up → turns off after a configurable duration.

---

## How it works

```
Your backend  ──POST /event──►  BlackVine (RPi)  ──UDP setPilot──►  WiZ bulb
```

BlackVine receives an HTTP event, resolves the bulb name to an IP (from env vars), and sends a raw UDP command to the bulb. A `threading.Timer` turns the bulb off after `duration` seconds.

---

## Setup

### 1. Clone and install

```bash
git clone https://github.com/youruser/blackvine ~/blackvine
cd ~/blackvine
python3 -m venv venv
venv/bin/pip install -r requirements.txt
```

### 2. Configure

```bash
cp .env.example .env
```

Edit `.env`:

```env
# One line per bulb — name it whatever you like
BULB_OFFICE=192.168.1.100
BULB_LIVING_ROOM=192.168.1.101

BLACKVINE_API_KEY=your-secret-key
```

To find a bulb's IP, check your router's DHCP table or run a LAN scanner (`nmap -sn 192.168.1.0/24`).

### 3. Run

**Development:**

```bash
venv/bin/python main.py
```

**Production (systemd):**

```bash
sudo cp setup/blackvine.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now blackvine
```

See [`setup/cloudflare-tunnel.md`](setup/cloudflare-tunnel.md) to expose the server to the internet.

---

## Sending events

**POST** `/event`

Headers:
- `X-Api-Key: <your key>` — required if `BLACKVINE_API_KEY` is set

### Named colour

```json
{"bulb": "office", "color": "red", "duration": 300}
```

### Raw RGB

```json
{"bulb": "office", "r": 255, "g": 0, "b": 0, "dimming": 80, "duration": 300}
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `bulb` | string | required | Matches `BULB_<NAME>` env var |
| `color` | string | — | Named colour (see below); overrides r/g/b |
| `r` / `g` / `b` | int 0–255 | 255 | Raw RGB (used when `color` is absent) |
| `dimming` | int 0–100 | 100 | Brightness |
| `duration` | int (seconds) | 0 | Auto-off after N seconds; 0 = stay on |

### Available colours

`white` `red` `green` `blue` `cyan` `amber` `yellow` `purple`

### Health check

```
GET /health  →  {"status": "ok"}
```

---

## Auto-deploy (GitHub Actions)

BlackVine ships with a self-hosted runner workflow that redeploys on every push to `main`. The runner runs directly on the RPi — no ports need to be open.

### One-time RPi setup

1. Register a self-hosted runner on the repo: **Settings → Actions → Runners → New self-hosted runner** — follow the Linux/ARM instructions.

2. Allow the runner to restart the service without a password:

```bash
echo "pi ALL=(ALL) NOPASSWD: /bin/systemctl restart blackvine" | sudo tee /etc/sudoers.d/blackvine
```

After that, every push to `main` automatically pulls the latest code and restarts the server.
