---
layout: single
title: "American Mahjong Analyzer"
description: "A C++ project exploring American Mahjong hand analysis, tile counting, and eventually probability-based discard recommendations."
category: project
date: 2026-10-29
classes: wide
author_profile: true
---

**American Mahjong Analyzer** is a C++ project I'm building to explore game strategy through algorithms, combinatorics, and probability. The long-term goal is to evaluate a player's hand against winning combinations on an American Mahjong card and recommend moves based on the chances of completing a hand.

Unlike Mahjong variants with a fixed set of winning structures, American Mahjong uses a card of designated hands that changes by year. That makes card-pattern representation and rule-aware matching essential parts of the problem.

## Current implementation

The initial command-line program focuses on tile representation and validation:

- **Tile types:** C++ `enum class` and `struct` definitions for numbered tiles, winds, dragons, flowers, and jokers.
- **Hand input:** parsing user-entered tiles into a structured hand.
- **Physical tile limits:** rejecting hands with more copies of a tile than exist in a set.
- **Frequency counting:** a 36-entry array representing the number of copies of each tile type.

## Planned algorithms

1. **Card-based hand matching:** encode target patterns and measure how many tiles are needed to complete each one.
2. **Joker-aware evaluation:** account for the restrictions on how jokers can substitute within a hand.
3. **Discard recommendations:** compare legal discards based on their effect on promising target hands.
4. **Tile probabilities:** use visible and unseen tile counts to estimate the likelihood of useful draws.
5. **Simulation:** explore Monte Carlo methods for comparing strategies under uncertainty.

**[View the code on GitHub](https://github.com/JiayuEllieSu/mahjong-analyzer)**
