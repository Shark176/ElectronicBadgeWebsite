from website import create_app
from waitress import serve
from models.communicate_database import process_data
from flask_mqtt import Mqtt
import json

app = create_app()
app.config['MQTT_BROKER_URL'] = "eu1.cloud.thethings.network"  # URL của MQTT broker
app.config['MQTT_BROKER_PORT'] = 1883  # Cổng của MQTT broker
app.config['MQTT_USERNAME'] = "electronicbadgever2@ttn" # Tên đăng nhập, nếu có
app.config['MQTT_PASSWORD'] = "NNSXS.WBI2LPFUIQFQU46SN6HUYCAWG46HI5N4FEQSWFI.WY3E4UHPXZQMZ2HWBCPAIN4CQB7ZHPN4MABQAKKI425TWJAVXSCA"  # Mật khẩu, nếu có
app.config['MQTT_KEEPALIVE'] = 60  # Thời gian giữ kết nối
app.config['MQTT_TLS_ENABLED'] = False  # Kích hoạt TLS nếu cần
mqtt = Mqtt(app)
# Đăng ký topic và xử lý tin nhắn
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('#')

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    json_data = json.loads(message.payload.decode('utf-8'))
    print(json_data)
    try: 
        process_data(json_data)
    except:
        print("Can't process data")

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
    # app.run(debug=True,host='0.0.0.0',port='5000')