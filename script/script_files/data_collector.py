import os
import csv, json
import xml.etree.ElementTree as ETree


class DataCollector:

    def __init__(self, file_path):
        self.file_path = file_path
        collected_data = self.data_collector()   
        self.collected = collected_data


    def data_collector(self):
        data = []
        header = None
        for root, dirs, files in os.walk(self.file_path):
                for file in files:
                    self.file_path = os.path.join(root, file)
                    name , extension = os.path.splitext(self.file_path)

                    if extension.lower() == '.csv': 
                        csv = self.read_csv()
                        
                        if header is None:
                            header = csv[0]
                        data.append(csv[1:])

                    if extension.lower() == '.json': 
                        json = self.read_json()
                        data.append(json)

                    if extension.lower() == '.xml': 
                        xml=self.read_xml()
                        data.append(xml)    

        flat_data=[]
        for list in data:
            flat_data.extend(list)

        return flat_data
    

    def read_csv(self):
        with open(self.file_path, 'r') as file:
            reader = csv.DictReader(file, delimiter=';')
            data_csv = []

            for row in reader:
                childrens = []

                if row['children']:
                    for children in row['children'].split(','):
                        name, age = children.strip().split()
                        childrens.append({'name': name, 'age': age})
                row['children'] = childrens
                data_csv.append(row)

        return data_csv



    def read_json(self):
        with open(self.file_path, 'r') as file:
            data_json = json.load(file)
        return data_json


    def read_xml(self, tags=None):
        tree = ETree.parse(self.file_path)
        root = tree.getroot()
        data_xml =[]

        for element in root.findall('.//user'):
            user_data = {
                'firstname': element.find('firstname').text,
                'telephone_number': element.find('telephone_number').text,
                'email': element.find('email').text,
                'password': element.find('password').text,
                'role': element.find('role').text,
                'created_at': element.find('created_at').text,
            }
            children_data = []
            for child_element in element.findall('.//child'):
                child_data = {
                    'name': child_element.find('name').text,
                    'age': child_element.find('age').text,
                }
                children_data.append(child_data)

            user_data['children'] = children_data
            data_xml.append(user_data) 

        return data_xml

        

