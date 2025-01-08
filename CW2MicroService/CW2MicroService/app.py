from flask import Flask, request, jsonify
import pyodbc

# Flask App Setup
app = Flask(__name__)

# Database Connection Configuration
DB_CONFIG = {
    "driver": "{ODBC Driver 17 for SQL Server}",  # Adjust based on the installed ODBC driver
    "server": "localhost",
    "database": "COMP2001CW2",
    "username": "SA",
    "password": "C0mp2001!",
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

# Sample Route: Get All Trails
@app.route("/trails", methods=["GET"])
def get_trails():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Failed to connect to the database."}), 500

    cursor = conn.cursor()
    query = "SELECT * FROM CW2.Trails"  # Adjust table name/schema if needed

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

# Sample Route: Add a New Trail
@app.route("/trails", methods=["POST"])
def add_trail():
    data = request.get_json()
    trail_name = data.get("TrailName")
    trail_length = data.get("TrailLength")

    if not trail_name:
        return jsonify({"error": "TrailName is required"}), 400

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

if __name__ == "__main__":
    app.run(debug=True)
