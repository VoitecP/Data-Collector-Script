import re
from script_files.db_manager import User
from script_files.db_manager import Child
from script_files.db_manager import session
from sqlalchemy import select
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound


class LoginFormat:

    def __init__(self, login, password):
        self.login = ''
        self.login = login   
        self.password = ''
        self.password = password
  
        is_phone = self.phone_format()
        self.is_phone = is_phone
        is_email = self.email_format()
        self.is_email = is_email
        is_pass = self.password_format()
        self.is_pass = is_pass


    def phone_format(self):

        phone = self.login 
        pattern = re.compile(r'^\d{9}$')
        if bool(pattern.match(phone)):
            return True
        else:
            return False


    def email_format(self):

        if self.is_phone == True:
            return False

        email = self.login
        pattern_1 = re.compile(r'^[^@]*@[^@]*$')
        pattern_2 = re.compile(r'^.+@.+?\.')
        pattern_3 = re.compile(r'\.[a-zA-Z0-9]{1,4}$')

        patterns=[
            (bool(pattern_1.match(email))),
            (bool(pattern_2.match(email))),
            (bool(pattern_3.search(email))),
        ]

        if all(patterns):
            return True
        else:
            return False


    def password_format(self):
        password = self.password
        pattern = re.compile(r'^\S{10}$')
        
        if bool(pattern.match(password)):
            return True
        else:
            return False
    
	
class UserValidator:

    def __init__(self, login, password):
        self.login = ''
        self.login = login   
        self.password = ''
        self.password = password
        self.instance = None
        self.admin = False
        self.auth = False
       
        auth = self.authenticate()
        self.auth = auth
        admin = self.is_admin()
        self.admin = admin
        

    def authenticate(self):
        login = self.login
        password = self.password

        format = LoginFormat(login, password)

        if format.is_pass == True: 
            if format.is_email == True :
                try:
                    query = select(User).where(User.email == login)
                    user = session.scalars(query).one()
                    session.close()
                    if user.password == password:
                        self.instance = user
                        return True
                    else:
                        return False
                    
                except NoResultFound:
                    return False
                
                except MultipleResultsFound:
                    return False

            elif format.is_phone == True:
                try:
                    query = select(User).where(User.telephone_number == login)
                    user = session.scalars(query).one()
                    session.close()
                    if user.password == password:
                        self.instance = user
                        return True
                    else:
                        return False
                    
                except NoResultFound:
                    return False
                
                except MultipleResultsFound:
                    return False
                
            else:
                return False   
            
        else:
            return False


    def is_admin(self):
        user = self.instance
        if self.auth == True:
            if user.role == 'admin':
                return True
            
            else:
                return False
        else:
            return False
