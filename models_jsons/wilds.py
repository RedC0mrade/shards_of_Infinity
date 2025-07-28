{
  "name": "Ученик подлесья",
  "crystals_cost": 1,
  "description": "Получите 3 здоровья. Единение - получите 5 атаки, если в этот ход сыграли другого Союзника природы.",
  "shield": 0,
  "champion_health": 0,
  "card_type": "Союзник",
  "faction": "Ветвь",
  "icon": "C:/telegram/card_1.jpeg",
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
      "value": 5,
      "effect_type": "conditional",
      "condition_type": "card_on_table",
      "condition_value": 0
    }
  ]
}


{
  "name": "Страж Шардвуда",
  "crystals_cost": 4,
  "description": "Получите 2 атаки и возьмите карту. Единение - получите 6 здоровья если в этот ход сыграли другого Союзника природы.",
  "shield": 0,
  "champion_health": 0,
  "faction": "Ветвь",
  "card_type": "Союзник",
  "icon": "c:/telegram/card_6.jpeg",
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
}


{
  "name": "Споровый клерик",
  "crystals_cost": 2,
  "description": "Получите 2 здоровья.",
  "shield": 0,
  "champion_health": 0,
  "faction": "Ветвь",
  "card_type": "Наёмник",
  "icon": "c:/telegram/card_7.jpeg",
  "effects": [
    {
      "action": "healing",
      "value": 4,
      "effect_type": "base",
      "condition_type": "none",
      "condition_value": 0
    }
  ]
}

{
  "name": "Рыцарь 3ль'шай",
  "crystals_cost": 3,
  "description": "Получите 3 атаки. Единение - вместо этого получите 6 атаки, если в этот ход сыграли другого Союзника природы.",
  "shield": 0,
  "champion_health": 0,
  "faction": "Ветвь",
  "card_type": "Наёмник",
  "icon": "c:/telegram/card_10.jpeg",
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
      "condition_value": 0
    }
  ]
}

{
  "name": "Осколочный реактор",
  "crystals_cost": 0,
  "description": "Получите 2 кристалла. Если у вас 10 могущества получите 3 кристалла. Если у вас 15 могущества получите 4 кристалла.",
  "shield": 0,
  "champion_health": 0,
  "card_type": "Реликвия",
  "faction": "Нейтральная",
  "icon": "c:/telegram/card_95.jpeg",
  "effects": [
    {
      "action": "crystal",
      "value": 2,
      "effect_type": "base",
      "condition_type": "none",
      "condition_value": 0
    },
    {
      "action": "crystal",
      "value": 3,
      "effect_type": "conditional",
      "condition_type": "mastery",
      "condition_value": 10
    },
    {
      "action": "crystal",
      "value": 4,
      "effect_type": "conditional",
      "condition_type": "mastery",
      "condition_value": 15
    }
  ]
}

{
  "name": "Кристалл",
  "crystals_cost": 0,
  "description": "Получите 1 кристалл",
  "shield": 0,
  "champion_health": 0,
  "card_type": "Реликвия",
  "faction": "Нейтральная",
  "icon": "c:/telegram/card_100.jpeg",
  "effects": [
    {
      "action": "crystal",
      "value": 1,
      "effect_type": "base",
      "condition_type": "none",
      "condition_value": 0
    }
  ]
}

{
  "name": "Бластер",
  "crystals_cost": 0,
  "description": "Получите 1 атаки",
  "shield": 0,
  "champion_health": 0,
  "card_type": "Реликвия",
  "faction": "Нейтральная",
  "icon": "c:/telegram/card_107.jpeg",
  "effects": [
    {
      "action": "attack",
      "value": 1,
      "effect_type": "base",
      "condition_type": "none",
      "condition_value": 0
    }
  ]
}


{
  "name": "Кристалл",
  "crystals_cost": 0,
  "description": "Получите 2 атаки. Если у вас 10 могущества, получите 3 атаки. Если у вас 20 могущества, получите 5 атаки. Если у вас 30 могущества, получите ∞ атаки",
  "shield": 0,
  "champion_health": 0,
  "card_type": "Реликвия",
  "faction": "Нейтральная",
  "icon": "c:/telegram/card_108.jpeg",
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
      "value": 3,
      "effect_type": "conditional",
      "condition_type": "mastery",
      "condition_value": 10
    },
    {
      "action": "attack",
      "value": 5,
      "effect_type": "conditional",
      "condition_type": "mastery",
      "condition_value": 20
    },
    {
      "action": "attack",
      "value": 1000,
      "effect_type": "conditional",
      "condition_type": "mastery",
      "condition_value": 30
    }
  ]
}