from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# MySQL connection config (change these)
db_config = {
    'host': '127.0.0.1',
    'user': 'admin',
    'password': 'admin',
    'database': 'wpdb',
    'port': 3306
}

def run_query(query):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)  # return dict rows
        cursor.execute(query)

        if query.strip().lower().startswith('select'):
            result = cursor.fetchall()
        else:
            conn.commit()
            result = {'affected_rows': cursor.rowcount}

        cursor.close()
        conn.close()
        return result

    except Error as e:
        return {'error': str(e)}

@app.route('/query', methods=['POST'])
def query_endpoint():
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({'error': 'Missing "query" in JSON body'}), 400

    query = data['query']
    result = run_query(query)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)