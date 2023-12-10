import os
from typing import List
from sqlalchemy import create_engine, inspect,  Integer, func, ForeignKey, String

from sqlalchemy.orm import DeclarativeBase, Mapped, sessionmaker
from sqlalchemy.orm import mapped_column, relationship

from script_files.data_collector import DataCollector
from script_files.data_validator import DataValidator 


## Settings  for folder name, and data base  file name
DATA_DIR = 'data'
DB_FILE = 'database.db'


class Base(DeclarativeBase):
    pass


class Child(Base):
    """
    Class to represent Child's from collected data in DB tables,
    related to User by ForeginKey
    """

    __tablename__ = 'childrens'

    id : Mapped[int] = mapped_column(primary_key=True)
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"))
    name : Mapped[str] = mapped_column(String)
    age : Mapped[str] = mapped_column(Integer)

    def __str__(self):
        return f'{self.name}, {self.age}'


class User(Base):
    """
    Class to represent User's from collected data in DB tables
    """

    __tablename__ = 'users'

    id : Mapped[int] = mapped_column(primary_key=True)
    firstname : Mapped[str] = mapped_column(String)
    telephone_number : Mapped[str] = mapped_column(String)
    email : Mapped[str] = mapped_column(String)
    password : Mapped[str] = mapped_column(String)
    role : Mapped[str] = mapped_column(String)
    created_at : Mapped[str] = mapped_column(String)
    children : Mapped[List["Child"]] = relationship('Child', backref='user')

    def __init__(self, data):
        self.firstname = data.get('firstname')
        self.telephone_number = data.get('telephone_number')
        self.email = data.get('email')
        self.password = data.get('password')
        self.role = data.get('role')
        self.created_at = data.get('created_at')

        children = []
        for child_data in data.get('children', []):
            child = Child(name = child_data.get('name'), 
                          age = child_data.get('age'))
            children.append(child)
        self.children = children

    def __str__(self):
        return f'name: {self.firstname}\nemail_address: {self.email}\ncreated_at: {self.created_at}'


class DataBaseManager:
    """
    Common class for all staticmethod for managing and processing database
    """
    #TODO: I think, it will be good to isolate session as another method or variable
    #TODO: to inject data to specific session / database

    @staticmethod
    def create_database(data):
        """
        Method for creating database thru manual command.
        If existing file will be found, function will delete database,
        collect data and create new instance of database.
        If success or unsuccess, function will return proper status.
        """
        
        path = DataBaseManager.return_db_path()

        if os.path.exists(path):
            try:
                os.remove(path)
            except:
                return "Can't create database"
    
        if  not os.path.exists(path):
            try:
                engine = create_engine(f'sqlite:///{DB_FILE}')
                Base.metadata.create_all(engine)
                Session = sessionmaker(bind=engine)
                session = Session()

                for item in data:
                    user = User(item)
                    session.add(user)
                session.commit()
                session.close()
                return "Database created"
            
            except:
                session.rollback()
                session.close()
                return "Can't create database"
                   

    @staticmethod
    def return_data_path():
        """
        Method for set proper path to data folder.
        It uses this schema:
                \n
        Parent_Dir \n
        |           \n
        |__<data>     \n
        |              \n
        |__script       \n
                |               \n
                |___ script.py   \n
                ......            \n
        """

        root_path = os.path.dirname(os.path.abspath(__file__))
        lvl1_path = os.path.dirname(root_path)
        lvl2_path = os.path.dirname(lvl1_path)
        path = os.path.join(lvl2_path, DATA_DIR)
        return path

    @staticmethod
    def return_db_path():
        """
        Method return path to database 
        """

        root_path = os.path.dirname(os.path.abspath(__file__))
        lvl1_path = os.path.dirname(root_path)
        path = os.path.join(lvl1_path, DB_FILE)
        return path


    @staticmethod
    def data_validator():
        """
        Method for collecting and validating data, returns valid data
        """

        path = DataBaseManager.return_data_path()
        data = DataCollector(path).collected
        valid_data = DataValidator(data).collected
        return valid_data
    

    @staticmethod
    def db_switcher():
        """
        Method for swithing between databases. If data in database file are corrupted
        method will load data to memory
        """
        
        path = DataBaseManager.return_db_path()
        corrupted = False   # Watchdog

        if os.path.exists(path):
            try:
                engine = create_engine(f'sqlite:///{DB_FILE}')
                Session = sessionmaker(bind=engine)
                session = Session()
                inspector = inspect(engine)
                # Returns table names if exist's
                tables = inspector.get_table_names()

                if not tables:
                    corrupted = True
                  
                if tables:
                    count = (
                        session
                        .query(func.count(User.id))
                        .limit(20)
                        .scalar()
                    )
                    if count > 0:
                        # Database exist and seems to be valid
                        corrupted = False
                        return session
                
                # Database can be valid but empty (no User rows)
                corrupted = True
                session.close()
               
            except:
                corrupted = True
                session.close()
                
        if corrupted:   # Database file  empty or corrupted,
            try:
                engine = create_engine('sqlite:///:memory:')
                Base.metadata.create_all(engine)
                Session = sessionmaker(bind=engine)
                session = Session()

                # Validatin and importing data
                valid_data = DataBaseManager.data_validator()

                for item in valid_data:
                    user = User(item)
                    session.add(user)
                session.commit()
                session.close()

            except:
                corrupted = True
                # Ups, computer malfunction ;)
                return 'Memory error'   
                   
        return session




