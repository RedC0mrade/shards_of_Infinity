[
  {
    "name": "Ученик подлесья",
    "crystals_cost": 1,
    "description": "Получите 3 здоровья. Единение - получите 5 атаки, если в этот ход сыграли другого Союзника природы.",
    "shield": 0,
    "champion_health": 0,
    "card_type": "Союзник",
    "faction": "Ветвь",
    "icon": "C:/telegram/card_1.jpeg",
    "start_card": "False",
    "effects": [
      {
        "action": "healing",
        "value": 3,
        "effect_type": "base",
        "condition_type": "none",
        "condition_value": 0
      },
      {
        "action": "attack",
        "value": 2,
        "effect_type": "conditional",
        "condition_type": "card_on_table",
        "condition_value": 1
      }
    ]
  },
  {
    "name": "Страж Шардвуда",
    "crystals_cost": 4,
    "description": "Получите 2 атаки и возьмите карту. Единение - получите 6 здоровья если в этот ход сыграли другого Союзника природы.",
    "shield": 0,
    "champion_health": 0,
    "faction": "Ветвь",
    "card_type": "Союзник",
    "icon": "c:/telegram/card_6.jpeg",
    "start_card": "False",
    "effects": [
      {
        "action": "attack",
        "value": 2,
        "effect_type": "base",
        "condition_type": "none",
        "condition_value": 0
      },
      {
        "action": "healing",
        "value": 6,
        "effect_type": "conditional",
        "condition_type": "card_on_table",
        "condition_value": 0
      }
    ]
  },
  {
    "name": "Споровый клерик",
    "crystals_cost": 2,
    "description": "Получите 4 здоровья.",
    "shield": 0,
    "champion_health": 0,
    "faction": "Ветвь",
    "card_type": "Наёмник",
    "icon": "c:/telegram/card_7.jpeg",
    "start_card": "False",
    "effects": [
      {
        "action": "healing",
        "value": 4,
        "effect_type": "base",
        "condition_type": "none",
        "condition_value": 0
      }
    ]
  },
  {
    "name": "Рыцарь 3ль'шай",
    "crystals_cost": 3,
    "description": "Получите 3 атаки. Единение - вместо этого получите 6 атаки, если в этот ход сыграли другого Союзника природы.",
    "shield": 0,
    "champion_health": 0,
    "faction": "Ветвь",
    "card_type": "Наёмник",
    "icon": "c:/telegram/card_10.jpeg",
    "start_card": "False",
    "effects": [
      {
        "action": "attack",
        "value": 3,
        "effect_type": "base",
        "condition_type": "none",
        "condition_value": 0
      },
      {
        "action": "attack",
        "value": 3,
        "effect_type": "conditional",
        "condition_type": "card_on_table",
        "condition_value": 1
      }
    ]
  }
]
