from flask import Blueprint, render_template, request, jsonify
from models.fetchData import fetch_data


views = Blueprint('view', __name__)

@views.route('/submit', methods=['GET'])
def submit():
    date = request.args.get('date')
    deviceID = request.args.get('deviceID')
    
    if date is None or deviceID is None:
        return jsonify({
            "status": "error",
            "message": "Missing date or deviceID parameters"
        }), 400
    print(f"Received data - Date: {date}, Device ID: {deviceID}")
    try:
        received_data = fetch_data(date, deviceID)
        print(received_data)
    except:
        received_data = {
                "status": "error",
                "message": "Data Error",
                "data": {"steps": [],"result": {},},
                "author": "nguyenhoangkhanhduy030903@gmail.com",
                }
    return received_data

    
    
    # return jsonify({"message": "Data received successfully!"})

@views.route('/')
def index():
    return render_template('index.html')
