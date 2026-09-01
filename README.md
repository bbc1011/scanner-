# LEGO Deal Finder — eBay + AI Prototype

This is a local prototype for scanning eBay listings through the official eBay Browse API,
optionally analyzing listing images with OpenAI vision, scoring potential deals, and sending
alerts to a Discord channel through a webhook.

## What this prototype does

1. Reads search settings from `.env`.
2. Gets an eBay Application Access Token using the client-credentials flow.
3. Searches eBay's Browse API for matching listings.
4. Calculates the listing's total price (item + shipping when supplied).
5. Optionally sends listing images to a vision-capable OpenAI model for LEGO identification.
6. Estimates a market price from a configurable baseline (prototype only).
7. Sends qualifying deals to Discord.
8. Stores alerted eBay item IDs in SQLite so the same listing is not repeatedly alerted.

## Important prototype limitation

This first version does **not** claim that its market-price estimate is a real sold-comps
valuation. The `REFERENCE_MARKET_PRICE_USD` setting is a simple baseline so we can verify the
pipeline end-to-end. A later version should add a real comparable-sales source and a more
sophisticated LEGO-specific valuation model.

## Requirements

- Python 3.10+
- eBay Developer account and app credentials for the Buy/Browse API
- Optional OpenAI API key for image analysis
- Optional Discord channel webhook URL

## Setup

Windows PowerShell:

```powershell
py -3 -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` and add your credentials/settings.

Run:

```powershell
python main.py
```

Run once without OpenAI image analysis:

```powershell
python main.py --no-ai
```

Send a test notification to Discord:

```powershell
python discord_test.py
```

## eBay credentials

Use the eBay Developer Program to create an application keyset. Put the Client ID and Client
Secret in `.env`. Do not commit `.env` or share it.

The Browse API uses an Application access token obtained through OAuth client credentials.

## Discord

For the prototype, a Discord **webhook** is simpler than a full interactive bot. It can post
rich embeds into one channel. A later version can replace this with a full Discord bot that
supports commands such as `/addsearch`, `/scan`, and `/status`.

## Suggested first test

Use something narrow, for example:

```text
SEARCH_QUERY=LEGO 501st Clone Trooper
MAX_PRICE_USD=60
MIN_DISCOUNT_PERCENT=30
REFERENCE_MARKET_PRICE_USD=80
MAX_RESULTS=20
```

Then run the scanner and inspect the terminal output before enabling AI.

## Project layout

- `main.py` — application entry point
- `ebay_client.py` — eBay OAuth + Browse API search
- `ai_vision.py` — OpenAI image analysis
- `deal_engine.py` — price and deal calculations
- `discord_notify.py` — Discord webhook notifications
- `database.py` — SQLite deduplication
- `config.py` — environment configuration
- `models.py` — dataclasses
- `discord_test.py` — simple Discord webhook test
- `.env.example` — configuration template
