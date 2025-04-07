import os
import subprocess
import psycopg2
from psycopg2 import sql
from datetime import datetime

# PostgreSQL connection details
DB_NAME = "system_monitor"
DB_USER = "postgres"
DB_PASSWORD = "postgres"  # Replace with your actual password
DB_HOST = "65.0.171.207"   
DB_PORT = "5435"

# Function to fetch disk usage details
def get_disk_usage():
    result = subprocess.run(["df", "-h"], capture_output=True, text=True)
    data = []
    for line in result.stdout.strip().split('\n')[1:]:
        parts = line.split()
        if len(parts) >= 6:
            # Ensure % is removed from the usage_percent value
            parts[4] = parts[4].strip('%')
            data.append(parts)
    return data

# Function to insert data into PostgreSQL
def insert_data_to_postgres(data):
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
        )
        cursor = conn.cursor()

        for entry in data:
            cursor.execute(
                sql.SQL(
                    "INSERT INTO disk_usage (filesystem, size, used, available, usage_percent, mount_point) "
                    "VALUES (%s, %s, %s, %s, %s, %s)"
                ),
                entry
            )

        conn.commit()
        print("✅ Disk usage data inserted successfully!")
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    disk_data = get_disk_usage()
    insert_data_to_postgres(disk_data)

