import argparse
import sys
from typing import Optional

from config import load_config
from database import Database
from deal_engine import evaluate
from discord_notify import send_deal_webhook
from ebay_client import EbayClient
from ai_vision import analyze_listing_images


def run(no_ai: bool = False, no_discord: bool = False) -> int:
    cfg = load_config()

    print("=" * 60)
    print("LEGO DEAL FINDER — PROTOTYPE")
    print("=" * 60)
    print(f"Search:             {cfg.search_query}")
    print(f"Max price:          ${cfg.max_price_usd:.2f}")
    print(f"Min discount:       {cfg.min_discount_percent:.1f}%")
    print(f"Reference market:   ${cfg.reference_market_price_usd:.2f}")
    print(f"AI enabled:         {bool(cfg.openai_api_key) and not no_ai}")
    print(f"Discord enabled:    {bool(cfg.discord_webhook_url) and not no_discord}")
    print()

    ebay = EbayClient(
        cfg.ebay_client_id,
        cfg.ebay_client_secret,
        cfg.ebay_marketplace_id,
        cfg.request_timeout_seconds,
    )
    db = Database(cfg.database_path)

    try:
        print("Searching eBay...")
        listings = ebay.search(
            cfg.search_query,
            max_results=cfg.max_results,
            max_price=cfg.max_price_usd,
            fixed_price_only=cfg.fixed_price_only,
        )
        print(f"Found {len(listings)} listings.\n")

        deals_found = 0

        for index, listing in enumerate(listings, start=1):
            print(f"[{index}/{len(listings)}] {listing.title}")
            print(f"    Price: ${listing.total_price:.2f} | {listing.condition or 'Unknown'}")

            if db.already_alerted(listing.item_id):
                print("    Skipping: already alerted.\n")
                continue

            ai_result = None
            if cfg.openai_api_key and not no_ai and listing.image_urls:
                try:
                    print("    Running AI image analysis...")
                    ai_result = analyze_listing_images(
                        cfg.openai_api_key,
                        cfg.openai_model,
                        listing,
                        cfg.ai_max_images,
                    )
                    if ai_result:
                        print(
                            f"    AI: {ai_result.summary} "
                            f"(confidence {ai_result.confidence:.0%})"
                        )
                except Exception as exc:
                    print(f"    AI warning: {exc}")

            deal = evaluate(
                listing,
                cfg.reference_market_price_usd,
                cfg.min_discount_percent,
                ai_result,
            )

            if not deal:
                print("    Not a qualifying deal.\n")
                continue

            deals_found += 1
            print(
                f"    🚨 DEAL: {deal.discount_percent:.1f}% below reference, "
                f"score {deal.score:.1f}/10"
            )

            if cfg.discord_webhook_url and not no_discord:
                try:
                    send_deal_webhook(
                        cfg.discord_webhook_url,
                        deal,
                        cfg.request_timeout_seconds,
                    )
                    print("    Discord alert sent.")
                except Exception as exc:
                    print(f"    Discord warning: {exc}")
                    # Do not mark it alerted if Discord failed.
                    continue

            db.mark_alerted(listing.item_id, listing.title)
            print()

        print("-" * 60)
        print(f"Potential deals found: {deals_found}")
        print("-" * 60)
        return 0

    finally:
        db.close()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--no-ai",
        action="store_true",
        help="Skip OpenAI image analysis.",
    )
    parser.add_argument(
        "--no-discord",
        action="store_true",
        help="Do not send Discord notifications.",
    )
    args = parser.parse_args()

    try:
        return run(no_ai=args.no_ai, no_discord=args.no_discord)
    except KeyboardInterrupt:
        print("\nStopped.")
        return 130
    except Exception as exc:
        print(f"\nERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
