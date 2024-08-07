import io
import time
import picamera
import pygsheets

from PIL import Image
from pyzbar.pyzbar import decode

client = pygsheets.authorize(service_account_file="/home/pi/Desktop/DIL_18/restaurantkv-1ff2f0101143.json")
def get_data():
    spreadsheet = client.open("kvnewrestaurant")
    worksheet = spreadsheet.worksheet("title","Sheet2")
    data_range = worksheet.get_all_values(include_tailing_empty_rows=False,include_tailing_empty=True)
    data = data_range[1:]
    print(data)
def update_table_status():
    spreadsheet = client.open("kvnewrestaurant")
    worksheet = spreadsheet.worksheet("title","Sheet2")
    worksheet.update_value(f'B{2}','0')
def detect_qr_code(image):
    decoded_objects = decode(image)
    for obj in decoded_objects:
        print("Data:", obj.data.decode())
        print("Type:", obj.type)
        return obj.data.decode()
        
    return len(decoded_objects) > 0
def main():
    data = get_data()
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.start_preview()
        time.sleep(2)
        while True:
            stream = io.BytesIO()
            camera.capture(stream, format='jpeg')
            stream.seek(0)
            image = Image.open(stream)
            qr_code_detected = detect_qr_code(image)
            if qr_code_detected:
                camera.stop_preview()
            if qr_code_detected == "WIPER":
                update_table_status()
                print("Table status updated to 0")
            
            
if __name__ == "__main__":
    main()

