class DeleteDebtUseCase:
    def __init__(self, unit_of_work):
        self.uow = unit_of_work

    def execute(self, debt_id: int, user_id: int):
        debt = self.uow.debts.get_by_id_and_user_id(debt_id, user_id)
        if debt is None:
            raise Exception("Debt not found")

        with self.uow.transaction():
            deleted = self.uow.debts.delete(debt.id)

        if not deleted:
            raise Exception("Failed to delete debt")

        return True