import re
from typing import Tuple, Dict, List
from core.models.literals import Comparison, Strength

COMPARISON_VALUES: List[Comparison] = ["Weaker", "Even", "Stronger"]
STRENGTH_VALUES: List[Strength] = ["Very Weak", "Weak", "Moderate", "Strong", "Very Strong"]

def parse_comparison_output(text: str) -> Tuple[Comparison, str]:
    for key in COMPARISON_VALUES:
        if key.lower() in text.lower():
            return key, text.strip()
    raise ValueError(f"Could not parse Comparison from text: {text}")

def parse_strength_output(text: str) -> Tuple[Strength, Strength, str]:
    ally, enemy = None, None
    for val in STRENGTH_VALUES:
        match = re.search(rf"ally[:\s]+{val}", text, re.IGNORECASE)
        if match:
            ally = val
        match = re.search(rf"enemy[:\s]+{val}", text, re.IGNORECASE)
        if match:
            enemy = val
    if not ally or not enemy:
        found = [val for val in STRENGTH_VALUES if val.lower() in text.lower()]
        if len(found) >= 2:
            ally, enemy = found[0], found[1]
    if ally and enemy:
        return ally, enemy, text.strip()
    raise ValueError(f"Could not parse Strengths from text: {text}")

def parse_threat_output(text: str) -> Dict[str, str]:
    threats = {}
    for line in text.strip().split("\n"):
        if ":" in line:
            name, desc = line.split(":", 1)
            threats[name.strip()] = desc.strip()
    return threats

def parse_cooldown_tip(text: str) -> str:
    return text.strip()
