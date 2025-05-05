import cv2
import math
import csv
from pyzbar.pyzbar import decode
from ultralytics import YOLO
import mysql.connector

# MySQL connection
conn = mysql.connector.connect(
    host="192.168.3.87",  
    user="root",
    password="1234",
    database="warehouse"
)

cursor = conn.cursor()



def initialize_csv():
    with open("Database.csv", mode='w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(["Data", "Detection Count"])

initialize_csv()



class BarcodeDetector:
    def __init__(self):
        self.saved_data = set()
        self.detection_count = 0

    def decode_barcodes(self, img, roi):
        barcodes = decode(roi)
        for barcode in barcodes:
            data = barcode.data.decode('utf-8')
            barcode_type = barcode.type
            (x, y, w, h) = barcode.rect

            # Draw a rectangle around the barcode
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text = f"{data} ({barcode_type})"
            cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            self.get_product_info(data)
            self.update_asset_status(data)

               
            
            # Save unique barcode data
            if data and data not in self.saved_data:
                print("Data found:", data)
                self.saved_data.add(data)
                self.detection_count += 1
                with open("Database.csv", mode='a') as csvfile:
                    csvfileWriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
                    csvfileWriter.writerow([data, self.detection_count])
    
    def update_asset_status(self, barcode_id):
        query = "SELECT * FROM identification WHERE IdentifierValue = %s"
        cursor.execute(query, (barcode_id,))
        resultset = cursor.fetchall()
        for row in resultset:
            asset_id = row[1]
            print("AssetID:", asset_id)
        
        if resultset:
            query = "UPDATE asset SET AssetFound = 1 WHERE AssetID = %s"
            cursor.execute(query, (asset_id,))            
            conn.commit()
            return True
        return False

    def get_product_info(self, barcode_id):
        query = "SELECT * FROM identification WHERE IdentifierValue = %s"
        cursor.execute(query, (barcode_id,))
        resultset = cursor.fetchall()
        
        if resultset:
            asset_id = resultset[0][1]
            query = "SELECT * FROM asset WHERE AssetID = %s"
            cursor.execute(query, (asset_id,))
            asset_info = cursor.fetchone()  
            product_id = asset_info[1]
            assetLocation = asset_info[2]
            assetCondition = asset_info[3]
            dateadded = asset_info[4]
            assetDispatched = asset_info[6]
            print(assetLocation)

            query = "SELECT * FROM product WHERE ProductID = %s"
            cursor.execute(query, (product_id,))
            product_info = cursor.fetchall()
            for row in product_info:
                productName = row[2]
                productCategory = row[3]
                productPrice = row[5]
                print(productName)
                print(productPrice)
            return product_info
        return None

cap = cv2.VideoCapture(0)
cap.set(3, 720)
cap.set(4, 720)

import cv2
import csv
import math
from ultralytics import YOLO

class QRCodeDetector:
    def __init__(self):
        self.saved_data = set()
        self.detection_count = 0

    def decode_qrcodes(self, img, roi):
        detector = cv2.QRCodeDetector()
        data, bbox, _ = detector.detectAndDecode(roi)

        print(f"Decoded Data: {data}")  # Debugging output
        if bbox is not None:
            print("Bounding box detected for QR code.")
        else:
            print("No bounding box detected.")

        if data:
            print(f"QR Code Data: {data}")
        else:
            print("No data found in QR code.")

        if bbox is not None:
            bbox = bbox.astype(int)
            for i in range(len(bbox)):
                start_point = tuple(bbox[i][0])
                end_point = tuple(bbox[(i + 1) % len(bbox)][0])
                cv2.line(img, start_point, end_point, color=(255, 0, 0), thickness=2)
            cv2.putText(img, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 250, 120), 2)

            # If QR code data is new, process it and save to the CSV
            if data and data not in self.saved_data:
                print("Data found:", data)
                self.saved_data.add(data)
                self.detection_count += 1
                with open("Database.csv", mode='a') as csvfile:
                    csvfileWriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
                    csvfileWriter.writerow([data, self.detection_count])

                # Call the SQL functions
                product_info = self.get_product_info(data)
                self.update_asset_status(data)

    def update_asset_status(self, qrcode_id):
        query = "SELECT * FROM identification WHERE IdentifierValue = %s"
        cursor.execute(query, (qrcode_id,))
        resultset = cursor.fetchall()
        for row in resultset:
            asset_id = row[1]
            print("AssetID:", asset_id)

        if resultset:
            query = "UPDATE asset SET AssetFound = 1 WHERE AssetID = %s"
            cursor.execute(query, (asset_id,))            
            conn.commit()
            return True
        return False

    def get_product_info(self, qrcode_id):
        query = "SELECT * FROM identification WHERE IdentifierValue = %s"
        cursor.execute(query, (qrcode_id,))
        resultset = cursor.fetchall()
        
        if resultset:
            asset_id = resultset[0][1]
            query = "SELECT * FROM asset WHERE AssetID = %s"
            cursor.execute(query, (asset_id,))
            asset_info = cursor.fetchone()  
            product_id = asset_info[1]
            assetLocation = asset_info[2]
            assetCondition = asset_info[3]
            dateadded = asset_info[4]
            assetDispatched = asset_info[6]
            print(assetLocation)

            query = "SELECT * FROM product WHERE ProductID = %s"
            cursor.execute(query, (product_id,))
            product_info = cursor.fetchall()
            for row in product_info:
                productName = row[2]
                productCategory = row[3]
                productPrice = row[5]
                print(productName)
                print(productPrice)
            return product_info
        return None

