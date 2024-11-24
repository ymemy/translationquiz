import customtkinter as ctk

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
