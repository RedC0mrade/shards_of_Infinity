[
  {
    "name": "Дрон-убийца",
    "crystals_cost": 1,
    "description": "Получите 2 атаки. Eсли у вас есть Чемпион в игре, получите вместо этого 4 атаки.",
    "shield": 0,
    "champion_health": 0,
    "faction": "homodeus",
    "card_type": "ally",
    "icon": "",
    "effects": [
      {
        "action": "attack",
        "value": 2,
        "effect_type": "base",
        "condition_type": "none",
        "condition_value": 0
      },
      {
        "action": "attack",
        "value": 4,
        "effect_type": "conditional",
        "condition_type": "card_on_table",
        "condition_value": "champion"
      }
    ]
  }
]