import psycopg2

def show_table(cursor,table):
    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()
    # In dữ liệu từ các dòng kết quả
    for row in rows:
        print(row)
def drop_table(cursor,table):
    cursor.execute((f"Drop table {table}"))

def concat_table(cursor,table1,table2,common):
    cursor.execute(f"SELECT * FROM {table1},{table2} Where {table1}.{common} = {table2}.{common}")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
        
try:
    # Kết nối đến PostgreSQL

    connection = psycopg2.connect(
        "postgres://electronic_bagde_user:p4Aa667xidpAPw5dfkII8Ufuo6fuZapH@dpg-cpfj9kdds78s739e54v0-a.oregon-postgres.render.com/electronic_bagde"
    )
    # Tạo một đối tượng cursor để thực hiện các truy vấn
    cursor = connection.cursor()

    devices =  '''CREATE TABLE Devices (
        DeviceID SERIAL UNIQUE,
        DeviceName varchar(255),
        DeviceDescription text,
        PRIMARY KEY (DeviceID)
        );'''
    dates = '''CREATE TABLE Dates (
        DateID SERIAL UNIQUE,
        Date DATE NOT NULL,
        PRIMARY KEY (DateID)
        );'''
    
    locationReports = '''CREATE TABLE LocationReports (
        ReportID SERIAL UNIQUE,
        DeviceID SERIAL,
        DateID SERIAL,
        Time TIME,
        Latitude FLOAT(48),
        Longitude FLOAT(48),
        RSSI INT,
        PRIMARY KEY (ReportID),
        FOREIGN KEY (DeviceID) REFERENCES Devices(DeviceID),
        FOREIGN KEY (DateID) REFERENCES Dates(DateID)
        );'''
    

    insert_devices = '''
        INSERT INTO Devices (DeviceName, DeviceDescription) VALUES
        ('Duy Device', 'Is use in school'),
        ('Kiệt Device', 'Is use in company'),
        ('Tuấn Device', 'Is use in tour');
        '''
    
    insert_dates = '''
        INSERT INTO Dates (Date) VALUES
        ('2024-6-4'),
        ('2024-6-5'),
        ('2024-6-7');
        '''
    
    insert_location_reports = '''
        INSERT INTO LocationReports (DeviceID, DateID, Time, Latitude, Longitude, RSSI) VALUES
        ('1', '7','09:00:45', 10.86785105096807, 106.79410036172382, -100),
        ('1', '7','10:00:45', 10.96785105096807, 106.89410036172382, -115),
        ('1', '8','12:00:45', 10.56785105096807, 106.69410036172382, -120),
        ('2', '7','19:00:45', 10.86785105096807, 106.79410036172382, -96),
        ('2', '9','20:00:45', 10.99785105096807, 106.89710036172382, -118),
        ('2', '9','22:00:45', 10.58785105096807, 106.60410036172382, -90),
        ('1', '7','00:00:45', 10.46785105096807, 106.79410036172382, -80),
        ('1', '8','17:00:45', 10.56785105096807, 106.85410036172382, -86),
        ('1', '9','18:00:45', 10.06785105096807, 106.63410036172382, -97);
        '''
    
    check_exists = "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'TinhThanh');"

    show_table(cursor,"LocationReports")
    # show_table(cursor,"TaiKhoan")
    # drop_table(cursor,"Dates")
    # concat_table(cursor,"Devices","LocationReports","DeviceID")
    
    # cursor.execute(insert_location_reports)
    cursor.execute('''DELETE FROM LocationReports
WHERE Latitude = 0 AND Longitude = 0;
''')
    connection.commit()

    # result = cursor.fetchone()[0]
    # # Lấy tất cả các dòng kết quả
    # print(result)

    # Đóng cursor và kết nối
    cursor.close()
    connection.close()

except (Exception, psycopg2.Error) as error:
    print("Lỗi khi kết nối đến PostgreSQL:", error)
