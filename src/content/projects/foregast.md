---
name: Foregast
description: A financial tool that forecasts fertilizer prices from natural gas market data, so farmers can see price swings coming before they buy.
event: HooHacks
award: 1st place in the financial track
date: 2026-03-01
team: Team of four
thumbnail: /images/projects/foregast.svg
links:
  - label: GitHub
    url: https://github.com/bob3457/HooHacks26
  - label: Devpost
    url: https://devpost.com/software/hoohacks-submission
---

## Inspiration

The idea came from price hedging in agriculture. While researching it, the team found
a strong correlation between natural gas prices and fertilizer prices. Large
processors and agricultural suppliers have access to this kind of data, but regular
farmers usually don't.

## What it does

Agricultural prices are largely inelastic because planting runs on a tight seasonal
schedule, so farmers have few protections against price swings. Foregast uses machine
learning to measure how fertilizer inputs like natural gas drive the price of
fertilizer. It forecasts the price of fertilizer 30, 60, and 90 days ahead.

A farmer enters their crop (for example, corn) and acreage. The app then calculates
their nitrogen exposure and turns global energy-market movements into a personalized
recommendation.

## The model

- **Six models.** Separate models were trained for the 30-, 60-, and 90-day horizons.
  For each horizon, an XGBoost regressor predicts the future price of urea and a
  separate XGBoost classifier predicts the probability that the market moves up or
  down.
- **Training data.** The models were trained on a 25-year dataset (1997–2024) built
  from free, public World Bank and EIA data. A randomized 15% of the data was held out
  as a blind test set.
- **Risk engine.** Walk-forward cross-validation produced a historical error
  distribution, which feeds a Monte Carlo engine. The engine runs 10,000 simulated
  price paths to produce confidence intervals, such as P10 and P90 worst cases, so
  farmers can weigh buying now against waiting.
- **Result.** The model predicts the direction of fertilizer prices 90 days out with
  about 75% accuracy, averaged across 50 training runs.

## Challenges

The model initially struggled with the 2021–2022 fertilizer price spikes. When tested
on the calmer 2023–2024 period, it predicted huge upward swings because it
over-weighted the 2022 volatility. The team fixed this by weighting years by how
recent they are and switching the classifier to a binary logistic objective.

Halfway through the 24 hours, the team stopped coding to agree on who the product was
for, and refocused it as a farmer-first tool rather than an abstract financial
dashboard.

## Built with

Python · XGBoost · pandas · NumPy · Plotly · Streamlit · SQLite · Docker · Railway ·
World Bank and EIA data · Claude
