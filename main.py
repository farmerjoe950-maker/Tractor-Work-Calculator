import json
import os
from pathlib import Path
from ui.app_window import TractorCalculatorApp

def load_json(filename: str) -> dict:
    path = Path(filename)
    if not path.exists():
        return{}
    with open(path, "r") as f:
        return json.load(f)

if __name__ == "__main__":
    tractors = load_json("tractor_profiles.json")
    implements = load_json("implement_profiles.json")

app = TractorCalculatorApp(tractors, implements)
app.mainloop()