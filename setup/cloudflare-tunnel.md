# Cloudflare Tunnel setup

Run these commands on the RPi. The config file lives at `/etc/cloudflared/config.yml`
and is never committed to the repo because it contains your tunnel ID.

```bash
# 1. Install cloudflared
curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64.deb -o cloudflared.deb
sudo dpkg -i cloudflared.deb

# 2. Authenticate + create a tunnel
cloudflared tunnel login
cloudflared tunnel create blackvine          # prints your tunnel ID

# 3. Route a subdomain to the tunnel
cloudflared tunnel route dns blackvine obs.yourdomain.com

# 4. Write the config (replace <TUNNEL_ID> with the ID from step 2)
sudo tee /etc/cloudflared/config.yml <<EOF
tunnel: <TUNNEL_ID>
credentials-file: /home/pi/.cloudflared/<TUNNEL_ID>.json

ingress:
  - hostname: obs.yourdomain.com
    service: http://localhost:5000
  - service: http_status:404
EOF

# 5. Install and start as a system service
sudo cloudflared service install
sudo systemctl enable --now cloudflared
```
