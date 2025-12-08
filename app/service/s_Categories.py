from app.model.m_Categories import Categories, db
from sqlalchemy.exc import SQLAlchemyError
from app.utils.exceptions import ServiceError
from app.service.BaseService import BaseService


class CategoriesService(BaseService):

    # -----------------------------------------------------
    # CREATE CATEGORY
    # -----------------------------------------------------
    def insert_category(self, data: dict) -> object:
        """
        Creates a new category with validated and cleaned data.
        """

        clean = self.create_resource(
            data,
            required=["user_id", "type", "name"],
            allowed=["user_id", "type", "name"]
        )

        new_category = Categories(**clean)

        return self.safe_execute(lambda: self._save(new_category),
                                 error_message="Failed to create category")

    # -----------------------------------------------------
    # GET CATEGORY
    # -----------------------------------------------------
    def get_category_by_id(self, category_id: int) -> object:
        category = Categories.query.filter_by(id=category_id).first()

        if not category:
            raise ServiceError(f"Category-{category_id} not found")

        return category

    def get_all_categories_by_user(self, user_id: int) -> list:
        return Categories.query.filter_by(user_id=user_id).all()

    # -----------------------------------------------------
    # UPDATE CATEGORY
    # -----------------------------------------------------
    def edit_category(self, category_id: int, data: dict) -> object:

        category = self.get_category_by_id(category_id)

        clean = self.create_resource(
            data,
            required=["name"],     # only name is required for editing
            allowed=["name"]       # only allow editing name
        )

        category.name = clean["name"]

        return self.safe_execute(lambda: self._save(category),
                                 error_message="Failed to update category")

    # -----------------------------------------------------
    # DELETE CATEGORY
    # -----------------------------------------------------
    def delete_category(self, category_id: int) -> bool:

        category = self.get_category_by_id(category_id)

        return self.safe_execute(
            lambda: self._delete(category),
            error_message="Failed to delete category"
        )

    # -----------------------------------------------------
    # PRIVATE DB HELPERS
    # -----------------------------------------------------
