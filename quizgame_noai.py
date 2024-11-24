import customtkinter as ctk
from tkinter import messagebox
import translation

# Function to read a file and return a list of tuples
def load_translation_file(file_path):
    translations = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Assuming the file format is like (key, value)
            line = line.strip().strip('()')
            pair = tuple(line.split(', '))
            translations.append(pair)
    return translations

# File paths for each language dataset
files = {
    'french': 'words/french.txt',
    'spanish': 'words/spanish.txt',
    'german': 'words/german.txt',
    'japanese': 'words/japanese.txt',
    'mandarin': 'words/mandarin.txt'
}

# Master dictionary to store translations for each language
master_data = {}

# Load data for each language into the master dictionary
for language, file_path in files.items():
    master_data[language] = load_translation_file(file_path)

class TranslationQuiz:
    def __init__(self, root):
        #appearance
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        #box
        self.root = root
        self.root.title("Who's the best translator?")
        self.root.geometry("600x400")
        
        # self.translation_data = {
        #     "What is your name?": {"Français": "Comment vous appelez-vous?", "Español": "¿Cómo te llamas?"},
        #     "Good morning": {"Français": "Bonjour", "Español": "Buenos días"},
        #     "Thank you": {"French": "Merci", "Español": "Gracias"}
        # }
        
        # self.questions = list(self.translation_data.keys())
        
        self.selected_language = None

        self.current_question = 0
        self.player_scores = [0, 0]  # Scores for Player 1 and Player 2
        self.current_player = 0 # 0 for Player 1, 1 for Player 2
        self.correct_answer = None

        # Frames pages
        self.home_frame = ctk.CTkFrame(root)
        self.quiz_frame = ctk.CTkFrame(root)
        self.gameover_frame = ctk.CTkFrame(root)

        self.create_home_screen()
        self.create_quiz_screen()
        self.create_gameover_screen()
        
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

        start_button = ctk.CTkButton(self.home_frame, text="Start Quiz", font=("Arial", 16), command=self.start_quiz)
        start_button.pack(pady=20)
    
    def start_quiz(self):
        """Starts the quiz with the selected language."""
        self.selected_language = self.language_var.get()
        self.current_question = 0
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
        # question = self.questions[self.current_question]

        if self.selected_language == "Français":
            question, self.correct_answer = translation.generate_sentences('french')
        elif self.selected_language == "Español":
            question, self.correct_answer = translation.generate_sentences('spanish')
        elif self.selected_language == "Deutsch":
            question, self.correct_answer = translation.generate_sentences('german')
        elif self.selected_language == "日本語":
            question, self.correct_answer = translation.generate_sentences('japanese')
        elif self.selected_language == "中文":
            question, self.correct_answer = translation.generate_sentences('mandarin')

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

        if self.current_question < 5:  # Set the number of questions you want
            # Update player turn label and display the next question
            self.player_label.config(
                text=f"Player {self.current_player + 1}'s Turn", text_color="blue" if self.current_player == 0 else "green"
            )
            self.display_question()
        else:
            # End game and show results
            self.show_results()

    def create_gameover_screen(self):
        """Creates the game over screen."""
        self.player_label = ctk.CTkLabel(self.quiz_frame, text="Game Over", font=("Arial", 16), text_color="white")
        self.player_label.pack(pady=10)

        self.next_button = ctk.CTkButton(self.quiz_frame, text="Next", font=("Arial", 14), command=self.next_question)
        self.next_button.pack(pady=20)

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