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
        host=os.getenv("DB_HOST", "mysql-zlgj.railway.internal"),
        port=int(os.getenv("DB_PORT", 3306)),  # Convert to int
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "kOTjbNUhdwMeEaMnIfqLuiCqBcLlERGC"),
        database=os.getenv("DB_NAME", "railway"),
    )

@app.route("/")
def home():
    return jsonify({"message": "Welcome to Products API"})

@app.route("/Users", methods=["GET"])
def get_products():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Users")


        
        products = cursor.fetchall()
        print("Success")  

        cursor.close()
        conn.close()
        
        return jsonify(products), 200 
    
    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return jsonify({"error": f"MySQL Error: {err}"}), 500
    
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return jsonify({"error": f"Unexpected Error: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Use Railway's assigned port
    app.run(host="0.0.0.0", port=port, debug=True)
