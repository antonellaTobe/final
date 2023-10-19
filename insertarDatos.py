from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import mysql.connector
from datetime import datetime
import random

# TODO: Call the createConnection() function and store the connection and cursor in variables.
def createConnection(user_name, database_name, user_password, host, port):
    """Creates a connection to the MySQL database

    Parameters
    -----------
        user_name {string} -- The username to the database
        database_name {string} -- The name of the database
        user_password {string} -- The password to the database
        host {string} -- The host of the database
        port {string} -- The port of the database

    Returns
    --------
        tuple -- A tuple containing the connection and the cursor
    """
    cnx = mysql.connector.connect(user=user_name, database=database_name, password=user_password, host=host, port=port)
    cursor = cnx.cursor()
    return (cnx, cursor)

def select_data():
    """Selects all the data from the database"""
    try:
        # Create a connection to the database
        cnx, cursor = createConnection('sql10652855', 'sql10652855', 'qN8cu9iQtI', 'sql10.freemysqlhosting.net', '3306')

        # Query the database
        query = ("SELECT * FROM dht_sensor_data")

        # Execute the query
        cursor.execute(query)

        # Get the data
        data = cursor.fetchall()

        # Close the connection
        cursor.close()
        cnx.close()

        # Return the data
        return data

    except mysql.connector.Error as err:
        """Handle possible errors"""
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

def create_data():
    """Inserts random sensor data into the database"""
    # For the float values, use the random.uniform() function.
    # Humidity: 0 to 100%, +-5%.
    humidity = float(random.uniform(0, 100) * random.uniform(0.95, 1.05))

    # Temperature: 0 to 100%, +-5%.
    temperature = float(random.uniform(0, 100) * random.uniform(0.95, 1.05))

    smoke = float(random.uniform(0, 100) * random.uniform(0.95, 1.05))
    
    # Date/Time: Current date and time
    current_datetime = datetime.now()
    
    # When you have the data, print it out to the console.
    print(f"Random Sensor Data - Humidity: {humidity}%, Temperature: {temperature}°C, Smoke: {smoke}, Timestamp: {current_datetime}")
    
    return humidity, temperature, smoke, current_datetime

def insert_data(humidity, temperature, smoke, date_time, cnx, cursor):
    try:
        # Query the database
        query = "INSERT INTO dht_sensor_data (humidity, temperature, smoke, date_time) VALUES (%s, %s, %s, %s)"
        
        # Data to insert
        data = (humidity, temperature, smoke, date_time)
        
        # Execute the query with the data
        cursor.execute(query, data)
        
        # Commit the changes
        cnx.commit()
        
        print("Data inserted successfully")
    
    except mysql.connector.Error as err:
        """Handle possible errors"""
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

    # No need to close the connection and cursor here, as they are closed later in the main loop

def create_plot(data):
    # Create a DataFrame from the data
    df = pd.DataFrame(data, columns=["id_dht_data", "humidity", "temperature", "smoke", "date_time"])
    
    # Create a line chart using Plotly Express
    fig = px.line(df, x="date_time", y=["humidity", "temperature", "smoke"], title="Sensor Data")
    
    return fig

if __name__ == '__main__':
    # Create a connection to the database
    cnx, cursor = createConnection('sql10652855', 'sql10652855', 'qN8cu9iQtI', 'sql10.freemysqlhosting.net', '3306')

    # Select data from the database
    data = select_data()

    # Generate and insert random data into the database
    for i in range(100):
        hum, temp, smo, dat = create_data()
        insert_data(hum, temp, smo, dat, cnx, cursor)

    # Create a plot using the data
    fig = create_plot(data)

    # Create a Dash app
    app = Dash(__name__)
    app.layout = html.Div([
        html.H1("Sensor Data Visualization"),
        dcc.Graph(figure=fig)
    ])

    # Run the Dash app
    app.run_server(debug=True)

    # Close the connection and cursor
    cursor.close()
    cnx.close()