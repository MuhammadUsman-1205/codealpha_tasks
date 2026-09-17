"""
Random Quote Generator — CustomTkinter edition
A modern-looking desktop app built with CustomTkinter.

Install once:   pip install customtkinter
Run with:        python quote_app_ctk.py
"""

import random
import customtkinter as ctk

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

QUOTES = [
    {"text": "The unexamined life is not worth living.", "author": "Socrates"},
    {"text": "It is not that we have a short time to live, but that we waste a lot of it.", "author": "Seneca"},
    {"text": "Whatever you are, be a good one.", "author": "Abraham Lincoln"},
    {"text": "The only way to do great work is to love what you do.", "author": "Steve Jobs"},
    {"text": "In the middle of difficulty lies opportunity.", "author": "Albert Einstein"},
    {"text": "What we think, we become.", "author": "Buddha"},
    {"text": "Turn your wounds into wisdom.", "author": "Oprah Winfrey"},
    {"text": "The journey of a thousand miles begins with one step.", "author": "Lao Tzu"},
    {"text": "Simplicity is the ultimate sophistication.", "author": "Leonardo da Vinci"},
    {"text": "Not all those who wander are lost.", "author": "J.R.R. Tolkien"},
    {"text": "I think, therefore I am.", "author": "René Descartes"},
    {"text": "The only true wisdom is in knowing you know nothing.", "author": "Socrates"},
    {"text": "Life is what happens when you're busy making other plans.", "author": "John Lennon"},
    {"text": "The future belongs to those who believe in the beauty of their dreams.", "author": "Eleanor Roosevelt"},
    {"text": "It always seems impossible until it's done.", "author": "Nelson Mandela"},
    {"text": "You must be the change you wish to see in the world.", "author": "Mahatma Gandhi"},
    {"text": "Do not go where the path may lead; go instead where there is no path and leave a trail.", "author": "Ralph Waldo Emerson"},
    {"text": "Two roads diverged in a wood, and I took the one less traveled by.", "author": "Robert Frost"},
    {"text": "That which does not kill us makes us stronger.", "author": "Friedrich Nietzsche"},
    {"text": "The only impossible journey is the one you never begin.", "author": "Tony Robbins"},
    {"text": "Be yourself; everyone else is already taken.", "author": "Oscar Wilde"},
    {"text": "A room without books is like a body without a soul.", "author": "Cicero"},
    {"text": "Success is not final, failure is not fatal: it is the courage to continue that counts.", "author": "Winston Churchill"},
    {"text": "Everything you can imagine is real.", "author": "Pablo Picasso"},
    {"text": "Genius is one percent inspiration and ninety-nine percent perspiration.", "author": "Thomas Edison"},
    {"text": "The best way to predict the future is to create it.", "author": "Peter Drucker"},
    {"text": "Happiness is not something ready made. It comes from your own actions.", "author": "Dalai Lama"},
]

# ---------------------------------------------------------------------------
# Look & feel
# ---------------------------------------------------------------------------

ACCENT = "#7C5CFF"          # violet accent used for the button + quote mark
ACCENT_HOVER = "#6845FF"
CARD_RADIUS = 20
BUTTON_RADIUS = 12

ctk.set_appearance_mode("dark")          # "dark", "light", or "system"
ctk.set_default_color_theme("dark-blue")  # base theme; overridden by our own colors


class QuoteApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Quotidian")
        self.geometry("560x420")
        self.minsize(440, 380)

        self.last_index = None

        # ------------------------------------------------------------------
        # Top bar: app name + light/dark toggle
        # ------------------------------------------------------------------
        topbar = ctk.CTkFrame(self, fg_color="transparent")
        topbar.pack(fill="x", padx=28, pady=(24, 0))

        ctk.CTkLabel(
            topbar, text="Quotidian",
            font=ctk.CTkFont(family="Helvetica", size=14, weight="bold"),
            
            text_color=("gray20", "gray70")
        ).pack(side="left")

        self.mode_switch = ctk.CTkSegmentedButton(
            topbar, values=["Light", "Dark"],
            command=self.toggle_appearance,
            width=140, height=28
        )
        self.mode_switch.set("Dark")
        self.mode_switch.pack(side="right")

        # ------------------------------------------------------------------
        # Card holding the quote
        # ------------------------------------------------------------------
        self.card = ctk.CTkFrame(
            self, corner_radius=CARD_RADIUS,
            fg_color=("white", "#1E1E24"),
            border_width=1, border_color=("gray85", "gray25")
        )
        self.card.pack(expand=True, fill="both", padx=28, pady=24)

        inner = ctk.CTkFrame(self.card, fg_color="transparent")
        inner.place(relx=0.5, rely=0.5, anchor="center")

        self.mark_label = ctk.CTkLabel(
            inner, text="\u201C",
            font=ctk.CTkFont(family="Georgia", size=52, weight="bold"),
            text_color=ACCENT
        )
        self.mark_label.pack(pady=(0, 0))

        self.quote_label = ctk.CTkLabel(
            inner, text="", justify="center",
            font=ctk.CTkFont(family="Helvetica", size=19),
            text_color=("gray10", "gray95"),
            wraplength=440
        )
        self.quote_label.pack(pady=(4, 18))

        self.author_label = ctk.CTkLabel(
            inner, text="",
            font=ctk.CTkFont(family="Helvetica", size=13, weight="bold"),
            text_color=("gray40", "gray60")
        )
        self.author_label.pack()

        # ------------------------------------------------------------------
        # Bottom: New Quote button + counter
        # ------------------------------------------------------------------
        bottom = ctk.CTkFrame(self, fg_color="transparent")
        bottom.pack(fill="x", padx=28, pady=(0, 28))

        self.button = ctk.CTkButton(
            bottom, text="New Quote",
            font=ctk.CTkFont(family="Helvetica", size=14, weight="bold"),
            corner_radius=BUTTON_RADIUS, height=44,
            fg_color=ACCENT, hover_color=ACCENT_HOVER,
            command=self.show_random_quote
        )
        self.button.pack(fill="x")

        self.counter_label = ctk.CTkLabel(
            bottom, text="", font=ctk.CTkFont(size=11),
            text_color=("gray55", "gray50")
        )
        self.counter_label.pack(pady=(10, 0))

        # Show a quote as soon as the app opens
        self.show_random_quote()

    # -----------------------------------------------------------------------
    def toggle_appearance(self, choice):
        ctk.set_appearance_mode(choice.lower())

    def show_random_quote(self):
        """Pick a random quote, avoiding an immediate repeat."""
        if len(QUOTES) > 1:
            index = self.last_index
            while index == self.last_index:
                index = random.randint(0, len(QUOTES) - 1)
        else:
            index = 0

        self.last_index = index
        quote = QUOTES[index]

        self.quote_label.configure(text=quote["text"])
        self.author_label.configure(text=f"— {quote['author']}")
        self.counter_label.configure(text=f"Quote {index + 1} of {len(QUOTES)}")


def main():
    app = QuoteApp()
    app.mainloop()


if __name__ == "__main__":
    main()
