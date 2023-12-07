import os
from script_files.data_collector import DataCollector 
from script_files.data_validator import DataValidator 
from script_files.db_manager import create_database
from script_files.db_manager import User
from script_files.db_manager import Child
from script_files.db_manager import session
from script_files.user_validator import UserValidator


def func_create_database():
    data_path = 'data'

    root_path = os.path.dirname(os.path.abspath(__file__))
    lvl1_path = os.path.dirname(root_path)
    lvl2_path = os.path.dirname(lvl1_path)
    path = os.path.join(lvl2_path, data_path)
   

    collector = DataCollector(path)
    data = collector.collected
    valid = DataValidator(data)
    valid_data = valid.collected
    status = create_database(valid_data)
    
    return status


def func_print_all_accounts(login, password):
    user = UserValidator(login, password)

    if bool(user.admin and user.auth):
        query = session.query(User).count()
        session.close()

        return query
    else:
        return 'Invalid Login'




