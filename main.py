import json
import os
from pathlib import Path
from ui.app_window import TractorCalculatorApp

BASE_DIR = Path(__file__).parent

def load_json(filename: str) -> dict:
    path = BASE_DIR / "data" / filename
    if not path.exists():
        print(f" ERROR: File not found at {path}")
        return{}
    with open(path, "r") as f:
        return json.load(f)

if __name__ == "__main__":
    tractors = load_json("tractor_profiles.json")
    implements = load_json("implement_profiles.json")

app = TractorCalculatorApp(tractors, implements)
app.mainloop()