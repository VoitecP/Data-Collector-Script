#### How to Set up

Clone repository to specific folder:
```
git clone https://github.com/VoitecP/Profile-Software-Task.git
```
You need to have installed Poetry package. If you don't have, please install using this command:
```
pip install poetry
```
Navigate to script folder by command:
```
cd Data-Collector-Script\script
```
Set poetry global option, to use project folder as place to hold Virtual environment (recommended):
```
poetry config virtualenvs.in-project true
```
Install virtual environment, using current dependencies:
```
poetry install
```



#### Run script using commands below ( In Windows )

To create and use local database
```
poetry run python script.py create_database
```

- If you dont want to create local database, you can just use this script 
using commands in format below, database will be stored in RAM memory,


- Remember about your valid data credentials.
- You can use both email or phone as login

#### Commands for admin only:
 
```
poetry run python script.py print-all-accounts --login <login> --password <password>
```
```
poetry run python script.py print-oldest-account --login <login> --password <password>
```
```
poetry run python script.py group-by-age --login <login> --password <password>
```
    
#### Commands for all users:
```
poetry run python script.py print-children --login <login> --password <password>
```
```
poetry run python script.py find-similar-children-by-age --login <login> --password <password>
```


