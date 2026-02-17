from app.domain.policies.BasePolicy import BasePolicy
from app.utils.exceptions.PolicyError import PolicyError
import re

class CategoryPolicy(BasePolicy):
    def validate_insert_category(self, data: dict) -> dict:
        filtered_category_data = self.create_resource(
            data,
            required=["user_id", "type", "name"],
            allowed=["user_id", "type", "name"]
        )

        if filtered_category_data["type"].lower() not in ("income", "expense"):
            raise PolicyError("Type should be income or expense only")
        
        filtered_category_data["name"] = self.validate_string(filtered_category_data["name"], "Category Name", min_len=3)
        
        return filtered_category_data

    def validate_duplicate_category_name_entry(self, category_obj):
        if category_obj:
            raise PolicyError(f"You already have '{category_obj.name}' as a category")
        
    def validate_category_editing(self, data: dict, category: object) -> dict:
        if category is None:
            raise PolicyError("Category not found")

        clean = self.update_resource(
            data, 
            allowed=["name", "user_id", "category_id"]
        )

        self.validate_id_values(clean["category_id"], "Category ID")
        self.validate_id_values(clean["user_id"], "User ID")
        self.validate_string(clean["name"], "Category Name", min_len=3)

        return clean
    
    def validate_category_deletion(self, category, current_user_id: int, category_in_use_checker: object):
        if category_in_use_checker is not None:
            raise PolicyError(f"Cannot delete category in use '{category.name}'")
        if category is None:
            raise PolicyError("No Category instance found")
        if category.user_id != current_user_id:
            raise PolicyError(f"Cannot delete category user don't own '{category.name}'")
        
    def validate_users_category_existence(self, category):
        if category is None:
            raise PolicyError("No category found")
