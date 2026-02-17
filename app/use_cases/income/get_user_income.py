from app.model.m_Income import Income as IncomeORM

class GetUserIncomeUseCase:
    def __init__(self, unit_of_work):
        self.uow = unit_of_work

    def execute(self, user_id: int):
        # Step 1: Get all income for user
        income_records = self.uow.incomes.get_all_by_user_id(user_id)
        
        # Step 2: Enrich with category names
        result = []
        for income in income_records:
            category = self.uow.categories.get_by_id(income.category_id)
            # Get ORM object to access created_at (domain entity doesn't track it)
            orm = IncomeORM.query.filter_by(id=income.id).first()
            result.append({
                "id": income.id,
                "name": (orm.name if orm and orm.name else ""),
                "source": income.source,
                "amount": income.amount,
                "category_name": category.name if category else "Unknown",
                "received_date": income.received_date,
                "payment_method": income.payment_method,
                "remarks": income.remarks,
                "created_at": orm.created_at if orm else None
            })
        
        return result