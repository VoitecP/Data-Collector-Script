import re


class DataValidator:


    def __init__(self, data):
        self.data = data
        validated_data = self.data_validator()   
        self.validated = validated_data
        

    def data_validator(self):

        is_valid = self.phone_validator()
        if is_valid == True:
            is_valid = self.email_validator()
    
            if is_valid == True:
                validated_dict=self.phone_formatter()

                return validated_dict
            
            else:
                return None
        else:
            return None
    

    def email_validator(self):

        email = self.data.get('email')
        pattern_1 = re.compile(r'^[^@]*@[^@]*$')
        pattern_2 = re.compile(r'^.+@.+?\.')
        pattern_3 = re.compile(r'\.[a-zA-Z0-9]{1,4}$')
    
        # bool_1 = bool(pattern_1.match(email))
        # bool_2 = bool(pattern_2.match(email))
        # bool_3 = bool(pattern_3.search(email))
        # patterns=[bool_1,bool_2,bool_3]

        patterns=[
            (bool(pattern_1.match(email))),
            (bool(pattern_2.match(email))),
            (bool(pattern_3.search(email))),
        ]

        if all(patterns):
            return True
        else:
            return False
           

    def phone_validator(self):

        phone = self.data.get('telephone_number')

        if phone:
            return True
        else:
            return False
       
    
    def phone_formatter(self):

        dict_data=self.data
        phone_data = dict_data.get('telephone_number')
        phone=phone_data.replace(" ", "")[-9:]
        dict_data['telephone_number'] = phone
    
        return dict_data
