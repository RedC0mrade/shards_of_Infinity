# # alembic init -t async alembic
# # alembic downgrade -1
# # alembic upgrade head
# # alembic revision --autogenerate -m "Create tables"


# # docker-compose up --build -d

# # python scripts/seed_cards.py


# # INSERT INTO tags (tag_name, tag_color)
# # VALUES
# # ('black', '#000000'),
# # ('grey', '#999999'),
# # ('yellow', '#fff000');

# # CREATE TYPE userroleenum AS ENUM ('admin', 'user', 'super_user');

# # UPDATE users
# # SET user_role = 'super_user'
# # WHERE id = 1;

# # UPDATE games 
# # SET status = 'FINISHED'::gamestatus
# # WHERE id = 1;

# # UPDATE player_card_instances
# # SET player_state_id = 2, zone = 'hand'
# # WHERE id = 22;

# # ruff check .  # проверка кода
# # ruff format .  # форматирование (как black)
# # ruff --fix .  # автоматическое исправление ошибок


# # python /d/Dev/telegramm/shards_of_Infinity/main.py http://127.0.0.1:8000/docs
# # uvicorn main:app --reload


# async def _handle_effect_result(
#     callback: CallbackQuery,
#     result: EffectResult,
# ):
#     media = []

#     for instance in result.instances:
#         icon_path = media_dir / Path(instance.card.icon)
#         media.append(InputMediaPhoto(media=FSInputFile(icon_path)))

#     if len(media) == 1:
#         await callback.bot.send_photo(
#             chat_id=callback.message.chat.id,
#             photo=media[0].media,
#         )
#     else:
#         await callback.bot.send_media_group(
#             chat_id=callback.message.chat.id,
#             media=media,
#         )

#     keyboard_factory = KEYBOARD_BY_ACTION.get(result.action)

#     if not keyboard_factory:
#         logger.warning("Нет клавиатуры для %s", result.action)
#         return

#     await callback.message.answer(
#         text="Выберите карту:",
#         reply_markup=keyboard_factory(result.instances),
#     )


# @router.callback_query(CardCallback.filter())
# async def handle_play_card(
#     callback: CallbackQuery,
#     callback_data: CardCallback,
# ):
#     logger.info("Обрабатываем команду розыгрыша карт")

#     async with db_helper.session_context() as session:
#         card_services = CardServices(session=session)
#         player_state_services = PlayerStateServices(session=session)
#         move_services = MoveServices(session=session)

#         player_state = await player_state_services.get_player_state_with_game(
#             player_id=callback.from_user.id,
#             active_player=True,
#         )

#         card = await card_services.get_hand_card(
#             player_state_id=player_state.id,
#             card_id=callback_data.id,
#             card_zone=CardZone.HAND,
#             game_id=player_state.game_id,
#         )

#         if not card:
#             return await callback.answer("Карты больше нет в руке")

#         result = await move_services.make_move(
#             card=card,
#             player_state=player_state,
#             game=player_state.game,
#             player_id=callback.from_user.id,
#         )

#         # ----------- ВАЖНОЕ МЕСТО -----------
#         if result:
#             await _handle_effect_result(
#                 callback=callback,
#                 result=result,
#             )
#             return

#         # обычный розыгрыш без доп. эффектов
#         photo = FSInputFile(media_dir / Path(card.icon))

#         await callback.message.answer_photo(
#             photo=photo,
#             caption=f"Вы сыграли карту {card.name}",
#         )


