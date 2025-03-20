from flask import Flask, jsonify, request
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
@app.route("/Users", methods=["POST"])
def add_user():
    try:
        data = request.get_json()
        user_id = data.get("id")
        user_name = data.get("User_Name")
        user_address = data.get("User_Address")
        user_password = data.get("User_Password")

        if not user_name or not user_address or not user_password:
            return jsonify({"error": "Missing required fields"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Users (id, User_Name, User_Address, User_Password) VALUES (%s, %s, %s, %s)",
            (user_id, user_name, user_address, user_password),
        )
        conn.commit()

        cursor.close()
        conn.close()
        return jsonify({"message": "User added successfully!"}), 201

    except mysql.connector.Error as err:
        return jsonify({"error": f"MySQL Error: {err}"}), 500
@app.route("/Users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Get the JSON data from the request
        data = request.get_json()
        new_name = data.get("User_Name")
        new_address = data.get("User_Address")

        # Ensure required fields are present
        if not new_name or not new_address:
            return jsonify({"error": "User_Name and User_Address are required"}), 400

        # Execute update query
        cursor.execute(
            "UPDATE Users SET User_Name = %s, User_Address = %s WHERE id = %s",
            (new_name, new_address, user_id),
        )
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": "User updated successfully"}), 200

    except mysql.connector.Error as err:
        return jsonify({"error": f"MySQL Error: {err}"}), 500

    except Exception as e:
        return jsonify({"error": f"Unexpected Error: {str(e)}"}), 500
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Use Railway's assigned port
    app.run(host="0.0.0.0", port=port, debug=True)
