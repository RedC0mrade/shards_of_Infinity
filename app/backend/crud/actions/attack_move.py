from app.backend.core.models.player_state import PlayerState
from app.backend.crud.base_service import BaseService
from app.backend.crud.card_instance_crud import CardInstanceServices
from app.utils.exceptions.exceptions import ShieldError


class AttackService(BaseService):

    async def attack(
        self,
        player_state: PlayerState,
        enemy_state: PlayerState,
    ):
        card_instance_service = CardInstanceServices(session=self.session)
        if enemy_state.invulnerability:
            self.logger.info(
                "Неуязвимость у игрока с id %s, начинаем проверку zetta_check",
                enemy_state.player_id,
            )
            card_instance_service.zetta_check(player_state=enemy_state)

        self.logger.info(
            "Здоровье противника - %s, щит противника - %s, атака игрока - %s",
            enemy_state.health,
            enemy_state.shield,
            player_state.power,
        )
        player_state.power -= enemy_state.shield
        self.logger.info("Атака игрока после снятия щитов ровна", player_state.power)

        if player_state.power <= 0:
            self.logger("Атака меньше или равна щиту выводим ошибку")
            raise ShieldError(message="Щит игрока больше или равен наносимому урону")
        
        enemy_state.health -= player_state.power

        self.logger.info(
            "Осташиеся здоровье - %s",
            enemy_state.health
        )
        # if enemy_state.health < 0:
        # self.logger.info("Здоровье меньше нуля, запускаем функцию 'поражение'")
        # await defeat_service.defeat(
        #     game_id=player_state.game_id,
        #     loser=enemy_state.player_id,
        # )
        player_state.power = 0
        await self.session.commit()
