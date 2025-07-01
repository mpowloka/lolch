from typing import Literal

PlayerRole = Literal["TOP", "JUNGLE", "MID", "BOTTOM", "SUPPORT"]
TeamSide = Literal["ALLY", "ENEMY"]
Comparison = Literal["Weaker", "Even", "Stronger"]
Strength = Literal["Very Weak", "Weak", "Moderate", "Strong", "Very Strong"]

LaningDimension = Literal[
    "Sustain",
    "Waveclear",
    "All-in Threat",
    "Mana Demands",
    "Preferred Trading Pattern",
    "Roaming",
    "Scaling",
    "Teamfighting",
    "Preferred Macro Pattern"
]

JungleDimension = Literal[
    "Clear Speed",
    "Early Gank Threat",
    "Scaling",
    "Teamfighting",
    "Preferred Macro Pattern",
    "1v1 Threat",
    "2v2 Threat"
]