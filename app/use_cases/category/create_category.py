from app.domain.policies.p_CategoryPolicy import CategoryPolicy

class CreateCategoryUseCase:
    def __init__(self, unit_of_work):
        self.uow = unit_of_work
        self.cat_policy = CategoryPolicy()

    def execute(self, category_data: dict):
        clean_category = self.cat_policy.validate_insert_category(category_data)
        
        category = self.uow.categories.create(**clean_category)

        with self.uow.transaction():
            saved = self.uow.categories.save(category)

        return saved