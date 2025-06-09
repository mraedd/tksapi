from flask import Flask, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# MySQL config
MYSQL_CONFIG = {
    'host': '127.0.0.1',    # Change to your MySQL server address
    'user': 'admin',
    'password': 'admin',
    'port': 3306,            # Default MySQL port
    'database': 'classicmodels'
}

def get_mysql_connection():
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

@app.route('/posts', methods=['GET'])
def get_wp_options():
    conn = get_mysql_connection()
    if conn is None:
        return jsonify({"error": "Could not connect to database"}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")  # Change to your table name
    wp_options = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(wp_options)

if __name__ == '__main__':
    app.run(debug=True)