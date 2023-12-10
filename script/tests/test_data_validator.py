import json, os,  pytest

from script_files.data_validator import DataValidator


@pytest.fixture
def sample_data():
    """
    Fixture that reads sample data from a JSON file.
    """
    file_path = './tests/test_data/test_users.json'
    path = os.path.abspath(file_path)

    return read_data_from_file(path)


def read_data_from_file(path):
    with open(path, 'r') as file:
        return json.load(file)


def test_using_data_from_fixture(sample_data):
    assert isinstance(sample_data, list)
    assert len(sample_data) > 0
    

def test_data_validator_init(sample_data):
    """
    Test init function for DataValidator class
    """ 
    validator = DataValidator(sample_data)
    assert validator.data == sample_data


def test_duplicate_remover(sample_data):
    """
    Test the duplicate remover function for DataValidator class.
    """
    validator = DataValidator(sample_data)
    collected = validator.collected

    # Should be 4 unique items
    assert len(collected) == 4 

    phones = set(item['telephone_number'] for item in collected)
    assert len(phones) == len(collected)

    emails = set(item['email'] for item in collected)
    assert len(emails) == len(collected)


## Test's for class DataValidator with invalid data
test_data = [
        {
            'email': 'valid@example.test', 
            'telephone_number': '1344-567 89'
         },
        {
            'email': 'invalid-email@@.test',    # invalid email
            'telephone_number': '789-9900'      # invalid phone
        },
        {
            'email': 'anothervalid@example.test', 
            'telephone_number': '96 705 9321'
        },
    ]


@pytest.fixture
def data_validator():
    """
    Fixture for creating an instance of DataValidator for testing.
    Fixture with invalid input data email and phone for testing
    """
    return DataValidator(test_data)

def test_email_validator_valid(data_validator):
    data_validator.item = test_data[0]
    result = data_validator.email_validator()
    assert result is True

def test_email_validator_invalid(data_validator):
    data_validator.item = test_data[1]
    result = data_validator.email_validator()
    assert result is False

def test_phone_validator_valid(data_validator):
    data_validator.item = test_data[0]
    result = data_validator.phone_validator()
    assert result is True

def test_phone_validator_invalid(data_validator):
    data_validator.item = test_data[1]
    result = data_validator.phone_validator()
    assert result is False

