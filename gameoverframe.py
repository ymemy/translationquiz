import customtkinter as ctk
from homeframe import HomeFrame

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
