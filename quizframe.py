import customtkinter as ctk
from tkinter import messagebox
import random
from gameoverframe import GameOverFrame

class QuizFrame(ctk.CTkFrame):
    def __init__(self, master, question_data, selected_language):
        super().__init__(master)

        self.selected_language = selected_language
        self.question_data = question_data 
        self.score = 0
        self.question_count = 0 

        self.load_new_question()

        self.label = ctk.CTkLabel(self, text=f"Translate this word: {self.question}", font=("Arial", 20))
        self.entry_answer = ctk.CTkEntry(self, font=("Arial", 14))
        self.next_button = ctk.CTkButton(self, text="Next", font=("Arial", 14), command=self.next_question)

        self.label.pack(pady=20)
        self.entry_answer.pack(pady=10)
        self.next_button.pack(pady=20) 

    def load_new_question(self):
        """Load a new random question."""
        self.index = random.randint(0, 49)
        self.question = self.question_data[self.selected_language][self.index][0]
        self.answer = self.question_data[self.selected_language][self.index][1]

    def next_question(self):
        """Handle the logic when the user submits an answer."""
        user_answer = self.entry_answer.get().strip()
        if user_answer.lower() == self.answer.lower():
            messagebox.showinfo("Correct!", "Your answer is correct!")
            self.score += 1
        else:
            messagebox.showerror("Wrong!", f"The correct answer was: {self.answer}")

        self.question_count += 1

        if self.question_count >= 5:
            self.end_game()
        else:
            self.load_new_question()
            self.label.configure(text=f"Translate this word: {self.question}")
            self.entry_answer.delete(0, 'end')

            # self.entry_answer.pack_forget()
            self.entry_answer.pack(pady=10)
    
    def end_game(self):
        """End the game after 10 questions."""
        messagebox.showinfo("Game Over", "You have completed 5 questions!")
        # Switch to the Game Over frame or perform other actions to end the game
        self.master.switch_frame(GameOverFrame(self.master, self.score))  # Assuming GameOverFrame is defined
