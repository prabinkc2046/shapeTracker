from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import datetime
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import time
import os
import re

app = Flask(__name__, static_url_path='/static')

# Global variables for MySQL connection and cursor
cnx = None
cursor = None
current_user = None

# Connect to the MySQL database
def connect_to_mysql():
    while True:
        try:
            cnx = mysql.connector.connect(
                host=os.environ.get('DB_HOST'),
                user=os.environ.get('DB_USER'),
                password=os.environ.get('DB_PASSWORD'),
                database=os.environ.get('DB_NAME')
            )
            return cnx
        except mysql.connector.Error:
            time.sleep(1)

def wait_for_mysql():
    while True:
        try:
            cnx.ping(reconnect=True)  # Ping the database to check the connection
            break
        except mysql.connector.Error:
            time.sleep(1)

def sanitize_table_name(username):
    # Remove special characters and spaces from the username and replace them with underscores
    sanitized_username = re.sub(r'[^a-zA-Z0-9]', '_', username)
    return f"{sanitized_username}_fitness_data"

@app.route('/', methods=['GET', 'POST'])
def login():
    global current_user  # Access the global current_user variable

    if request.method == 'POST':
        existing_user = request.form.get('existing_user')

        if existing_user == 'yes':
            username = request.form.get('username')
            password = request.form.get('password')

            # SQL statement to fetch the user with matching username and password
            sql = "SELECT * FROM user WHERE username = %s AND password = %s"
            values = (username, password)

            # Execute the SQL statement
            cursor.execute(sql, values)

            # Fetch the first row
            row = cursor.fetchone()

            if row is not None:
                current_user = username
                print(f"User '{username}' logged in successfully!")
                return redirect(url_for('index'))
            else:
                print(f"Failed login attempt for user '{username}'. Invalid username or password!")
                return render_template('login.html', error_message='Invalid username or password!')

        else:
            username = request.form.get('username')
            password = request.form.get('password')

            # SQL statement to fetch the user with matching username
            sql = "SELECT * FROM user WHERE username = %s"
            values = (username,)

            # Execute the SQL statement
            cursor.execute(sql, values)

            # Fetch the first row
            row = cursor.fetchone()

            if row is not None:
                print(f"Failed registration attempt for user '{username}'. Username already exists!")
                return render_template('login.html', error_message='Username already exists!')

            # SQL statement to insert data into the user table
            sql = "INSERT INTO user (username, password) VALUES (%s, %s)"
            values = (username, password)

            # Execute the SQL statement
            cursor.execute(sql, values)

            # Commit the changes to the database
            cnx.commit()

            # Create a new table for the user
            table_name = sanitize_table_name(username)

            # SQL statement to create the table if it doesn't exist
            create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} (id INT AUTO_INCREMENT PRIMARY KEY, timestamp VARCHAR(20), waist_size FLOAT, weight FLOAT)"

            # Execute the SQL statement
            cursor.execute(create_table_sql)

            # Commit the changes to the database
            cnx.commit()

            current_user = username
            print(f"User '{username}' registered successfully!")
            return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/form', methods=['GET', 'POST'])
def index():
    global cnx, cursor, current_user  # Access the global connection, cursor, and current_user variables

    if current_user is None:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Get user input from the form
        waist = float(request.form['waist'])
        weight = float(request.form['weight'])

        # Get current timestamp
        current_time = datetime.datetime.now().strftime('%b %d')

        wait_for_mysql()

        # Use the global connection and cursor
        cursor = cnx.cursor()

        # Table name for the user's fitness data
        table_name = sanitize_table_name(current_user)

        # SQL statement to insert data into the user's fitness data table
        sql = f"INSERT INTO {table_name} (timestamp, waist_size, weight) VALUES (%s, %s, %s)"
        values = (current_time, waist, weight)

        # Execute the SQL statement
        cursor.execute(sql, values)

        # Commit the changes to the database
        cnx.commit()

        # Ask if the user wants to view their progress
        choice = request.form['progress']
        if choice.lower() == "yes":
            print(f"User '{current_user}' added progress data and wants to view it!")
            return redirect(url_for('view_progress'))
        else:
            print(f"User '{current_user}' added progress data and chose not to view it.")
            return "Okay, exiting..."
    else:
        return render_template('form.html', username=current_user)

@app.route('/view_progress', methods=['GET'])
def view_progress():
    global cnx, cursor, current_user  # Access the global connection, cursor, and current_user variables

    if current_user is None:
        return redirect(url_for('login'))

    wait_for_mysql()

    # Use the global connection and cursor
    cursor = cnx.cursor()

    # Table name for the user's fitness data
    table_name = sanitize_table_name(current_user)

    # SQL statement to fetch all entries from the user's fitness data table
    sql = f"SELECT * FROM {table_name}"

    # Execute the SQL statement
    cursor.execute(sql)

    # Fetch all the rows
    rows = cursor.fetchall()

    # Check if the user has any progress data
    if not rows:
        print(f"User '{current_user}' does not have any progress data.")
        return "No progress data available."

    # Separate the fetched data
    timestamps = []
    print("Time Stamps:", timestamps)
    waist_sizes = []
    weights = []

    for row in rows:
        _, timestamp, waist_size, weight = row
        timestamps.append(str(timestamp))
        print("after appended:", timestamps)
        waist_sizes.append(waist_size)
        weights.append(weight)

    # Plotting the waist size graph
    plt.subplot(2, 1, 1)
    plt.bar(timestamps, waist_sizes, color='cyan')
    plt.xlabel('')
    plt.ylabel('Waist Size (cm)')
    plt.title('Waist Size Progress Over Time')

    # Plotting the weight graph
    plt.subplot(2, 1, 2)
    plt.bar(timestamps, weights, color='orange')
    plt.xlabel('')
    plt.ylabel('Weight (kg)')
    plt.title('Weight Progress Over Time')

    # Adjust layout
    plt.tight_layout()

    # Save the graph to a BytesIO object
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)

    # Encode the image as base64
    encoded_image = base64.b64encode(image_stream.getvalue()).decode('utf-8')

    # Clear the current figure to avoid overlapping plots
    plt.clf()

    return render_template('view_progress.html', graph=encoded_image, username=current_user)



@app.route('/logout', methods=['GET'])
def logout():
    global current_user  # Access the global current_user variable
    current_user = None
    print("User logged out.")
    return redirect(url_for('login'))

if __name__ == '__main__':
    cnx = connect_to_mysql()  # Establish the initial connection
    cursor = cnx.cursor()
    app.run(host="0.0.0.0")
