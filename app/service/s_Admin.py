from app.model.m_Admin import Admin

class AdminService:
    def get_admin_by_user_id(self, user_id: id) -> object:
        return Admin.query.filter_by(user_id=user_id).first()