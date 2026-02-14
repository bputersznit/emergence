# Project Agent Notes

## Purpose
Ubuntu GUI app that draws cards from a 54-card deck (52 + 2 jokers), with a draw-until-pip behavior and a visual stack of cards.

## Design Intent
- Use a standard poker card aspect ratio of 5:7 (width:height).
- Keep card size constant (no scaling for up to 5 stacked cards).
- Stack cards with right-side peeking so previous cards show on the right; pip card on top.
- Corner indices/symbols must remain fully visible in the stack.
- Jokers use Unicode symbols:
  - Black Joker: U+1F0CF (🃏)
  - Red Joker: U+1F0BF (🃟)
- Show joker symbols in the corners for visibility in a stack.
- History line shows each draw; each press is separated by a semicolon placed after the pip card.
- Each card in history is colored according to its suit (red/black).

## Behavior
- Each button press draws repeatedly until a pip card is drawn (A–10).
- Maintain a draw history for the session.
- Provide a "Go Back One Draw" action that undoes the last draw batch and restores those cards to the deck in reverse draw order.
- Provide a "Reshuffle Deck" action that resets history and deck.

## Files
- `app.py`: main app
- `GoE-Card Draw.py`: variant with same behavior and a different window title

## Window/Layout
- Window must be large enough to show all buttons without resizing.
- Canvas width should allow up to 5 cards without scaling.

## Git
- Repo is initialized locally and has a remote named `emergence`.
- Network access for this environment may be restricted; `git push` can fail with DNS resolution errors here even if it works in a normal terminal.
