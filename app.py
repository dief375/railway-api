from flask import Flask, request, jsonify
import pymysql
import os

app = Flask(__name__)

# Get Railway MySQL credentials from environment variables
DB_HOST = os.getenv("MYSQLHOST", "pharm_mup_db.railway.app")
DB_USER = os.getenv("MYSQLUSER", "AhmedDief")
DB_PASSWORD = os.getenv("MYSQLPASSWORD", "Awad$375")
DB_NAME = os.getenv("MYSQLDATABASE", "Pharm_db")
DB_PORT = int(os.getenv("MYSQLPORT", 3306))

def get_db_connection():
    return pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME, port=DB_PORT, cursorclass=pymysql.cursors.DictCursor)

@app.route("/products", methods=["GET"])
def get_products():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM products")  # Change 'products' to your table name
            result = cursor.fetchall()
        connection.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)