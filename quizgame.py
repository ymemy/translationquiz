import customtkinter as ctk
from tkinter import messagebox

class TranslationQuiz:
    def __init__(self, root):
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.root = root
        self.root.title("Who's the best translator?")
        self.root.geometry("600x400")

        self.translation_data = {
            "What is your name?": {"French": "Comment vous appelez-vous?", "Spanish": "¿Cómo te llamas?"},
            "Good morning": {"French": "Bonjour", "Spanish": "Buenos días"},
            "Thank you": {"French": "Merci", "Spanish": "Gracias"}
        }
        self.questions = list(self.translation_data.keys())
        self.selected_language = None

        self.current_question = 0
        self.player_scores = [0, 0]  # Scores for Player 1 and Player 2
        self.current_player = 0 # 0 for Player 1, 1 for Player 2

        # Frames
        self.home_frame = ctk.CTkFrame(root)
        self.quiz_frame = ctk.CTkFrame(root)
        
        self.create_home_screen()
        self.create_quiz_screen()
        
        self.show_frame(self.home_frame)  # Show the home screen initially

    def show_frame(self, frame):
        """Switch between frames."""
        self.home_frame.pack_forget()
        self.quiz_frame.pack_forget()
        frame.pack(fill="both", expand=True, padx=20, pady=20)

    def create_home_screen(self):
        """Creates the home screen with rules."""
        title = ctk.CTkLabel(self.home_frame, text="Welcome to the Translation Quiz!", font=("Arial", 20))
        title.pack(pady=20)
        
        rules = (
            "Rules:\n"
            "1. This is a two-player game.\n"
            "2. Players will take turns translating prompts.\n"
            "3. Each correct answer earns 1 point.\n"
            "4. The player with the most points at the end wins!\n"
        )
        rules_label = ctk.CTkLabel(self.home_frame, text=rules, font=("Arial", 14), justify="left")
        rules_label.pack(pady=20)
        
        # Language selection
        language_label = ctk.CTkLabel(self.home_frame, text="Select the source language:", font=("Arial", 14))
        language_label.pack(pady=10)
        
        # Languages drop down menu
        self.language_var = ctk.StringVar(value="Français")
        languages = ["Français", "Español", "Deutsch", "日本語", "中文"]
        self.language_dropdown = ctk.CTkComboBox(self.home_frame, variable=self.language_var, values=languages)
        self.language_dropdown.pack(pady=10)

        start_button = ctk.CTkButton(self.home_frame, text="Start Quiz", font=("Arial", 16), command=lambda: self.show_frame(self.quiz_frame))
        start_button.pack(pady=20)
    
    def start_quiz(self):
        """Starts the quiz with the selected language."""
        self.selected_language = self.language_var.get()
        self.show_frame(self.quiz_frame)
        self.display_question()
    
    def create_quiz_screen(self):
        """Creates the quiz screen with translation input."""
        self.player_label = ctk.CTkLabel(self.quiz_frame, text="Player 1's Turn", font=("Arial", 16), text_color="white")
        self.player_label.pack(pady=10)

        self.question_label = ctk.CTkLabel(self.quiz_frame, text="", font=("Arial", 16), wraplength=400)
        self.question_label.pack(pady=20)

        self.answer_entry = ctk.CTkEntry(self.quiz_frame, font=("Arial", 14))
        self.answer_entry.pack(pady=10)

        self.next_button = ctk.CTkButton(self.quiz_frame, text="Next", font=("Arial", 14), command=self.next_question)
        self.next_button.pack(pady=20)

    def display_question(self):
        """Displays the current question."""
        question = self.questions[self.current_question]
        self.question_label.config(text=f"Translate this: {question}")
        self.question_label.pack(pady=10)
        self.answer_entry.delete(0, ctk.END)  # Clear the entry box

    def next_question(self):
        """Validates the translation and proceeds to the next question."""
        player_input = self.answer_entry.get().strip()
        question = self.questions[self.current_question]
        correct_translation = self.translation_data[question][self.selected_language]

        if player_input.lower() == correct_translation.lower():
            self.player_scores[self.current_player] += 1

        # Switch players and move to the next question
        self.current_player = (self.current_player + 1) % 2
        self.current_question += 1

        if self.current_question < len(self.questions):
            # Update player turn and display the next question
            self.player_label.config(
                text=f"Player {self.current_player + 1}'s Turn", text_color="blue" if self.current_player == 0 else "green"
            )
            self.display_question()
        else:
            # End game and show results
            self.show_results()

    def show_results(self):
        """Displays the final results and exits the program."""
        result_message = (
            f"Game Over!\n"
            f"Player 1's Score: {self.player_scores[0]}\n"
            f"Player 2's Score: {self.player_scores[1]}"
        )
        winner = None
        if self.player_scores[0] > self.player_scores[1]:
            winner = "Player 1 Wins!"
        elif self.player_scores[1] > self.player_scores[0]:
            winner = "Player 2 Wins!"
        else:
            winner = "It's a Tie!"

        result_message += f"\n\n{winner}"
        messagebox.showinfo("Results", result_message)
        self.root.destroy()

main = ctk.CTk()
quiz = TranslationQuiz(main)
main.mainloop()