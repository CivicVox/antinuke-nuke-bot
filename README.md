# Anti-Nuke / Nuke Bot
# ONLY USE THIS IN YOUR OWN, PRIVATE SERVERS
## THIS VIOLATES DISCORD'S TOS IF USED TO NUKE OTHER'S SERVERS AND CAN GET YOUR ACCOUNT BANNED
This Discord bot protects your server from mass-destruction attacks (anti-nuke mode) and can perform a nuke (wipe) if enabled.

---

## Features

- **Anti-Nuke Mode:**
  - Monitors for dangerous actions (channel/role deletions, bans) by untrusted bots.
  - Kicks untrusted bots that perform suspicious actions.
- **Nuke Mode:**
  - Deletes all channels and roles (except @everyone and roles above the bot).
  - Bans all members without admin permissions.
  - Spams new channels with messages.
- **Mode Switching:**
  - `!set_mode <anti-nuke|nuke>`: Switch between protection and nuke mode (admin only).
- **Protection:**
  - Trusted bots and unnukable servers are configurable at the top of the script.

---

## Setup

1. **Copy the bot file to your server.**
2. **Install dependencies:**
   ```sh
   pip install discord.py
   ```
3. **Configure your bot token:**
   - Replace the `bot.run('YOUR_TOKEN')` line with your actual bot token.
4. **(Optional, but recommended) Edit trusted bot/user/server IDs at the top of the file.**
5. **Run the bot:**
   ```sh
   python index.py
   ```

---

## Commands

- `!set_mode <anti-nuke|nuke>` — Switch bot mode (admin only).
- `!nuke <server_id>` — Nuke a server (admin only, only in nuke mode).

---

## Warnings
- **Never share your bot token publicly!**
- The nuke command is extremely destructive. Only use it in test servers or with extreme caution.
- The anti-nuke system is basic and can be improved for your needs.

---

## License & Disclaimer
This project is provided **AS-IS** with no warranty, guarantee, or support. Use at your own risk. The authors are not responsible for any damage, loss, or misuse. For educational purposes only. Use responsibly.

