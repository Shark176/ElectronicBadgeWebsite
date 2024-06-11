import psycopg2
import datetime
import pytz

def communicate_database(sql_query, parameters=None, fetch_type=None):
    try:
        # Kết nối tới database PostgreSQL
        connection = psycopg2.connect(
            "postgres://electronic_bagde_user:p4Aa667xidpAPw5dfkII8Ufuo6fuZapH@dpg-cpfj9kdds78s739e54v0-a.oregon-postgres.render.com/electronic_bagde"
        )
        # Tạo một đối tượng cursor để thực hiện các truy vấn
        cursor = connection.cursor()
        if parameters:
            cursor.execute(sql_query, parameters)
        else:
            cursor.execute(sql_query)

        if fetch_type == 'FETCH_ONE':
            result = cursor.fetchone()[0]
        elif fetch_type == 'FETCH_ALL':
            result = cursor.fetchall()
        else:
            result = None

        # Đóng kết nối
        connection.commit()
        connection.close()

        return result

    except psycopg2.Error as error:
        print("Lỗi kết nối database:", error)
        return None

def fetch_data(table1,table2,common):
    query = f"SELECT * FROM {table1},{table2} Where {table1}.{common} = {table2}.{common}"
    data = communicate_database(query,'FETCH_ALL')
    return data

def check_exists(table_name, field_name, field_value):
    query = "SELECT EXISTS(SELECT 1 FROM {} WHERE {} = %s)".format(table_name, field_name)
    exists = communicate_database(query, (field_value,), fetch_type='FETCH_ONE')
    return exists

def insert_data(table_name, fields, values):
    query = "INSERT INTO {} ({}) VALUES ({})".format(table_name, ', '.join(fields), ', '.join(['%s'] * len(fields)))  
    result = communicate_database(query, values)
    return result

def insert_location_report(deviceID, date, time, latitude, longitude, RSSI):
    query = """
    INSERT INTO LocationReports (DeviceID, DateID, Time, Latitude, Longitude, RSSI) 
    SELECT d.DeviceID, dt.DateID, %s, %s, %s, %s
    FROM Devices d, Dates dt 
    WHERE d.DeviceID = %s AND dt.Date = %s
    """  
    params = (time, latitude, longitude, RSSI, deviceID, date)
    communicate_database(query, params)

def process_data(data):
    deviceID = data["end_device_ids"]["device_id"]
    latitude = data["uplink_message"]["decoded_payload"]["lat"]
    longitude = data["uplink_message"]["decoded_payload"]["lon"]
    RSSI = data["uplink_message"]["rx_metadata"][0]["rssi"]
    time_string = data["uplink_message"]["rx_metadata"][0]["received_at"]
    # Loại bỏ phần thừa của micro giây
    time_string = time_string[:26]
    # Chuyển đổi thành đối tượng datetime
    datetime_object = datetime.datetime.strptime(time_string, "%Y-%m-%dT%H:%M:%S.%f")
    # Đặt múi giờ ban đầu là UTC
    datetime_object = datetime_object.replace(tzinfo=pytz.utc)
    # Chuyển đổi sang múi giờ mới
    new_timezone = pytz.timezone('Asia/Ho_Chi_Minh')  # Múi giờ Hồ Chí Minh
    converted_time = datetime_object.astimezone(new_timezone)
    date = converted_time.date()
    time = converted_time.time()
    if(latitude != 0):
        if (check_exists("Devices", "DeviceID", deviceID) == False):
            insert_data("Devices", ["DeviceID", "DeviceName", "DeviceDescription"], [deviceID, deviceID + "Name", deviceID + "Description"])
            print("Created a new device")
        if (check_exists("Dates", "Date", date) == False):
            insert_data("Dates", ["Date"], [date])
            print("Created a new date")
        insert_location_report(deviceID, date, time, latitude, longitude, RSSI)
    print("A new location report is created")
    print(deviceID)
    print(latitude)
    print(longitude)
    print(RSSI)

