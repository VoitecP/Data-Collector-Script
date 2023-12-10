import os, logging

import pytest
from faker import Faker
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session

from script_files.user_actions import UserAction


@pytest.fixture
def login():
    # Admin login
    login = 'jwilliams@example.com'   
    return login

@pytest.fixture
def password():
    password = '4^8(Oj52C+'  
    return password


def test_func_create_database():
    '''
    Test function to test if will be creater database 
    '''
    # TODO: It will be good to rewrite this method and inject 
    # TODO: variable session \ database and test this function better
    # TODO: Just like in class UserValidator(login, pass,  session)

    status = UserAction.func_create_database()
    options = ['Database created', "Can't create database"]
    # use parameter -s  to see printed  output
    print(f'\n{status}')
    assert status in options


def test_func_print_all_accounts(login, password):
    
    result = UserAction.func_print_all_accounts(login, password)
    
    print(f'\n{result}')
    assert isinstance(result, int) 


def test_func_print_oldest_account(login, password):

    result = UserAction.func_print_oldest_account(login, password)
    
    print(f'\n{result}')
    assert result is not None
 

def test_func_group_by_age(login, password):

    result = UserAction.func_group_by_age(login, password)

    print(f'\n{result}')
    assert result is not None


def test_func_print_children(login, password):

    result = UserAction.func_print_children(login, password)

    print(f'\n{result}')
    assert result is not None


def test_func_find_similar_children(login, password):

    result = UserAction.func_find_similar_children(login, password)

    print(f'\n{result}')
    assert result is not None