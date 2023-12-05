import os
from script_files import data_collector
from script_files import data_validator

def path_setup():
    # Set the data dir name
    dir_name='data'

    root_path = os.path.dirname(os.path.abspath(__file__))
    parent_path = os.path.dirname(root_path)
    path = os.path.join(parent_path, dir_name)

    return path


def file_writer(data, path):
  
    with open(path, 'w') as file:
        for item in data:

            # todo  data validation

            valid=data_validator.DataValidator(data=item)
        
            if valid.validated is not None:
            
                file.write(str(valid.validated) + '\n') 



            # file.write(str(item) + '\n') 
            
        #file.write(str(data)) 

        
    

def main():
    
    path=path_setup()
    collector=data_collector.DataCollector(file_path=path)
    
    # print(collector.data)
    output_path='collected_data_validated2.txt'
    # Todo write
    # file_writer(collector.data_dict, output_path)
    #file_writer(collector.data, output_path)

    file_writer(collector.collected, output_path)


if __name__ == '__main__':
    main()