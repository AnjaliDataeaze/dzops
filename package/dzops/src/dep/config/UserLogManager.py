from psycopg2.extras import RealDictCursor
import requests
from dzops.src.dep.config.Connection import *
from dzops.src.dep.InputProperties import *
prop=properties()
connection = Connection()
conn = connection.get_connection()

class User_log:
    def login(self,access_token,username):
        try:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            file_path = os.path.join(dir_path, 'udops_config')

            url = 'https://api.github.com/user'
            headers = {'Authorization': f'token {access_token}'}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                github_username = response.json()['login']
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                query = f"select user_name from udops_users where user_name = '{username}';"
                cursor.execute(query)
                rows = cursor.fetchone()
                database_username = rows['user_name']
                conn.commit()

                if username != github_username:
                    print('Wrong username')
                elif github_username != database_username:
                    print('Username Doesnt exist in Udops')
                else:
                    config = configparser.ConfigParser()
                    config.read(dir_path + '/udops_config')
                    if 'github' not in config:
                        config.add_section('github')
                    config.set('github', 'ACCESS_TOKEN', access_token)

                    with open(dir_path + '/udops_config', 'w') as config_file:
 

                        config.write(config_file)
                    print("login Successfully !!!")

            else:
                return print(response.status_code)
        except Exception as e:
            print(e)

    def logout(self):
        data_to_erase = 'github'
        dir_path = os.path.dirname(os.path.realpath(__file__))


        with open(dir_path + "/udops_config", 'r') as file:

            



            lines = file.readlines()

        modified_lines = [line for line in lines if data_to_erase not in line]




        with open(dir_path + "/udops_config", 'w') as file:
            print("Logout Successful")






