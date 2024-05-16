from .menu import main_menu
from .db.db_manager import DBManager

db_manager_obj = DBManager('RealDictCursor')
main_menu(db_manager_obj)

