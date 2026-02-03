from werkzeug.security import check_password_hash, generate_password_hash
from app.ext import db

# Repository-backed Unit of Work (pre-wired)
from app.persistence import create_unit_of_work

# Create a default unit of work instance (can be injected into use-cases)
UOW = create_unit_of_work()

__all__ = [
	"check_password_hash",
	"generate_password_hash",
	"UOW",
]