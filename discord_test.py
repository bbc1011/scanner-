from config import load_config
from discord_notify import send_plain_webhook

if __name__ == "__main__":
    cfg = load_config()
    if not cfg.discord_webhook_url:
        raise RuntimeError("Set DISCORD_WEBHOOK_URL in .env first.")
    send_plain_webhook(
        cfg.discord_webhook_url,
        "✅ LEGO Deal Finder Discord webhook is connected.",
        cfg.request_timeout_seconds,
    )
    print("Discord test message sent.")
