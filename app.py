from flask import Flask, jsonify
import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("mysql-zlgj.railway.internal"),
        port=os.getenv("3306"),
        user=os.getenv("root"),
        password=os.getenv("kOTjbNUhdwMeEaMnIfqLuiCqBcLlERGC"),
        database=os.getenv("railway"),
    )

@app.route("/")
def home():
    
    return jsonify({"message": "products"})

@app.route("/Users", methods=["GET"])
def get_products():
   try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM Users")
        products = cursor.fetchall()

        cursor.close()
        conn.close()
        
        return jsonify(products)
    
   except mysql.connector.Error as err:
        return jsonify({"error": f"MySQL Error: {err}"}), 500
    
   except Exception as e:
        return jsonify({"error": f"Unexpected Error: {str(e)}"}), 500

    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
