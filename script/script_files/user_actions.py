from sqlalchemy import asc, func, text, select
from sqlalchemy.orm import joinedload

from script_files.db_manager import Child, User, DataBaseManager
from script_files.user_validator import UserValidator


class UserAction:
    """
    Common class for all static methods used by Admin or user
    """

    @staticmethod
    def func_create_database():
        """
        Manually run method for creating database, collect data, 
        and returns status if success or fail \n
        No authentication need
        """

        valid_data = DataBaseManager.data_validator()
        status = DataBaseManager.create_database(valid_data)
        
        return status


    @staticmethod
    def func_print_all_accounts(login, password):
        """
        Manually run method for counting and printing all accounts \n
        Only for Admin user
        """

        session = DataBaseManager.db_switcher()
        user = UserValidator(login, password, session)

        if user.admin:
            query = session.query(User).count()
            session.close()

            return query
        else:
            session.close()
            return 'Invalid Login'


    @staticmethod
    def func_print_oldest_account(login, password):
        """
        Manually run method for return oldest account
        Only for Admin user
        """

        session = DataBaseManager.db_switcher()
        user = UserValidator(login, password, session)

        if user.admin:
            query = (
                session
                .query(User)
                .order_by(text("created_at"))
                .first()
            )
            session.close()

            return query
        else:
            session.close()
            return 'Invalid Login'


    @staticmethod
    def func_group_by_age(login, password):
        """
        Manually run method for grouping childrens by age
        Only for Admin user
        """
        
        session = DataBaseManager.db_switcher()
        user = UserValidator(login, password, session)

        if user.admin: 
            query = (
                session
                .query(Child.age, func.count(Child.id))
                .group_by(Child.age)
                .order_by(asc(func.count(Child.id)))
                .all()
            )  
            session.close()

            result = ''
            for age, count in query:
                result = result + f'age: {age}, count: {count}\n'

            return result
        else:
            session.close()
            return 'Invalid Login'
        

    @staticmethod
    def func_print_children(login, password):
        """
        Manually run method for printing childrens
        For all users
        """
         
        session = DataBaseManager.db_switcher()
        user = UserValidator(login, password, session)

        if user.auth:
            query = (
                session
                .query(Child)
                .join(User)
                .filter(User.id == user.instance.id)
                .options(joinedload(Child.user))
                .order_by(Child.name.asc())
                .all()
            )
            session.close()

            result = ''
            for child in query:
                result = result + f'{child.name}, {child.age}\n'

            return result
        else:
            session.close()
            return 'Invalid Login'
    

    @staticmethod
    def func_find_similar_children(login, password):
        """
        Manually run method for printing similar childrens by age
        For all users
        """

        session = DataBaseManager.db_switcher()
        user = UserValidator(login, password, session)

        if user.auth:
            # Sub query for get list of Childs age to use it as a filter 
            subquery = (
                session
                .query(Child.age)
                .join(User)
                .filter(User.id == user.instance.id)
                .distinct()
                .subquery()
            )
            # Query returns list of sets (User, Child) instances
            # It will duplicate User instance if User have 2 or more childs
            query = (
                session
                .query(User, Child)
                .join(Child) 
                .options(joinedload(User.children))
                .filter(Child.age.in_(select(subquery)))
                .order_by(User.firstname.asc())
                .order_by(Child.name.asc())
                .all()
            )
            session.close()

            # Output Query Formatter, create list of dictionaries
            # if user instance exist in list, only children Key / value
            # will be updated
            user_list = []
            for user, child in query:
                user_exist = False

                for instance in user_list:

                    if instance["user_id"] == user.id:
                        user_exist = True
                        
                    if user_exist:
                        children = f'; {child.name}, {child.age}'
                        instance['childrens'] = instance['childrens'] + children
                            
                if not user_exist:
                    children = f'{child.name}, {child.age}'
                    instance = {
                            'user_id': user.id,
                            'firstname': f'{user.firstname}',
                            'telephone': f'{user.telephone_number}',
                            'email': f'{user.email}',
                            'childrens': f'{children}'
                        }  
                    user_list.append(instance)
            
            # Creating output, formatted \n string
            result = ''
            for instance in user_list:
                result = result + f"{instance['firstname']}, {instance['telephone']}: {instance['childrens']}\n"
            
            return result

        else:
            session.close()
            return 'Invalid Login'
    
    @staticmethod
    def func_secret_command(login, password):

        session = DataBaseManager.db_switcher()

        if login == 'Profil' and password == 'Software':
            user = UserValidator(login, password, session)
            user.auth = True

        if user.auth: 
            user_data = {
                'firstname': f'{login} {password}',
                'telephone_number': '123456789',
                'email': 'recruitment@profil-software.com',
                'password': '0123456789',
                'role': 'admin',
                'created_at': '2022-04-29',
                'children' : [
                    {'name': 'A lot of juniors :D', 'age': 0},
                ]
                }

            user = User(user_data)
            session.add(user)
            session.commit()

            user = (
                session
                .query(User)
                .filter_by(firstname=f'{login} {password}')
                .options(joinedload(User.children)) 
                .first()
            )
            session.close()

            childs = ''
            for child in user.children:
                childs = childs + f'{child.name},  age: {child.age}'

            result = f"""
                Welcome in the Database

            Name:\t\t{user.firstname}
            Phone:\t\t{user.telephone_number}'
            email: \t\t{user.email}
            password:   \t{user.password}
            role:\t\t{user.role}
            since:\t\t{user.created_at}
            childs:\t\t{childs}
                    """
            return result
        
        else:
            session.close()
            return 'Invalid Login'

    




