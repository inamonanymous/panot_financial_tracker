from app.domain.policies.p_CategoryPolicy import CategoryPolicy

class CreateCategoryUseCase:
    def __init__(self, unit_of_work):
        self.uow = unit_of_work
        self.cat_policy = CategoryPolicy()

    def execute(self, category_data: dict):
        clean_category = self.cat_policy.validate_insert_category(category_data)
        category = self.uow.categories.create(**clean_category)
        duplicate_category = self.uow.categories.get_by_name_and_user_id(clean_category["name"], clean_category["user_id"])
        self.cat_policy.validate_duplicate_category_name_entry(duplicate_category)
        with self.uow.transaction():
            saved = self.uow.categories.save(category)
        return saved