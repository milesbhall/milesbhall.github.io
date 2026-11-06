---
name: GreenMachine
description: An ecologically conscious product-suggestion chatbot that uses Gemini to learn what a shopper values, then scores products from a database to steer them toward safer, greener alternatives.
event: "&Hacks XI"
award: 1st place in the Ferguson Challenge
date: 2025-09-01
team: With a partner
thumbnail: /images/projects/greenmachine.svg
links:
  - label: GitHub
    url: https://github.com/milesbhall/-Hacks
  - label: Devpost
    url: https://devpost.com/software/ferguson-ai
---

## Inspiration

GreenMachine came from wanting to drive environmentally friendly consumer choices.
It nudges shoppers toward products with higher standards of safety and environmental
consciousness, and it's designed to be easy for businesses to add to their online
stores.

## What it does

GreenMachine is two things: a chatbot and an algorithm.

1. After a shopper picks a product, the chatbot starts a conversation to find out
   what they value about it. For example, if the product is ADA compliant, the chatbot
   works out whether the shopper cares about ADA compliance.
2. Gemini analyzes the conversation and scores the shopper's priorities from 0.0 to
   1.0 across environmental sustainability, product safety, and product match.
3. Those scores weight an algorithm that searches a SQLite product database and
   returns the three best-scoring products.

It's aimed at businesses with large numbers of SKUs and overwhelming search filters,
giving them a simple, friendly way to match customers with greener products.

## Design choice

Ranking happens in a conventional algorithm rather than in the language model.
Having Gemini scan a database of thousands of items would have been inefficient and
wasted energy.

## Built with

Python · Google Gemini API · SQLite

## What's next

Next steps are more weighted variables, a better user experience, a database that
changes in real time, and integration into a web storefront.
