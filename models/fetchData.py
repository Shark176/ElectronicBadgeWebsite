from models.communicate_database import communicate_database
import json

def fetch_data(date, device_id):
    query = '''
        SELECT 
            lr.ReportID,
            d.DeviceName,
            lr.Time,
            lr.Latitude,
            lr.Longitude,
            lr.RSSI
        FROM 
            LocationReports lr
        INNER JOIN 
            Devices d ON lr.DeviceID = d.DeviceID
        INNER JOIN 
            Dates dt ON lr.DateID = dt.DateID
        WHERE 
            dt.Date = %s AND lr.DeviceID = %s;
        '''
    data = communicate_database(query,(date, device_id),'FETCH_ALL')
    json_data = convert_to_json(data, date, device_id)
    return json_data

def convert_to_json(data, date, device_id):
    markers = []
    for entry in data:
        marker = {
            "ReportID": entry[0],
            "Device_Name": entry[1],
            "Time_Recieve": entry[2].strftime('%H:%M:%S.%f')[:-3],  # Chuyển đổi thời gian thành chuỗi
            "Latitude": entry[3],
            "Longitude": entry[4],
            "Signal_Strength": entry[5]
        }
        markers.append(marker)

    # Tạo dictionary tổng thể
    output_data = {
        "date": date,  # Bạn có thể thay đổi ngày nếu cần thiết
        "device_id": device_id,
        "markers": markers
    }

    # Chuyển đổi thành JSON
    json_data = json.dumps(output_data, indent=4, ensure_ascii=False)
    return json_data

    