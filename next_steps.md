# Next upgrades

## 1. Real LEGO market valuation

The current prototype uses one configurable reference value. Replace it with:

- recent sold/comparable data where legally and technically available
- median rather than simple average
- condition-aware comps
- exact set/minifigure/component matching
- shipping and fees
- confidence intervals

## 2. Better LEGO image identification

Add a candidate catalog containing:

- LEGO set numbers
- minifigure IDs
- known visual descriptors
- historical price ranges

Then have the vision model return candidate IDs rather than only free-text guesses.

## 3. Multi-search configuration

Move from one `.env` search to a `searches.json` or database table:

```json
[
  {"name":"501st","query":"LEGO 501st Clone Trooper","max_price":60,"min_discount":30},
  {"name":"Clone Wars","query":"LEGO Clone Wars figures","max_price":100,"min_discount":35}
]
```

## 4. Full Discord bot

Replace/augment the webhook with a real bot and slash commands:

- `/addsearch`
- `/removesearch`
- `/searches`
- `/scan`
- `/pause`
- `/status`

## 5. Continuous server mode

Run the scanner on a VPS or container with a scheduler. The same project can run locally
during development and move to a server when ready.
