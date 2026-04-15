class GetUserSavingGoalsUseCase:
    def __init__(self, unit_of_work):
        self.uow = unit_of_work

    def execute(self, user_id: int):
        return self.uow.saving_goals.get_all_by_user_id(user_id)