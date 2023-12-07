import os
import sys
import argparse
from script_files.user_actions import func_print_all_accounts
from script_files.user_actions import func_create_database






def commander():

    parser = argparse.ArgumentParser(description='Python CLI script,  coded by Wojciech Piwowarski')
    subparsers = parser.add_subparsers(dest='command', metavar='command list    /',  help='/  Description')

    create_database = subparsers.add_parser('create_database', help='Create Database')
    
    # print-all-accounts    # Admin 
    print_all_accounts = subparsers.add_parser('print-all-accounts', help='Print all accounts')
    print_all_accounts.add_argument('--login', required='print-all-accounts' in sys.argv, help='Login')
    print_all_accounts.add_argument('--password', required='print-all-accounts' in sys.argv, help='Password')

    # print-oldest-account  # Admin
    print_oldest_account = subparsers.add_parser('print-oldest-account', help='Print oldest account')
    print_oldest_account.add_argument('--login', required='print-all-accounts' in sys.argv, help='Login')
    print_oldest_account.add_argument('--password', required='print-all-accounts' in sys.argv, help='Password')

    # group-by-age   # Admin
    group_by_age = subparsers.add_parser('group-by-age', help='Group by age')
    group_by_age.add_argument('--login', required='print-all-accounts' in sys.argv, help='Login')
    group_by_age.add_argument('--password', required='print-all-accounts' in sys.argv, help='Password')
    

    # print-children  # User
    print_children = subparsers.add_parser('print-children', help='Print children')
    print_children.add_argument('--login', required='print-all-accounts' in sys.argv, help='Login')
    print_children.add_argument('--password', required='print-all-accounts' in sys.argv, help='Password')


    # find-similar-children-by-age    # User
    similar_children = subparsers.add_parser('find-similar-children-by-age', help='Find similar children by age')
    similar_children.add_argument('--login', required='print-all-accounts' in sys.argv, help='Login')
    similar_children.add_argument('--password', required='print-all-accounts' in sys.argv, help='Password')
    
    args = parser.parse_args()



    if args.command == 'create_database':
        status = func_create_database()
        print(status)
        # pass

    elif args.command == 'print-all-accounts':  # Admin
        result = func_print_all_accounts(args.login, args.password)
        print(result)

        # # TODO  args  user actions 
        # user = UserValidator(args.login, args.password)
    
        pass
    elif args.command == 'print-oldest-account':   # Admin
        print('oldest account')
        pass

    elif args.command == 'group-by-age':        # Admin
        pass

    elif args.command == 'print-children':      # User
        pass

    elif args.command == 'find-similar-children-by-age':    # User
        pass

    else:
        print('Uknown Command.')
        




    



if __name__ == '__main__':
    commander()





