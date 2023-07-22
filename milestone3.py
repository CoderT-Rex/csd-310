import mysql.connector

# Establish a connection to the MySQL database
db = mysql.connector.connect(
    host='localhost',
    user='outland_user',
    password='adventures',
    database='outland_adventures'
)

# Create a cursor to execute SQL queries
cursor = db.cursor()

# Query to check if any location has a downward trend in bookings
query1 = '''
SELECT location_name, trip_id, start_date, end_date, number_of_bookings, season
FROM Trip
JOIN Location ON Trip.location_id = Location.location_id
ORDER BY location_name, start_date;
'''

# Query to check if there are inventory items over five years old
query2 = '''
SELECT equipment_name, purchase_date
FROM Equipment
WHERE purchase_date <= DATE_SUB(NOW(), INTERVAL 5 YEAR);
'''

# Query to retrieve the amount of equipment purchased by customers
query3 = '''
SELECT COUNT(*) AS equipment_purchases
FROM Customer
WHERE equipment_id IS NOT NULL;
'''

# Execute the queries

cursor.execute(query1)
trips = cursor.fetchall()

cursor.execute(query2)
old_inventory = cursor.fetchall()

cursor.execute(query3)
equipment_purchases = cursor.fetchone()[0]

# Close the cursor and the database connection
cursor.close()
db.close()

# Display the results

print("\nTrends in bookings by location:")
current_country = None
previous_end_date = None
previous_num_bookings = None

for trip in trips:
    location_name, trip_id, start_date, end_date, num_bookings, season = trip

    print(f"{location_name} ({season}) has {num_bookings} bookings")
    if location_name != current_country:
        current_country = location_name
        previous_start_date = start_date
        previous_num_bookings = num_bookings
    else:
        if num_bookings < previous_num_bookings:
            difference = num_bookings - previous_num_bookings
            percentage_change = abs(difference / previous_num_bookings) * 100
            print(f"{current_country} saw a {percentage_change:.2f}% decrease in bookings from {previous_start_date} to {start_date}.")
        if num_bookings > previous_num_bookings:
            difference = previous_num_bookings - num_bookings
            percentage_change = abs(difference / num_bookings) * 100
            print(f"{current_country} saw a {percentage_change:.2f}% increase in bookings from {previous_start_date} to {start_date}.")
    previous_start_date = start_date
    previous_num_bookings = num_bookings



print("\nInventory items over five years old:")
for inventory in old_inventory:
    equipment_name, purchase_date = inventory
    print(f"{equipment_name}: Purchased on {purchase_date}")

print("\nAmount of equipment purchased by customers:", equipment_purchases)
