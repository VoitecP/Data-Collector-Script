import re
from script_files import data_validator

def main():


    dict_data={
            'key':'value',
            'email':'sadsada@dass.pl!',
            'telephone_number': '(+48)123456789',
         }


    validator=data_validator.DataValidator(data=dict_data)
    
    print(validator.validated)
    






if __name__ == '__main__':
    main()



