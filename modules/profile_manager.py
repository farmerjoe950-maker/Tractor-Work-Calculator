import json
import os

TRACTOR_PROFILE = "tractor_profiles.json"
IMPLEMENT_PROFILE = "implement_profiles.json"

DEFAULT_TRACTORS = {
    "John Deere 5075E": {
        "specs": {
            "HP": 75,
            "fuel_burn_hour": 2.8,
            "wear_cost": 75
        }
    },
    "Mahindra 4540": {
        "specs": {
            "HP": 41,
            "fuel_burn_hour": 2.8,
            "wear_cost": 41
        }
    },
    "Kubota L2501": {
        "specs": {
            "HP": 25,
            "fuel_burn_hour": 1.2,
            "wear_cost": 1.5
        }
    }
}

DEFAULT_IMPLEMENTS = {
    "6ft Brush Cutter": {
        "specs": {
            "category": "Mowing",
            "width": 6,
            "pto_speed": 540,
            "min_hp": 30,
            "max_hp": 90
        }
    },
    "5ft Box Blade": {
        "specs": {
            "category": "Grading",
            "width": 5,
            "min_hp": 25
        }
    }
}

# Tractor Functions

def load_tractors() -> dict:
    if not os.path.exists(TRACTOR_PROFILE):
        save_tractors(DEFAULT_TRACTORS)
        return DEFAULT_TRACTORS
    try:
        with open(TRACTOR_PROFILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Warning: Could not read profile file. Re-creating defaults.")
        save_tractors(DEFAULT_TRACTORS)
        return DEFAULT_TRACTORS

def save_tractors(tractors:dict) -> None:
    with open(TRACTOR_PROFILE, "w") as f:
        json.dump(tractors, f, indent = 4)

def add_tractor_profile(
        name: str,
        HP: float,
        fuel_burn_hour: float,
        wear_cost: float
)   ->  dict:
    tractors = load_tractors()

    tractors[name] = {
        "HP": float(HP),
        "fuel_burn_hour": float(fuel_burn_hour),
        "wear_cost": float(wear_cost)
    }

    save_tractors(tractors)
    return tractors

def delete_tractor_profile(name: str) -> dict:
    tractors = load_tractors()
    if name in tractors:
        del tractors[name]
        save_tractors(tractors)
    return tractors

# Implement Function

def load_implements() -> dict:
    if not os.path.exists(IMPLEMENT_PROFILE):
        save_implements(DEFAULT_IMPLEMENTS)
        return DEFAULT_IMPLEMENTS
    try:
        with open(IMPLEMENT_PROFILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError: 
        print("Warning: Could not read profile file. Re-creating defaults.")
        save_implements(DEFAULT_IMPLEMENTS)
        return DEFAULT_IMPLEMENTS

def save_implements(implements:dict) -> None:
    with open(IMPLEMENT_PROFILE, "w") as f:
        json.dump(implements, f, indent= 4)

def add_implement_profile(
        name: str,
        category: str,
        width: float,
        pto_speed: float,
        min_hp: float,
        max_hp: float
    ) -> dict:
    implements = load_implements()
    implements[name] = {
        "Category": str(category),
        "Width": float(width),
        "PTO Speed": float(pto_speed),
        "MIN HP": float(min_hp),
        "MAX HP": float(max_hp)
    }
    save_implements(implements)
    return implements

def delete_implements_profiles(name: str) -> dict:
    implements = load_implements()
    if name in implements:
        del implements[name]
        save_implements(implements)
    return implements