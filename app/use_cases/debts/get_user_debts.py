class GetUserDebtsUseCase:
    def __init__(self, unit_of_work):
        self.uow = unit_of_work

    def execute(self, user_id: int):
        debts = self.uow.debts.get_all_by_user_id(user_id)
        for i in debts:
            print(i.__dict__)
        return debts
    
    