import tkinter as tk
from ttkthemes import ThemedTk
from tkinter import ttk
from tkinter import simpledialog, messagebox




# Window
window = ThemedTk(theme="arc")
window.title("Flashcard Quiz App")
window.geometry("700x500")



# Flashcards
flashcards = [
    {
        "question": "What is Python?",
        "answer": "Python is a programming language."
    },
    {
        "question": "What is a variable?",
        "answer": "A variable stores data."
    },
    {
        "question": "What is a list?",
        "answer": "A list stores multiple items."
    }
]

current_card = 0

# Title
title_label = ttk.Label(
    window,
    text="🧠 Flashcard Quiz",
    font=("Arial", 28, "bold")
)
title_label.pack(pady=25)

# Card
card_frame = ttk.Frame(window, padding=30)
card_frame.pack(padx=40, pady=20, fill="both", expand=True)

# NEW: label that shows whether the card is on "QUESTION" or "ANSWER"
state_label = ttk.Label(
    card_frame,
    text="QUESTION",
    font=("Arial", 12, "bold")
)
state_label.pack(pady=(0, 10))

question_label = ttk.Label(
    card_frame,
    text=flashcards[current_card]["question"],
    font=("Arial", 20),
    anchor="center",
    justify="center"
)
question_label.pack(expand=True)

# NEW: label that shows "Card X of Y"
counter_label = ttk.Label(
    card_frame,
    text=f"Card 1 of {len(flashcards)}",
    font=("Arial", 11)
)
counter_label.pack(pady=(10, 0))

# Show answer
def show_answer():
    question_label.config(
        text=flashcards[current_card]["answer"]
    )
    state_label.config(text="ANSWER")

# Next card
def next_card():
    global current_card

    if current_card < len(flashcards) - 1:
        current_card += 1
    else:
        current_card = 0

    question_label.config(
        text=flashcards[current_card]["question"]
    )
    state_label.config(text="QUESTION")
    counter_label.config(text=f"Card {current_card + 1} of {len(flashcards)}")

# Previous card
def previous_card():
    global current_card

    if current_card > 0:
        current_card -= 1
    else:
        current_card = len(flashcards) - 1

    question_label.config(
        text=flashcards[current_card]["question"]
    )
    state_label.config(text="QUESTION")
    counter_label.config(text=f"Card {current_card + 1} of {len(flashcards)}")
    

def show_question():
    question_label.config(
        text=flashcards[current_card]["question"]
    )
    state_label.config(text="QUESTION")
    counter_label.config(text=f"Card {current_card + 1} of {len(flashcards)}")
    
    
def add_card():
    question = simpledialog.askstring(
        "Add Card",
        "Enter your question:"
    )

    if not question:
        return

    answer = simpledialog.askstring(
        "Add Card",
        "Enter your answer:"
    )

    if not answer:
        return

    flashcards.append({
        "question": question,
        "answer": answer
    })

    global current_card
    current_card = len(flashcards) - 1

    show_question()

    messagebox.showinfo(
        "Success",
        "New flashcard added!"
    )
    
def edit_card():
    old_question = flashcards[current_card]["question"]
    old_answer = flashcards[current_card]["answer"]

    new_question = simpledialog.askstring(
        "Edit Card",
        "Edit question:",
        initialvalue=old_question
    )

    if not new_question:
        return

    new_answer = simpledialog.askstring(
        "Edit Card",
        "Edit answer:",
        initialvalue=old_answer
    )

    if not new_answer:
        return

    flashcards[current_card]["question"] = new_question
    flashcards[current_card]["answer"] = new_answer

    show_question()

    messagebox.showinfo(
        "Success",
        "Flashcard updated!"
    )   

def delete_card():
    global current_card

    if len(flashcards) == 0:
        return

    confirm = messagebox.askyesno(
        "Delete Card",
        "Are you sure you want to delete this card?"
    )

    if confirm:
        flashcards.pop(current_card)

        if len(flashcards) == 0:
            question_label.config(text="No flashcards available.")
            state_label.config(text="")
            counter_label.config(text="Card 0 of 0")
            return

        if current_card >= len(flashcards):
            current_card = len(flashcards) - 1

        show_question()


# Buttons
button_frame = ttk.Frame(window)
button_frame.pack(pady=20)

previous_button = ttk.Button(
    button_frame,
    text="← Previous",
    command=previous_card
)
previous_button.grid(row=0, column=0, padx=10)

answer_button = ttk.Button(
    button_frame,
    text="Show Answer",
    command=show_answer
)
answer_button.grid(row=0, column=1, padx=10)

next_button = ttk.Button(
    button_frame,
    text="Next →",
    command=next_card
)
next_button.grid(row=0, column=2, padx=10)

management_frame = ttk.Frame(window)
management_frame.pack(pady=15)

add_button = ttk.Button(
    management_frame,
    text="＋ Add Card",
    command=add_card
)

add_button.grid(
    row=0,
    column=0,
    padx=8
)

edit_button = ttk.Button(
    management_frame,
    text="✎ Edit Card",
    command=edit_card
)

edit_button.grid(
    row=0,
    column=1,
    padx=8
)
delete_button = ttk.Button(
    management_frame,
    text="✕ Delete Card",
    command=delete_card
)

delete_button.grid(
    row=0,
    column=2,
    padx=8
)

window.mainloop()
