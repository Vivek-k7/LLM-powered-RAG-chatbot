from app.core.models.users import User
from app.core.database import Base, engine
from app.core.models import users  # IMPORTANT: forces model import

Base.metadata.create_all(bind=engine)