# CleaningService

#Commands to be exceuted in a Sequence

# Create virtual enviroment (write in terminal)
python -m venv ./venv

#Activate virtual envrioment
./venv/Scripts/activate

#Run requirements.txt
pip install -r requirements.txt 

# Run file
python app.py

# Using Postman and GET execute
http://127.0.0.1:5000/add_ons/Uppsala   <br/>
http://127.0.0.1:5000/add_ons/Stockholm

# Using Postman and POST execute with payload json
http://127.0.0.1:5000/quotation  <br/>
1) <br/>
{ <br/>
    "city": "Stockholm", <br/>
    "total_square_meters_of_house": 100, <br/>
    "selected_add_ons": ["Window_cleaning", "Balcony_cleaning", "Dusting"] <br/>
} <br/>
2) <br/>
{
    "city": "Stockholm", <br/>
    "total_square_meters_of_house": 00, <br/>
    "selected_add_ons": ["Window_cleaning", "Balcony_cleaning", "Dusting"] <br/>
} <br/>
3) <br/>
{
    "city": "Stockholm", <br/>
    "total_square_meters_of_house": 00, <br/>
    "selected_add_ons": ["abc"] <br/>
} <br/>


