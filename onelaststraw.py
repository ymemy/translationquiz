import customtkinter as ctk
from tkinter import messagebox
import random 

############# Loading data #############

def load_translation_file(file_path):
    """Reads the files and returns the tuples inside a list."""
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
    'Français': 'words/french.txt',
    'Español': 'words/spanish.txt',
    'Deutsch': 'words/german.txt',
    '日本語': 'words/japanese.txt',
    '中文': 'words/mandarin.txt'
}

# Dictionary to store translations for each language
data = {}

# Load data for each language into the master dictionary
for language, file_path in files.items():
    data[language] = load_translation_file(file_path)

############# ctk frames #############

class HomeFrame(ctk.CTkFrame):
    """Home page."""
    def __init__(self, master, on_continue):
        super().__init__(master)
        
        self.on_continue = on_continue

        rules = (
            "Rules:\n"
            "1. This is a two-player game.\n"
            "2. Players will take turns translating prompts.\n"
            "3. Each correct answer earns 1 point.\n"
            "4. The player with the most points at the end wins!\n"
        )

        languages = ["Français", "Español", "Deutsch", "日本語", "中文"]

        self.label_title = ctk.CTkLabel(self, text="Welcome to the Translation Quiz!", font=("Arial", 20))
        self.label_rules = ctk.CTkLabel(self, text=rules, font=("Arial", 14), justify="left")
        self.label_language = ctk.CTkLabel(self, text="Select the source language:", font=("Arial", 14))
        self.dropdown = ctk.CTkComboBox(self, values=languages)
        self.button = ctk.CTkButton(self, text="Continue", command=self.continue_game)

        self.label_title.pack(pady=(10, 20))
        self.label_rules.pack(pady=(10, 20))
        self.label_language.pack(pady=(10, 5))
        self.dropdown.pack(pady=(5, 20))
        self.button.pack(pady=10)

    def continue_game(self):
        selected_language = self.dropdown.get()  # Fetch the selected language
        if self.on_continue:
            self.on_continue(selected_language)

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

class GameOverFrame(ctk.CTkFrame):
    def __init__(self, master, score):
        super().__init__(master)

        self.label1 = ctk.CTkLabel(self, text="Game Over!", font=("Arial", 20))
        self.label2 = ctk.CTkLabel(self, text=f"Score: {score}", font=("Arial", 20))
        self.restart_button = ctk.CTkButton(self, text="Restart", font=("Arial", 14), command=self.restart_game)

        self.label1.pack(pady=20)
        self.label2.pack(pady=20)
        self.restart_button.pack(pady=20)

    def restart_game(self):
        """Restart the game from the home screen."""
        self.master.switch_frame(HomeFrame(self.master, self.master.start_quiz))

############# ctk instance #############

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("System") 
        ctk.set_default_color_theme("blue") 

        self.title("Translation Quiz")
        self.geometry("1200x800")
        self.current_frame = None
        self.selected_language = None

        self.home_frame = HomeFrame(self, self.start_quiz)
        self.switch_frame(self.home_frame)

    def switch_frame(self, frame):
        # Remove the current frame and display the new one
        if self.current_frame:
            self.current_frame.pack_forget()
        self.current_frame = frame
        self.current_frame.pack(fill="both", expand=True, padx=20, pady=20)

    def start_quiz(self, selected_language):
        self.selected_language = selected_language
        self.quiz_frame = QuizFrame(self, data, self.selected_language)
        self.switch_frame(self.quiz_frame)

app = App()
app.mainloop()