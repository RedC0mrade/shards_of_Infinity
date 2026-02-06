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
