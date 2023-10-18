
print("I m Priyanka");

# load envrioment variables from .env file
import os
import urllib.parse as up

# for database connection
import psycopg2

from dotenv import load_dotenv

# for flask framework
from flask import Flask, request, jsonify

# this command with read all env variables from .env file. 
load_dotenv()

app = Flask(__name__)

# DB connection
#url = os.getenv("DATABASE_URL")

connection = psycopg2.connect(database="csxecxjt", user="csxecxjt", password="qLeTm46aqyzZ91X7aZKDe6GzfeUKB01a", host="cornelius.db.elephantsql.com")
print("DB successfully connected...")

# Create a table
CREATE_ADDONS_TABLE = "CREATE TABLE IF NOT EXISTS addons(id SERIAL PRIMARY KEY, Window_Cleaning TEXT, Balcony_Cleaning TEXT, Garbage_Removal TEXT, Dusting TEXT)";
# using ON DELETE CASCADE means that if we delete a city, all its referenced addons will be deleted too.
CREATE_CITY_TABLE = "CREATE TABLE IF NOT EXISTS city(id SERIAL PRIMARY KEY, city_name TEXT, square_meter_price TEXT, available_addOns INTEGER, FOREIGN KEY(available_addOns) REFERENCES addons(id) ON DELETE CASCADE)";



# POPULATING DB
INSERT_AddOnsData = "INSERT INTO addons (Window_Cleaning, Balcony_Cleaning, Garbage_Removal, Dusting ) VALUES (%s, %s, %s, %s) RETURNING id";
INSERT_cityData = "INSERT INTO city (city_name, square_meter_price, available_addOns) VALUES (%s, %s, %s)";
DROP_CityTable = "DELETE FROM city";
DROP_AddonsTable = "DROP TABLE if exists addOns cascade";

# Execute db queries
with connection:
    with connection.cursor() as cursor:
        
        cursor = connection.cursor();
        cursor.execute("DROP TABLE if exists addons cascade")
        cursor.execute("DROP TABLE city")
        cursor.execute(CREATE_ADDONS_TABLE)
        cursor.execute(CREATE_CITY_TABLE)
        print("Table created sucessfully")
       
        print(cursor.execute(INSERT_AddOnsData, ("300", "550", "80", "280")));
        print("Entries in Table Addons created sucessfully")
        available_addons_id = cursor.fetchone()[0]
        cursor.execute(INSERT_cityData, ("Stockholm", "65", available_addons_id));
        cursor.execute(INSERT_cityData, ("Uppsala", "55", available_addons_id));
        print("Entries in Table city created sucessfully")


#status code errors
@app.errorhandler(404)
def handle_404(e):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def handle_500(e):
    return jsonify({'error': 'Internal Server Error'}), 500

@app.errorhandler(400)
def handle_400(e):
    return jsonify({'error': 'Bad Request, Please enter proper parameters'}), 400


@app.route("/add_ons/<cityname>", methods=["GET"])
def get_add_ons(cityname):
    if(cityname != "Uppsala" or cityname != "Stockholm"):
        return jsonify({"error": "City not found"}), 404

    cursor.execute("select available_addons from city where city_name = %s", (cityname, ))
    idaddon = cursor.fetchone()[0]
    cursor.execute("select * from addons where id = %s", (idaddon, ))
    row = cursor.fetchone()
    print("Row:", row)
    window_cleaning = row[1] 
    balcony_cleaning = row[2] 
    garbage_removal = row[3] 
    dusting = row[4] 
        
    if len(row) != 0:
        return jsonify({"message": f"These are availables addons.", "Window_Cleaning":window_cleaning, "Balcony_Cleaning":balcony_cleaning, 
            "Garbage_Removal": garbage_removal, "Dusting": dusting}), 201 

SELECT_per_square_meter_price = "SELECT square_meter_price FROM city where city_name=%s"
FETCH_SELECTED_ADDON = "SELECT * FROM addons"

@app.route("/quotation", methods=["POST"])
def calculate_quotation():
    data = request.get_json()
    city = data.get("city")
    total_square_meters_of_house = data.get("total_square_meters_of_house")
    selected_add_ons = data.get("selected_add_ons", [])   #type is list
    
    cursor.execute(SELECT_per_square_meter_price, (city,))    
    price_per_sq_meter = cursor.fetchone()[0]

    cursor.execute(FETCH_SELECTED_ADDON)
    row = cursor.fetchone()

    if int(total_square_meters_of_house) <= 0:
        return jsonify({"error": "Invalid square meters"}), 400

    column_names = [desc[0] for desc in cursor.description] 
    selected_add_ons = list(map(lambda x: x.lower(), selected_add_ons))
    
    index = []
    if (set(column_names) and set(selected_add_ons)):
        for addon in (set(column_names) & set(selected_add_ons)):
             index.append(column_names.index(addon))

    if len(index) == 0:
        return jsonify({"error": "Bad addons"}), 400
    
    total_price = 0;
    for j in index:
        total_price = total_price + int(row[j]) ;
    total_price = total_price + (int(price_per_sq_meter) * int(total_square_meters_of_house))

    return jsonify({"quotation of cleaning services in SEK" : total_price})


if __name__ == "__main__":
    app.run(debug=True)
