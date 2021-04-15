# Thu vien doc file xml
import xml.etree.ElementTree as ET
# Thu vien doc anh opencv
import cv2
import os
import random
from pathlib import Path
# Đường dẫn project
base_dir = os.path.dirname(os.path.realpath(__file__))
# Tạo tự động folder lưu kết quả lưu ảnh khuôn mặt
Path(base_dir + '/results/').mkdir(parents=True, exist_ok=True)

# Thu muc chua anh
image_dir = "images"
# Liet ke danh sach folder con trong folder chua anh
# VD: images
# ----------karik
# ----------khanh_vy
# ----------..... 
for per in os.listdir(image_dir):
    per_dir = os.path.join(image_dir, per) # Join duong dan thu muc anh
    for file in os.listdir(per_dir): # Liet ke danh sach file trong tung folder nguoi
        if 'xml' in file: # Chỉ lấy file xml
            # Lấy tên ảnh vì tên ảnh và tên xml giống nhau chỉ khác extension
            image_file = file[:-4] + '.jpg'
            # Join đường dẫn file xml đầy đủ
            xml_path = os.path.join(per_dir, file)
            # Join đường dẫn file ảnh đầy đủ
            image_path = os.path.join(per_dir, image_file)
            # Khởi tạo cây xml
            tree = ET.parse(xml_path)
            root = tree.getroot()
            # Liệt kê tất cả object trong file xml
            for obj in root.findall('object'):
                # Liệt kê tất cả giá trị trong trường bnbbox trong xml
                for value in obj.findall('bndbox'):
                    # Lấy giá trị từng trường xmin, ymin, xmax, ymax
                    xmin = int(value.find('xmin').text)
                    xmax = int(value.find('xmax').text)
                    ymin = int(value.find('ymin').text)
                    ymax = int(value.find('ymax').text)
            # Đọc ảnh từ opencv
            image = cv2.imread(image_path)
            # Cắt ảnh theo khung xmin, ymin, xmax, ymax
            crop_face = image[ymin:ymax, xmin:xmax, :]
            # Resize khuôn mặt về tỉ lệ 256x256
            crop_face = cv2.resize(crop_face, (256,256))
            # Lưu khuôn mặt theo tên random
            cv2.imwrite('results/' + str(random.random()) + '.jpg', crop_face)
            # Vẽ đường bao khuôn mặt vào ảnh gốc, nếu cần visualize
            # image = cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (255,0,0), 3)
            
            # # Visualize ảnh cắt và ảnh gốc
            # cv2.imshow("Face", crop_face)
            # cv2.imshow("Origin", image)
            # # Nhấn q để chuyển sang ảnh khác
            # cv2.waitKey(0)