import json
from pathlib import Path
from app.backend.core.models.card import Card, CardAction, CardEffect, CardFaction, CardType, ConditionType, EffectType
from app.backend.factories.database import db_helper



async def import_cards_from_json(json_file_path: str, database_url: str):
    # ... (остальной код такой же)
    
    async with db_helper.session_context() as session:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Заменяем f"{base_dir}" на актуальный путь
        base_dir = Path(__file__).parent
        content = content.replace('f"{base_dir}', str(base_dir))
        
        cards_data = json.loads(content)
        
        try:
            for card_data in cards_data:
                # Создаем объект карты
                card = Card(
                    name=card_data['name'],
                    crystals_cost=card_data['crystals_cost'],
                    description=card_data['description'],
                    shield=card_data['shield'],
                    champion_health=card_data['champion_health'],
                    faction=CardFaction(card_data['faction']),
                    card_type=CardType(card_data['card_type']),
                    icon=card_data['icon'],
                    start_card=card_data['start_card']
                )
                
                session.add(card)
                session.flush()  # Получаем ID карты
                
                # Создаем эффекты карты
                for effect_data in card_data['effects']:
                    effect = CardEffect(
                        card_id=card.id,
                        action=CardAction(effect_data['action']),
                        value=effect_data['value'],
                        effect_type=EffectType(effect_data['effect_type']),
                        condition_type=ConditionType(effect_data['condition_type']) if effect_data['condition_type'] != "none" else None,
                        condition_value=effect_data['condition_value'] if effect_data['condition_value'] != 0 else None
                    )
                    session.add(effect)
                
                print(f"Добавлена карта: {card_data['name']}")
            
            # Коммитим изменения
            session.commit()
            print("Импорт завершен успешно!")
            
        except Exception as e:
            session.rollback()
            print(f"Ошибка при импорте: {e}")
            raise
        finally:
            session.close()

    if __name__ == "__main__":
        # Укажите путь к вашему JSON файлу и URL базы данных
        json_file_path = "path/to/your/cards.json"
        database_url = "sqlite:///your_database.db"  # или "postgresql://user:password@localhost/dbname"
        
        import_cards_from_json(json_file_path, database_url)