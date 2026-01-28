from app.policies.BasePolicy import BasePolicy
from app.utils.exceptions.PolicyError import PolicyError
import re

class CategoryPolicy(BasePolicy):
    def validate_insert_category(self, data: dict) -> dict:
        """ 
            Validates category insertion and returns filtered fields from received data
            
            Param:
                data: Dictionary
                    * user_id : String
                    * type : Enum("income", "expense") 
                    * name : String  
            Return:
                filtered_category_data: String        
        """
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
        """ 
            Validates category (insertion or editing) when there is a duplicate name record found under user's record
            
            Param:
                * category_obj : Object 
            Exception:
                Will raise PolicyError when record found in database
        """
        if category_obj:
            raise PolicyError(f"You already have '{category_obj.name}' as a category")
        
    def validate_category_editing(self, data: dict, category: object) -> dict:
        """ 
            Validates category edit record and returns filtered fields from received data
            
            Param:
                * name: String
            Return:
                clean: String
        """
        if category is None:
            raise PolicyError("Category not found")

        clean = self.update_resource(
            data,
            allowed=["name"]
        )

        if "name" not in clean:
            raise PolicyError("Name should be present")
        
        clean["name"] = self.validate_string(clean["name"], "Category Name", min_len=3)

        return clean
    
    def validate_category_deletion(self, category, current_user_id: int, category_in_use_checker: object):
        """ 
            Validates category deletion raises PolicyError
            Param:
                * id : Int
            Return:
                None
            Exception:
                Raise PolicyError when target category is used (Income, Expense)
                Raise PolicyError when no category is found
                Raise PolicyError when current user's target category does not belong to user
        """
        if category_in_use_checker is not None:
            raise PolicyError(f"Cannot delete category in use '{category.name}'")
        if category is None:
            raise PolicyError("No Category instance found")
        if category.user_id != current_user_id:
            raise PolicyError(f"Cannot delete category user don't own '{category.name}'")
        
    def validate_users_category_existence(self, category):
        if category is None:
            raise PolicyError("No category found")
    
