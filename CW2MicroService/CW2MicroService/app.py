import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
import pyodbc

# Flask App Setup
app = Flask(__name__, static_url_path='', static_folder='static')

# Swagger UI setup
SWAGGER_URL = '/swagger'  # URL to access Swagger UI
API_URL = '/static/swagger.yaml'  # Path to the Swagger YAML file

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "TrailServiceAPI"}
)

# Register the blueprint
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# Authentication API endpoint
auth_url = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"

# Serve swagger.yaml from the static folder
@app.route("/swagger.yaml")
def swagger_yaml():
    return send_from_directory('static', 'swagger.yaml')

# Verify Credentials Function
def verify_credentials(email, password):
    response = requests.post(auth_url, json={"email": email, "password": password})  # Changed to json format
 
    if response.status_code == 200:
        try:
            json_response = response.json()

            print(f"Response content: {json_response}")  # Debug output to check what you're getting
            
            if len(json_response) > 1 and json_response[0] == "Verified" and json_response[1] == "True":
                print("Authentication successful!")
                return True
            else:
                print("Authentication failed: User not verified.")
                return False

        except requests.JSONDecodeError:
            print("Response is not valid JSON. Raw response content:")
            print(response.text)
            return False
    else:
        print(f"Authentication failed with status code {response.status_code}")
        print("Response content:", response.text)
        return False

# Check authentication before running the app
def check_authentication():
    # Retrieve email and password from environment variables, headers, or user input
    email = "grace@plymouth.ac.uk"  # Replace with dynamic email input
    password = "ISAD123!"   # Replace with dynamic password input
    
    # Authenticate with the web API using the provided email and password
    if verify_credentials(email, password):
        print("Authentication successful!")
        return True
    else:
        print("Authentication failed!")
        return False

# Check authentication before running the app
if check_authentication():
    print("Starting the Trail Service API...")

    # Database Connection Configuration
    DB_CONFIG = {
        "driver": "{ODBC Driver 17 for SQL Server}",
        "server": "localhost",
        "database": "COMP2001CW2",
        "username": "SA",
        "password": "C0mp2001!"
    }

    # Database Connection
    def get_db_connection():
        try:
            conn = pyodbc.connect(
                f"DRIVER={DB_CONFIG['driver']};"
                f"SERVER={DB_CONFIG['server']};"
                f"DATABASE={DB_CONFIG['database']};"
                f"UID={DB_CONFIG['username']};"
                f"PWD={DB_CONFIG['password']}"
            )
            return conn
        except Exception as e:
            print(f"Error: {e}")
            return None

    # Route: Get All Trails
    @app.route("/trails", methods=["GET"])
    def get_trails():
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Failed to connect to the database."}), 500

        cursor = conn.cursor()
        query = "SELECT * FROM CW2.Trails"

        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            trails = [{"ID": row[0], "TrailName": row[1], "TrailLength": row[2]} for row in rows]
            return jsonify(trails)
        except Exception as e:
            print(f"Database error: {e}")
            return jsonify({"error": "Failed to fetch trails."}), 500
        finally:
            cursor.close()
            conn.close()

    # Route: Add a New Trail
    @app.route("/trails", methods=["POST"])
    def add_trail():
        data = request.get_json()

        trail_name = data.get("TrailName")
        trail_length = data.get("TrailLength")

        if not trail_name or not trail_length:
            return jsonify({"error": "Both TrailName and TrailLength are required"}), 400

        if not isinstance(trail_length, (int, float)):
            return jsonify({"error": "TrailLength must be a number"}), 400

        # Insert data into the database
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Failed to connect to the database."}), 500

        cursor = conn.cursor()
        query = "INSERT INTO CW2.Trails (TrailName, TrailLength) VALUES (?, ?)"
        try:
            cursor.execute(query, (trail_name, trail_length))
            conn.commit()
            return jsonify({"message": "Trail added successfully"}), 201
        except Exception as e:
            print(f"Database error: {e}")
            return jsonify({"error": "Failed to add trail."}), 500
        finally:
            cursor.close()
            conn.close()

    # Route: Add a New User (Only Name)
    @app.route("/users", methods=["POST"])
    def add_user():
        data = request.get_json()

        name = data.get("UserName")

        if not name:
            return jsonify({"error": "Name is required"}), 400

        # Insert data into the database
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Failed to connect to the database."}), 500

        cursor = conn.cursor()
        query = "INSERT INTO CW2.Users (UserName) VALUES (?)"
        try:
            cursor.execute(query, (name,))
            conn.commit()
            return jsonify({"message": "User added successfully"}), 201
        except Exception as e:
            print(f"Database error: {e}")
            return jsonify({"error": "Failed to add user."}), 500
        finally:
            cursor.close()
            conn.close()

    # Route: Get All Users
    @app.route("/users", methods=["GET"])
    def get_users():
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Failed to connect to the database."}), 500

        cursor = conn.cursor()
        query = "SELECT * FROM CW2.Users"

        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            users = [{"ID": row[0], "Name": row[1]} for row in rows]
            return jsonify(users)
        except Exception as e:
            print(f"Database error: {e}")
            return jsonify({"error": "Failed to fetch users."}), 500
        finally:
            cursor.close()
            conn.close()

    # Start Flask app
    if __name__ == "__main__":
        app.run(debug=True)

else:
    print("Authentication failed. Application will not start.")
