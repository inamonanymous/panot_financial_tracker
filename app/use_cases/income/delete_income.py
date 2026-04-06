class DeleteIncomeUseCase:
    def __init__(self, unit_of_work):
        self.uow = unit_of_work

    def execute(self, income_id: int, user_id: int):
        income = self.uow.incomes.get_by_id_and_user_id(income_id, user_id)
        if income is None:
            raise Exception("Income not found")

        with self.uow.transaction():
            deleted = self.uow.incomes.delete(income.id)

        if not deleted:
            raise Exception("Failed to delete income")

        return True