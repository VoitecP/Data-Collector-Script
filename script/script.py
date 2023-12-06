import os
from script_files.data_collector import DataCollector 
from script_files.data_validator import DataValidator 
from script_files.db_manager import read_test, create_database


def path_setup():
    # Set the data directory name
    dir_name='data'

    root_path = os.path.dirname(os.path.abspath(__file__))
    parent_path = os.path.dirname(root_path)
    path = os.path.join(parent_path, dir_name)

    return path


# def file_writer(data, path):
def db_writer():
  
        path = path_setup()
        collector = DataCollector(path)
        data = collector.collected
        valid = DataValidator(data)
        valid_data = valid.collected
        create_database(valid_data)



     

def main():

    db_writer()

    
    pass

def test():

    
    print('test')
    

    #db = python script.py create_database

    pass


if __name__ == '__main__':
    main()

    #test()