from aiogram.fsm.state import State, StatesGroup


class AcceptInvitationStates(StatesGroup):
    waiting_for_invite_code = State()
