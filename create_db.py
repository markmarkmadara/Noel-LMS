import sqlite3

# Connect to the database
conn = sqlite3.connect("database.db")
c = conn.cursor()

# Execute a SELECT query
c.execute("SELECT is_admin FROM users")

# Fetch the results
result = c.fetchall()

# Print the column values
for row in result:
    column_value = row[0]
    print(column_value)

# Close the database connection
conn.close()
