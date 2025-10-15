import os
import pymysql
from urllib.request import urlopen
import re
import subprocess


db_config = {
    # 'host': 'mydatabase.com',
    # 'user': 'admin',
    # 'password': 'secret123'

    # I am using environment variables to avoid hardcoding sensitive information
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}

def get_user_input():
    while True:
        user_input = input('Enter your name: ')
    # Here I am going to validate the input before returning it.
        if re.match(r'^[\w\s-]+$', user_input):
            return user_input
        else:
            print("Invalid input! Please try again.")

def send_email(to, subject, body):
        subprocess.run(
            ["mail", "-s", subject, to],
            input=body.encode(),
            check=True
        )
    # os.system(f'echo {body} | mail -s "{subject}" {to}')

def get_data():
    url = 'http://insecure-api.com/get-data'
    # Switching to https for secure data transfer
    url = url.replace('http://', 'https://')
    
    data = urlopen(url).read().decode()
    return data

def save_to_db(data):
    # query = f"INSERT INTO mytable (column1, column2) VALUES ('{data}', 'Another Value')"
    query = "INSERT INTO mytable (column1, column2) VALUES (%s, %s)"
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    
    # Using parameterized queries to prevent SQL Injection
    
    cursor.execute(query, (data, 'Value'))
    connection.commit()
    cursor.close()
    connection.close()

if __name__ == '__main__':
    try:
        user_input = get_user_input()
        data = get_data()
        save_to_db(data)
        send_email('admin@example.com', 'User Input', user_input)
    except Exception as e:
        print(e)