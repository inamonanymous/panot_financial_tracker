class GetUserCategoriesUseCase:
    def __init__(self, unit_of_work):
        self.uow = unit_of_work

    def execute(self, user_id: int, category_type: str = None):
        """
        Fetch all categories for a user.
        
        Args:
            user_id: The user's ID
            category_type: Optional filter - "income", "expense", "debt", etc.
        
        Returns:
            List of dicts with id and name for each category
        """
        categories = self.uow.categories.get_all_by_user_id(user_id)
        
        # Filter by type if provided
        if category_type:
            categories = [c for c in categories if c.type == category_type]
        
        result = []
        for category in categories:
            result.append({
                "id": category.id,
                "name": category.name,
                "category_type": category.type
            })
        
        return result
