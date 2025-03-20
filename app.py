from flask import Flask, jsonify
import mysql.connector
import os
#from dotenv import load_dotenv

# Load environment variables
#load_dotenv()

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
        users = cursor.fetchall()
        
        print("Fetched users:", users)  # Debugging print
        
        cursor.close()
        conn.close()
        
        return jsonify(users)

    except mysql.connector.Error as err:
        print("Database error:", err)
        return jsonify({"error": str(err)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
