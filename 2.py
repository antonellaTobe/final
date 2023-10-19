from dash import Dash, html, dcc
import plotly.express as px
import mysql.connector
import pandas as pd

# Define the function to create a database connection
def createConnection(user_name, database_name, user_password, host, port):
    cnx = mysql.connector.connect(user=user_name, database=database_name, password=user_password, host=host, port=port)
    cursor = cnx.cursor()
    return (cnx, cursor)

# Define the function to retrieve sensor data from the database
def select_data():
    try:
        # Create a database connection
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
        # Handle possible errors
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    finally:
        # Close the connection
        if ('cnx' in locals() or 'cnx' in globals()) and ('cursor' in locals() or 'cursor' in globals()):
            cnx.close()
            cursor.close()

# Retrieve sensor data from the database
data = select_data()

# Create a DataFrame from the retrieved data
df = pd.DataFrame(data, columns=["id_dht_data", "humidity", "temperature", "smoke", "date_time"])

# Create a plot using Plotly Express
fig = px.line(df, x="date_time", y=["humidity", "temperature", "smoke"], title="Line Graph")

app = Dash(__name__)

# Define the layout of the Dash app
app.layout = html.Div([
    html.Div(
        children=[
            html.H1("Temperature, humidity and smoke", style={'text-align': 'center'}),
            dcc.Graph(figure=fig)
        ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
    




