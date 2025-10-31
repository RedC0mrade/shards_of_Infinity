import asyncio
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.backend.core.models.engine import DatabaseHelper
from app.backend.core.models.card import Card, CardEffect
from config import settings
from models_jsons.start_deck import start_data
from models_jsons.wilds import wilds_data
from models_jsons.demirealm import demirealm_cards
from models_jsons.homodeus import homodeus_cards
from models_jsons.order import order_cards


async def seed_all_cards():
    """Заполняет базу данных всеми картами (стартовые и дикой природы)"""
    # Инициализируем DatabaseHelper с настройками из config
    db_helper = DatabaseHelper(
        url=str(settings.db.url),
        echo=settings.db.echo,
        echo_pool=settings.db.echo_pool,
        pool_size=settings.db.pool_size,
        max_overflow=settings.db.max_overflow,
    )

    try:
        async with db_helper.session_context() as session:
            from sqlalchemy import select

            print("Проверяем существующие карты в базе...")

            # Проверяем, есть ли уже карты в базе
            result = await session.execute(select(Card))
            existing_cards = result.scalars().all()

            if existing_cards:
                print(
                    f"✅ В базе уже есть {len(existing_cards)} карт. Пропускаем заполнение."
                )
                return

            print("Начинаем заполнение базы данных картами...")

            # Объединяем все данные карт
            all_cards_data = (
                start_data
                + wilds_data
                + homodeus_cards
                + demirealm_cards
                + order_cards
            )
            total_cards = len(all_cards_data)

            print(f"Всего карт для добавления: {total_cards}")
            print(f"  - Стартовые карты: {len(start_data)}")
            print(f"  - Карты дикой природы: {len(wilds_data)}")

            # Создаем все карты
            created_count = 0
            for i, card_data in enumerate(all_cards_data, 1):
                try:
                    # Создаем эффекты для карты
                    effects = []
                    for effect_data in card_data["effects"]:
                        effect = CardEffect(
                            action=effect_data["action"],
                            value=effect_data["value"],
                            effect_type=effect_data["effect_type"],
                            condition_type=effect_data["condition_type"],
                            condition_value=effect_data["condition_value"],
                        )
                        effects.append(effect)

                    # Для карт дикой природы добавляем поле start_card если его нет
                    start_card_value = card_data.get("start_card", "other")

                    # Создаем карту
                    card = Card(
                        name=card_data["name"],
                        crystals_cost=card_data["crystals_cost"],
                        description=card_data["description"],
                        shield=card_data["shield"],
                        champion_health=card_data["champion_health"],
                        card_type=card_data["card_type"],
                        faction=card_data["faction"],
                        icon=card_data["icon"],
                        start_card=start_card_value,
                        effects=effects,
                    )

                    session.add(card)
                    created_count += 1

                    # Выводим информацию о добавленной карте
                    faction = card_data["faction"]
                    card_type = card_data["card_type"]
                    print(
                        f"  [{i}/{total_cards}] Добавлена: {card_data['name']} ({faction} - {card_type})"
                    )

                except Exception as e:
                    print(
                        f"  ❌ Ошибка при создании карты {card_data['name']}: {e}"
                    )
                    continue

            # Сохраняем изменения
            await session.commit()
            print(f"\n✅ Успешно создано {created_count} карт в базе данных!")
            print(f"   - Стартовые карты: {len([c for c in start_data])}")
            print(f"   - Карты дикой природы: {len([c for c in wilds_data])}")

    except Exception as e:
        print(f"❌ Ошибка при заполнении базы данных: {e}")
        raise
    finally:
        await db_helper.dispose()


async def check_existing_cards():
    """Проверяет существующие карты в базе"""
    db_helper = DatabaseHelper(
        url=str(settings.db.url),
        echo=settings.db.echo,
        echo_pool=settings.db.echo_pool,
        pool_size=settings.db.pool_size,
        max_overflow=settings.db.max_overflow,
    )

    try:
        async with db_helper.session_context() as session:
            from sqlalchemy import select, func

            # Получаем общее количество карт
            result = await session.execute(select(func.count(Card.id)))
            total_cards = result.scalar()

            # Получаем количество карт по фракциям
            result = await session.execute(
                select(Card.faction, func.count(Card.id)).group_by(Card.faction)
            )
            factions_count = result.all()

            # Получаем количество карт по типам
            result = await session.execute(
                select(Card.card_type, func.count(Card.id)).group_by(
                    Card.card_type
                )
            )
            types_count = result.all()

            print(f"\n📊 Статистика базы данных:")
            print(f"   Всего карт: {total_cards}")
            print(f"   По фракциям:")
            for faction, count in factions_count:
                print(f"     - {faction}: {count}")
            print(f"   По типам:")
            for card_type, count in types_count:
                print(f"     - {card_type}: {count}")

    except Exception as e:
        print(f"❌ Ошибка при проверке базы данных: {e}")
    finally:
        await db_helper.dispose()


if __name__ == "__main__":
    print("🚀 Запуск заполнения базы данных всеми картами...")
    asyncio.run(seed_all_cards())
    asyncio.run(check_existing_cards())
