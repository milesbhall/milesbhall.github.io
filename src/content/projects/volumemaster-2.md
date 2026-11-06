---
name: VolumeMaster 2
description: A Firefox extension that helps people avoid prediction markets vulnerable to manipulation by overlaying real TCGplayer sales volume on Kalshi's Pokémon price markets.
event: "&Hacks XII"
award: 2nd in the financial track
date: 2026-09-01
team: Solo
thumbnail: /images/projects/volumemaster-2.svg
links:
  - label: GitHub
    url: https://github.com/milesbhall/volumemaster2
  - label: Devpost
    url: https://devpost.com/software/volumemaster2
---

## Inspiration

The project was inspired by Jane Street's manipulation of Indian options markets.
The same kind of manipulation could happen on online prediction markets where the
underlying market is much smaller than the trading volume placed on it. One market
fits that description well: Kalshi's prediction markets on the prices of Pokémon
products.

## What it does

VolumeMaster 2 is a Firefox extension that shows its findings right on the Kalshi
dashboard. It places TCGplayer sales volume next to each Pokémon price market and
warns about markets with dangerous levels of trading volume compared with low
activity in the underlying product market. A panel, which starts minimized, gives an
overview of the active markets, and clicking a row opens that market.

## The pipeline

A Python data pipeline feeds the extension. It runs once a day, which keeps Apify
usage low enough for the free plan.

1. **Kalshi.** Collect the active Pokémon price markets and their market data. New
   series are found by tag or title, and only price markets are kept.
2. **TCGCSV.** Match each product to a TCGplayer listing by exact name or closest
   price, then confirm the match by price. Saved matches are reused in later months
   and can be overridden by hand.
3. **Apify.** Fetch weekly sales volume for each product.
4. **Overlay.** Combine everything into one file for the extension. Closed markets are
   dropped.

The pipeline also reports the gap between each TCGplayer price and the Kalshi price,
and it flags gaps over 30%. A GitHub Actions workflow runs it every day at 21:00 UTC
and commits the refreshed data.

## Challenges

TCGplayer hasn't offered API access in years and doesn't allow scraping, so getting
sales data meant combining several third-party APIs. To keep API calls down, the
pipeline only collects data on products listed as currently active on Kalshi.

## Built with

Python · Kalshi API · TCGCSV · Apify · GitHub Actions · Firefox WebExtension · Claude Code

## What's next

Getting approved for the TCGplayer and Collectr APIs would remove the dependence on
Apify. The extension could also be extended to other prediction markets and other
types of prediction.
