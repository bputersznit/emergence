#!/usr/bin/env python3
import random
import tkinter as tk
from tkinter import ttk


def build_deck():
    suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    deck = [(rank, suit) for suit in suits for rank in ranks]
    deck.append(("Joker", "Red"))
    deck.append(("Joker", "Black"))
    return deck


def card_suit_symbol(suit):
    return {
        "Clubs": "♣",
        "Diamonds": "♦",
        "Hearts": "♥",
        "Spades": "♠",
    }[suit]


def card_suit_color(suit):
    return "#b00020" if suit in ("Hearts", "Diamonds") else "#1a1a1a"


def suit_interpretation(suit):
    return {
        "Clubs": "Intuition/Motivation (Internal State)",
        "Diamonds": "Perception/Actions (Performance)",
        "Hearts": "Relationship/Manuver (Tactics)",
        "Spades": "Understanding/Planning (Stratgy)",
    }[suit]


def skill_aspect_for_suit(suit):
    return {
        "Clubs": "Focus",
        "Diamonds": "Technique",
        "Hearts": "Tactics",
        "Spades": "Strategy",
    }[suit]


def card_text_color(rank, suit):
    if rank == "Joker":
        return "#b00020" if suit == "Red" else "#1a1a1a"
    return card_suit_color(suit)


def suit_color_name(rank, suit):
    if rank == "Joker":
        return "Red" if suit == "Red" else "Black"
    return "Red" if suit in ("Hearts", "Diamonds") else "Black"


def joker_symbol(suit):
    return "🃏" if suit == "Black" else "🃟"


def draw_card_image(canvas, rank, suit, card_width, card_height, offset_x=0, offset_y=0, scale=1.0):
    padding = 12
    scaled_width = card_width * scale
    scaled_height = card_height * scale

    card_left = padding + offset_x
    card_top = padding + offset_y
    card_right = card_left + scaled_width
    card_bottom = card_top + scaled_height

    # Card base
    canvas.create_rectangle(
        card_left,
        card_top,
        card_right,
        card_bottom,
        outline="#2b2b2b",
        width=2,
        fill="#f8f7f4",
    )

    if rank == "Joker":
        accent = "#b00020" if suit == "Red" else "#1a1a1a"
        corner_symbol = joker_symbol(suit)
        canvas.create_text(
            card_left + 16,
            card_top + 18,
            text=corner_symbol,
            font=("TkDefaultFont", int(21 * scale), "bold"),
            fill=accent,
        )
        canvas.create_text(
            card_right - 16,
            card_bottom - 18,
            text=corner_symbol,
            font=("TkDefaultFont", int(21 * scale), "bold"),
            fill=accent,
        )
        canvas.create_text(
            (card_left + card_right) / 2,
            (card_top + card_bottom) / 2 - 12,
            text=joker_symbol(suit),
            font=("TkDefaultFont", int(84 * scale), "bold"),
            fill=accent,
        )
        canvas.create_text(
            (card_left + card_right) / 2,
            (card_top + card_bottom) / 2 + 30,
            text=f"JOKER ({suit})",
            font=("TkDefaultFont", int(18 * scale), "bold"),
            fill=accent,
        )
        return

    symbol = card_suit_symbol(suit)
    color = card_suit_color(suit)

    # Corner labels
    canvas.create_text(
        card_left + 16,
        card_top + 18,
        text=rank,
        font=("TkDefaultFont", int(21 * scale), "bold"),
        fill=color,
    )
    canvas.create_text(
        card_left + 16,
        card_top + 36,
        text=symbol,
        font=("TkDefaultFont", int(18 * scale), "bold"),
        fill=color,
    )

    canvas.create_text(
        card_right - 16,
        card_bottom - 36,
        text=symbol,
        font=("TkDefaultFont", int(18 * scale), "bold"),
        fill=color,
    )
    canvas.create_text(
        card_right - 16,
        card_bottom - 18,
        text=rank,
        font=("TkDefaultFont", int(21 * scale), "bold"),
        fill=color,
    )

    # Center emblem
    canvas.create_text(
        (card_left + card_right) / 2,
        (card_top + card_bottom) / 2,
        text=symbol,
        font=("TkDefaultFont", int(78 * scale), "bold"),
        fill=color,
    )


def draw_card_stack(canvas, cards, card_width, card_height, stack_offset=32, max_stack=8, allow_scale=True):
    canvas.delete("all")
    if not cards:
        return

    stack_offset = stack_offset
    max_stack = max_stack
    start = max(0, len(cards) - max_stack)
    visible_cards = cards[start:]

    # Only scale if more than 5 cards are visible.
    if not allow_scale or len(visible_cards) <= 5:
        scale = 1.0
    else:
        padding = 12
        base_inner_width = card_width
        max_offset = (len(visible_cards) - 1) * stack_offset
        if base_inner_width > 0:
            scale = (card_width - max_offset) / base_inner_width
        else:
            scale = 1.0
        scale = max(0.6, min(1.0, scale))
    for idx, (rank, suit) in enumerate(visible_cards):
        offset_x = idx * stack_offset
        offset_y = 0
        draw_card_image(
            canvas,
            rank,
            suit,
            card_width,
            card_height,
            offset_x=offset_x,
            offset_y=offset_y,
            scale=scale,
        )


def main():
    deck = []
    history = []
    draw_batches = []

    root = tk.Tk()
    root.title("GoE Card Draw")
    # Poker size ratio: 2.5" x 3.5" -> 5:7 aspect
    card_width = 250
    card_height = 350
    stack_offset = 32
    max_visible = 5
    canvas_width = card_width + (max_visible - 1) * stack_offset + 24
    canvas_height = card_height + 24

    root.geometry("780x1000")
    root.minsize(780, 1000)
    root.resizable(True, True)

    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    container = ttk.Frame(root, padding=16)
    container.pack(fill="both", expand=True)

    title = ttk.Label(container, text="Draw a Card", font=("TkDefaultFont", 24, "bold"))
    title.pack(pady=(0, 8))

    card_canvas = tk.Canvas(
        container,
        width=canvas_width,
        height=canvas_height,
        highlightthickness=0,
        bg="#e7e1d5",
    )
    card_canvas.pack(pady=(0, 10))

    card_var = tk.StringVar(value="Press the button to draw")
    card_label = ttk.Label(container, textvariable=card_var, font=("TkDefaultFont", 18))
    card_label.pack(pady=(0, 10))

    history_text = tk.Text(
        container,
        height=4,
        wrap="word",
        font=("TkDefaultFont", 15),
    )
    history_text.pack(pady=(0, 10), fill="x")
    history_text.insert("1.0", "Drawn: ")
    history_text.config(state="disabled")

    interpretation_var = tk.StringVar(value="Suit Meaning: ")
    interpretation_label = ttk.Label(
        container,
        textvariable=interpretation_var,
        font=("TkDefaultFont", 15),
        wraplength=700,
        justify="left",
    )
    interpretation_label.pack(pady=(0, 10))

    outcome_var = tk.StringVar(value="Outcome: ")
    outcome_label = ttk.Label(
        container,
        textvariable=outcome_var,
        font=("TkDefaultFont", 15),
        wraplength=700,
        justify="left",
    )
    outcome_label.pack(pady=(0, 10))

    adv_var = tk.StringVar(value="")
    adv_label = ttk.Label(
        container,
        textvariable=adv_var,
        font=("TkDefaultFont", 15),
        wraplength=700,
        justify="left",
    )
    adv_label.pack(pady=(0, 6))

    xp_var = tk.StringVar(value="")
    xp_label = ttk.Label(
        container,
        textvariable=xp_var,
        font=("TkDefaultFont", 15),
        wraplength=700,
        justify="left",
    )
    xp_label.pack(pady=(0, 10))

    def format_card_short(rank, suit):
        if rank == "Joker":
            return joker_symbol(suit)
        return f"{card_suit_symbol(suit)}{rank}"

    def update_history():
        history_text.config(state="normal")
        history_text.delete("1.0", "end")
        history_text.insert("1.0", "Drawn: ")
        for idx, (token, color, is_separator) in enumerate(history):
            if is_separator:
                history_text.insert("end", "; ")
                continue
            tag = f"card_{idx}"
            history_text.tag_configure(tag, foreground=color)
            history_text.insert("end", f"{token} ", tag)
        history_text.config(state="disabled")

    pip_ranks = {"A", "2", "3", "4", "5", "6", "7", "8", "9", "10"}

    def draw_card():
        nonlocal deck
        last_rank = None
        last_suit = None
        drawn_cards = []
        drawn_this_press = []
        while True:
            if not deck:
                deck = build_deck()
                random.shuffle(deck)
            rank, suit = deck.pop()
            drawn_cards.append((rank, suit))
            drawn_this_press.append((format_card_short(rank, suit), card_text_color(rank, suit)))
            if rank in pip_ranks:
                last_rank = rank
                last_suit = suit
                break
        if last_rank == "Joker":
            card_var.set(f"Joker ({last_suit})")
            interpretation_var.set("Suit Meaning: Joker")
            outcome_var.set("Outcome: ")
        else:
            card_var.set(f"{last_rank} of {last_suit}")
            interpretation_var.set(f"Suit Meaning: {suit_interpretation(last_suit)}")
            pip_color = suit_color_name(last_rank, last_suit)
            face_matches = 0
            face_mismatches = 0
            face_count = 0
            joker_count = 0
            for rank, suit in drawn_cards:
                if rank in {"J", "Q", "K"}:
                    face_count += 1
                    if suit_color_name(rank, suit) == pip_color:
                        face_matches += 1
                    else:
                        face_mismatches += 1
                elif rank == "Joker":
                    joker_count += 1
            net_advantage = face_matches - face_mismatches
            outcome_parts = []
            adv_var.set("")
            xp_var.set("")
            if face_count > 0:
                if net_advantage > 0:
                    adv_var.set(f"Advantage: +{net_advantage}")
                    outcome_parts.append(f"Advantage +{net_advantage}")
                elif net_advantage < 0:
                    adv_var.set(f"Disadvantage: {net_advantage}")
                    outcome_parts.append(f"Disadvantage {net_advantage}")
                else:
                    adv_var.set("Adv/Dis: Neutral (0)")
                    outcome_parts.append("Neutral (0)")
            if joker_count > 0:
                xp_var.set(f"PoV XP: +{joker_count} -> {skill_aspect_for_suit(last_suit)}")
                outcome_parts.append(
                    f"PoV XP +{joker_count} -> {skill_aspect_for_suit(last_suit)}"
                )
            if not outcome_parts:
                outcome_parts.append("Neutral (0)")
            outcome_var.set("Outcome: " + " | ".join(outcome_parts))
        card_label.configure(foreground=card_text_color(last_rank, last_suit))
        draw_card_stack(
            card_canvas,
            drawn_cards,
            card_width,
            card_height,
            stack_offset=stack_offset,
            max_stack=8,
            allow_scale=False,
        )
        for token, color in drawn_this_press:
            history.append((token, color, False))
        history.append(("", "", True))
        draw_batches.append(drawn_cards)
        update_history()

    def reshuffle():
        nonlocal deck, history, draw_batches
        deck = build_deck()
        random.shuffle(deck)
        history = []
        draw_batches = []
        card_var.set("Press the button to draw")
        interpretation_var.set("Suit Meaning: ")
        outcome_var.set("Outcome: ")
        adv_var.set("")
        xp_var.set("")
        card_label.configure(foreground="#1a1a1a")
        card_canvas.delete("all")
        update_history()

    def go_back_one_draw():
        nonlocal deck, history, draw_batches
        if not draw_batches:
            return
        last_batch = draw_batches.pop()
        # Return cards to the top of the deck in reverse draw order.
        for rank, suit in reversed(last_batch):
            deck.append((rank, suit))

        # Remove history entries for the last batch plus its separator.
        remove_count = len(last_batch) + 1
        if remove_count <= len(history):
            history = history[:-remove_count]
        else:
            history = []

        # Update display to previous batch or reset.
        if draw_batches:
            prev_batch = draw_batches[-1]
            prev_rank, prev_suit = prev_batch[-1]
            if prev_rank == "Joker":
                card_var.set(f"Joker ({prev_suit})")
                interpretation_var.set("Suit Meaning: Joker")
                outcome_var.set("Outcome: ")
                adv_var.set("")
                xp_var.set("")
            else:
                card_var.set(f"{prev_rank} of {prev_suit}")
                interpretation_var.set(f"Suit Meaning: {suit_interpretation(prev_suit)}")
                pip_color = suit_color_name(prev_rank, prev_suit)
                face_matches = 0
                face_mismatches = 0
                face_count = 0
                joker_count = 0
                for rank, suit in prev_batch:
                    if rank in {"J", "Q", "K"}:
                        face_count += 1
                        if suit_color_name(rank, suit) == pip_color:
                            face_matches += 1
                        else:
                            face_mismatches += 1
                    elif rank == "Joker":
                        joker_count += 1
                net_advantage = face_matches - face_mismatches
                outcome_parts = []
                adv_var.set("")
                xp_var.set("")
                if face_count > 0:
                    if net_advantage > 0:
                        adv_var.set(f"Advantage: +{net_advantage}")
                        outcome_parts.append(f"Advantage +{net_advantage}")
                    elif net_advantage < 0:
                        adv_var.set(f"Disadvantage: {net_advantage}")
                        outcome_parts.append(f"Disadvantage {net_advantage}")
                    else:
                        adv_var.set("Adv/Dis: Neutral (0)")
                        outcome_parts.append("Neutral (0)")
                if joker_count > 0:
                    xp_var.set(
                        f"PoV XP: +{joker_count} -> {skill_aspect_for_suit(prev_suit)}"
                    )
                    outcome_parts.append(
                        f"PoV XP +{joker_count} -> {skill_aspect_for_suit(prev_suit)}"
                    )
                if not outcome_parts:
                    outcome_parts.append("Neutral (0)")
                outcome_var.set("Outcome: " + " | ".join(outcome_parts))
            card_label.configure(foreground=card_text_color(prev_rank, prev_suit))
            draw_card_stack(
                card_canvas,
                prev_batch,
                card_width,
                card_height,
                stack_offset=stack_offset,
                max_stack=8,
                allow_scale=False,
            )
        else:
            card_var.set("Press the button to draw")
            interpretation_var.set("Suit Meaning: ")
            outcome_var.set("Outcome: ")
            adv_var.set("")
            xp_var.set("")
            card_label.configure(foreground="#1a1a1a")
            card_canvas.delete("all")
        update_history()

    draw_button = ttk.Button(container, text="Draw Card", command=draw_card)
    draw_button.pack(pady=(0, 6))

    draw_another_button = ttk.Button(container, text="Draw Another Card", command=draw_card)
    draw_another_button.pack()

    go_back_button = ttk.Button(container, text="Go Back One Draw", command=go_back_one_draw)
    go_back_button.pack(pady=(6, 0))

    reshuffle_button = ttk.Button(container, text="Reshuffle Deck", command=reshuffle)
    reshuffle_button.pack(pady=(6, 0))

    # Initial draw to show a card image
    draw_card()

    root.mainloop()


if __name__ == "__main__":
    main()
