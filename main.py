import sys
from pathlib import Path
import customtkinter as ctk

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from ui.app_window import TractorCalculatorApp

if __name__ == "__main__":
    print("Starting application...")
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("green")

    app = TractorCalculatorApp()
    app.mainloop()