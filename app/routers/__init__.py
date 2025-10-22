from .auth import router as auth_router
from .admin import router as admin_router
from .uploads import router as upload_router
from .formations import router as formations_router
from .actualites import router as actualites_router
from .directors import router as directors_router
from .about import router as about_router
from .contact_info import router as contact_info_router
from .contact_messages import router as contact_messages_router

__all__ = [
    "auth_router",
    "admin_router", 
    "upload_router",
    "formations_router",
    "actualites_router", 
    "directors_router",
    "about_router",
    "contact_info_router",
    "contact_messages_router"
]