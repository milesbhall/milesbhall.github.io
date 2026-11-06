---
name: Shelf-Life Guard
description: A safeguard for a delivery-time prediction system that screens, re-weights, and double-checks incoming delivery records so outdated data and sloppy scans don't quietly make delivery promises wrong.
event: Case-a-thon II
award: 1st overall
date: 2026-10-01
team: Team of three
thumbnail: /images/projects/shelf-life-guard.svg
links:
  - label: Project site
    url: https://1628745.github.io/Case-a-thon2026/
---

## The problem

A delivery-time model tells customers when a package will arrive, and it retrains
weekly on recent deliveries. When bad records flow into that retraining, nothing on
screen warns anyone, and the delivery promises quietly drift.

The project looks at three ordinary ways the data goes bad:

- **Outdated data:** old history is kept at full weight, and courier and area
  statistics stop refreshing.
- **Sloppy scanning:** couriers mark whole stacks of packages as delivered at the
  end of a shift, and some records are uploaded twice.
- **Both at once:** the two problems combined.

Of these, sloppy scans added far more error per package than outdated data did.

## How the Guard works

The Guard adds three checks:

1. **Check at the door.** New records are screened for warning signs: many packages
   marked delivered in the same minute, duplicate uploads, and impossible times or
   distances. Suspicious records are down-weighted rather than deleted.
2. **Weigh by trust.** Recent records count more. Couriers whose records disagree
   with peers in the same area and hour count less. Older statistics are kept, and a
   person is alerted.
3. **Final check before promising.** The promise is tuned to be on time about four
   out of five times. Unusual packages, such as those in areas the model hasn't seen
   or with very uncertain predictions, go to a dispatcher.

## Built with

- Two LightGBM gradient-boosted regressors: a median model and an 80th-percentile
  (P80) model
- Conformal calibration of the P80 promise for each area type
- The LaDe Chongqing last-mile delivery dataset

The project site includes a **Try it** page that runs entirely in the browser, so
uploaded files are never sent anywhere, and it publishes no raw records, courier IDs,
or locations.
