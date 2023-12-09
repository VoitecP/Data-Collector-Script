import re


class DataValidator:
    """
    Class for validating, colledted data.
    Removes duplicated accounts, or invalid logins (phone, email)...
    """

    def __init__(self, data):
        self.data = []
        self.item = {}
        self.collected = []
        self.data = data   
        collected=self.duplicat_remover()
        self.collected = collected
            

    def duplicat_remover(self):
        """
        Function for removing duplicates.
        If valid but duplicated account will be found, 
        function will replace older instance  for newer one.
        """
        collected = []
        unique_phone = set()
        unique_mail = set()

        for item in self.data:
            self.item = item
            # In first place login should be validated 
            # and with proper format
            valid = self.item_validator() 

            if valid is not None:
                mail = valid['email']
                phone = valid['telephone_number']

                if (mail not in unique_mail and
                    phone not in unique_phone):

                    # If mail and phone is uniqe, 
                    # account will be collected as valid
                    unique_mail.add(mail)
                    unique_phone.add(phone)
                    collected.append(valid)
                
                elif (mail in unique_mail or
                    phone in unique_phone):

                    for item in self.collected:
                        if (valid['email'] == item['email'] or
                            valid['telephone_number'] == item['telephone_number']): 

                            if valid['created_at'] > item['created_at']:
                                item = valid
  
        return collected

    def item_validator(self):
        """
        Function for managing order of login (email or phone)
        to validate.
        Order is set specifficaly to get optimal time in processing data.
        """

        is_valid = self.phone_validator()
        if is_valid == True:
            is_valid = self.email_validator()
    
            if is_valid == True:
                validated_dict = self.phone_formatter()

                return validated_dict
            
            else:
                return None
        else:
            return None
    

    def email_validator(self):
        """
        Email validator, based on predefined patterns.
        """

        email = self.item.get('email')
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
           

    def phone_validator(self):
        """
        Phone validator, for find empty fields
        """
        phone = self.item.get('telephone_number')

        if phone:
            return True
        else:
            return False
       
    
    def phone_formatter(self):
        """
        Phone field formatter
        """
        dict_data = self.item
        phone_data = dict_data.get('telephone_number')
        phone = phone_data.replace(" ", "")[-9:]
        dict_data['telephone_number'] = phone
    
        return dict_data

