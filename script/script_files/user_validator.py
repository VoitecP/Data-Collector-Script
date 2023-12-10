import re

from sqlalchemy import select
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound

from script_files.db_manager import User



class LoginFormat:
    """
    Class for checking if login format and password format is correct, 
    before this auth data will be compared with login/pass data in database
    """

    def __init__(self, login, password):
        self.login = login   
        self.password = password
        self.is_phone = self.phone_format()
        self.is_email = self.email_format()
        self.is_pass = self.password_format()
    

    def phone_format(self):
        """
        Function check if phone is nine digit format
        """
        phone = self.login 
        pattern = re.compile(r'^\d{9}$')
        if bool(pattern.match(phone)):
            return True
        else:
            return False


    def email_format(self):
        """
        If initial login is not in phone format,
        Function check if email is in correct format
        """

        if self.is_phone == True:
            return False
        else:
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
        """
        Password's in database are in 10 character format, without whitespace,
        function will check if pass i matching to that format,
        Allow only 10 charactes, no white spaces
        """
        password = self.password
        pattern = re.compile(r'^\S{10}$')
        
        if bool(pattern.match(password)):
            return True
        else:
            return False
    
	
class UserValidator:
    """
    Class for validate authentication data and usertype,
    """

    def __init__(self, login, password, session):
        self.login = login   
        self.password = password
        self.session = session
        self.instance = None
        self.admin = False  
        self.auth = False  
        self.format = LoginFormat(self.login, self.password)
        self.auth = self.authenticate() 
        self.admin = self.is_admin() 
      

    def authenticate(self):
        """
        Function for routing queries to database for authentication,
        based on instance class LoginFormat 
        """
        
        login = self.login
        password = self.password

        if self.format.is_pass == True: 
            if self.format.is_email == True :

                try:
                    # Query should select only one instance, if none 
                    # or multiple user's will found, 
                    # validation will be rejected
                    query = select(User).where(User.email == login)
                    user = self.session.scalars(query).one()
                    self.session.close()

                    if user.password == password:
                        self.instance = user
                        return True
                    else:
                        return False    
                    
                except NoResultFound:
                    return False
                
                except MultipleResultsFound:
                    return False

            elif self.format.is_phone == True:

                try:
                    # Similar situation when using phone number, 
                    # only one instance is allowed
                    query = select(User).where(User.telephone_number == login)
                    user = self.session.scalars(query).one()
                    self.session.close()

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
        """
        When user will be authenticated, function will check role
        """
        user = self.instance
        if self.auth == True:
            if user.role == 'admin':
                return True  
            else:
                return False
        else:
            return False
