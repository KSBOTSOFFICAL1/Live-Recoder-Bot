"""Validate deployment configuration, then start the Pyrogram bot."""

import os
import sys


def main() -> None:
    missing = [
        key
        for key in ("TELEGRAM_BOT_TOKEN", "TELEGRAM_API_HASH")
        if not os.getenv(key, "").strip()
    ]
    if missing:
        print(
            "Missing required Replit Secrets: "
            + ", ".join(missing)
            + ". Add them before starting the bot.",
            file=sys.stderr,
        )
        raise SystemExit(2)

    import bot

    bot.app.run(bot._bot_main())


if __name__ == "__main__":
    main()