import os, pytest

from script_files.data_collector import DataCollector


@pytest.fixture
def csv_collector():
    root_path = os.path.dirname(os.path.abspath(__file__))
    data = 'test_data'
    path = os.path.join(root_path, data)
    collector = DataCollector(path)
    return  collector


def test_data_collection_csv_file(csv_collector):
    '''
    Test data collection from CSV file.
    '''
    collected_data = csv_collector.collected

    print(f'\n{collected_data[:3]}')
    assert collected_data is not None
    assert isinstance(collected_data, list)


@pytest.fixture
def xml_collector():
    root_path = os.path.dirname(os.path.abspath(__file__))
    data = 'test_data'
    path = os.path.join(root_path, data)
    collector = DataCollector(path)

    return collector


def test_data_collection_xml_file(xml_collector):
    '''
    Test data collection from XML file.
    '''
    collected_data = xml_collector.collected

    print(f'\n{collected_data[:3]}')
    assert collected_data is not None
    assert isinstance(collected_data, list)


@pytest.fixture
def json_collector():
    root_path = os.path.dirname(os.path.abspath(__file__))
    data = 'test_data'
    path = os.path.join(root_path, data)
    collector = DataCollector(path)
    return collector

def test_data_collection_json_file(json_collector):
    '''
    Test data collection from JSON file.
    '''
    collected_data = json_collector.collected

    print(f'\n{collected_data[:3]}')
    assert collected_data is not None
    assert isinstance(collected_data, list)




