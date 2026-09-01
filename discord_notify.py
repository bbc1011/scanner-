import requests

from models import Deal


def send_deal_webhook(webhook_url: str, deal: Deal, timeout: int = 20) -> None:
    listing = deal.listing

    fields = [
        {
            "name": "Listing price",
            "value": f"${listing.total_price:.2f}",
            "inline": True,
        },
        {
            "name": "Reference market",
            "value": f"${deal.market_price:.2f}",
            "inline": True,
        },
        {
            "name": "Below reference",
            "value": f"{deal.discount_percent:.1f}%",
            "inline": True,
        },
        {
            "name": "Condition",
            "value": listing.condition or "Not supplied",
            "inline": True,
        },
        {
            "name": "Deal score",
            "value": f"{deal.score:.1f}/10",
            "inline": True,
        },
    ]

    if deal.ai:
        items = "\n".join(f"• {x}" for x in deal.ai.items[:8]) or "No specific items identified."
        fields.append(
            {
                "name": f"AI identification (confidence {deal.ai.confidence:.0%})",
                "value": items[:1024],
                "inline": False,
            }
        )

    embed = {
        "title": "🚨 Potential LEGO Deal",
        "description": f"[{listing.title}]({listing.url})",
        "fields": fields,
    }

    payload = {
        "username": "LEGO Deal Finder",
        "embeds": [embed],
    }

    response = requests.post(
        webhook_url,
        json=payload,
        timeout=timeout,
    )
    response.raise_for_status()


def send_plain_webhook(webhook_url: str, content: str, timeout: int = 20) -> None:
    response = requests.post(
        webhook_url,
        json={"content": content},
        timeout=timeout,
    )
    response.raise_for_status()
