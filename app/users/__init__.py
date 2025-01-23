from flask import Blueprint

bp = Blueprint("user_name", 
               __name__, 
               template_folder="templates/users",
               #url_prefix="/users2"
               )

from . import views