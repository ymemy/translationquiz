import customtkinter as ctk
from gameoverframe import GameOverFrame
from homeframe import HomeFrame
from quizframe import QuizFrame

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
