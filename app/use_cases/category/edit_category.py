from app.domain.policies.p_CategoryPolicy import CategoryPolicy
from app.utils.exceptions import PolicyError

class EditCategoryUseCase:
    def __init__(self, unit_of_work):
        self.uow = unit_of_work
        self.cat_policy = CategoryPolicy()

    def execute(self, category_data: dict):
        category = self.uow.categories.get_by_id_and_user_id(category_data["category_id"], category_data["user_id"])
        clean_data = self.cat_policy.validate_category_editing(category_data, category)
        duplicate_category = self.uow.categories.get_by_name_and_user_id(clean_data["name"], clean_data["user_id"])
        self.cat_policy.validate_duplicate_category_name_entry(duplicate_category)

        category.rename(clean_data["name"])
        category.update_description(clean_data.get("description"))

        with self.uow.transaction():
            updated_category = self.uow.categories.update(category)

        return updated_category
