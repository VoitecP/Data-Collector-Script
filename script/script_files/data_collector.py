import os
import csv, json
import xml.etree.ElementTree as ETree


class DataCollector:
    """
    Class for collecting and parsing data from given folder (need folder path)
    Can serach also thru  subfolders.
    Supports CSV, JSON, XML file types.
    """

    def __init__(self, file_path):
        self.file_path = file_path
        self.collected = self.data_collector()   

    def data_collector(self):
        """
        Function for collecting all datafrom file parsers to common list 
        """
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
                        xml = self.read_xml()
                        data.append(xml)    

        flat_data=[]
        # Flating data to get clean data and easy to process
        for list in data:
            flat_data.extend(list)

        return flat_data

    def read_csv(self):
        """
        CSV file parser
        """
        with open(self.file_path, 'r') as file:
            reader = csv.DictReader(file, delimiter=';')
            data_csv = []

            for row in reader:
                childrens = []

                if row['children']:
                    for children in row['children'].split(','):
                        name, age = children.strip().split()
                        age = age.replace('(', '').replace(')', '')
                        childrens.append({'name': name, 'age': int(age)})
                row['children'] = childrens
                data_csv.append(row)

        return data_csv

    def read_json(self):
        """
        JSON file parser
        """
        with open(self.file_path, 'r') as file:
            data_json = json.load(file)
            
        return data_json

    def read_xml(self, tags=None):
        """
        XML file parser
        """
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
                    'age': int(child_element.find('age').text),
                }
                children_data.append(child_data)

            user_data['children'] = children_data
            data_xml.append(user_data) 

        return data_xml

    