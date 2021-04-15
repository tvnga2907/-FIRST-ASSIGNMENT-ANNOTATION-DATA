from cv2 import data
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
from PIL import Image

data_X = []
image_names = []
# Đọc ảnh
for image_file in os.listdir('results'):
    image = cv2.imread(os.path.join('results', image_file))
    # Lưu đường dẫn file ảnh
    image_names.append(os.path.join('results', image_file))
    # Chuyển ảnh về 1 chiều, 1D
    image_1d = image.copy().reshape(-1)
    data_X.append(image_1d)

data_X = np.array(data_X) # Chuyển danh sách chứa ảnh về dạng numpy

# Khởi tạo TSNE mặc định
tsne = TSNE()
reduced = tsne.fit_transform(data_X)
reduced_transformed = reduced - np.min(reduced, axis=0)
reduced_transformed /= np.max(reduced_transformed, axis=0)
image_xindex_sorted = np.argsort(np.sum(reduced_transformed, axis=1))


# draw all images in a merged image
no_of_images = len(image_names)
image_width = 256
ellipside = True

merged_width = int(np.ceil(np.sqrt(no_of_images))*image_width)
merged_image = np.zeros((merged_width, merged_width, 3), dtype='uint8')

for counter, index in enumerate(image_xindex_sorted):
    # set location
    if ellipside:
        a = np.ceil(reduced_transformed[counter, 0] * (merged_width-image_width-1)+1)
        b = np.ceil(reduced_transformed[counter, 1] * (merged_width-image_width-1)+1)
        a = int(a - np.mod(a-1,image_width) + 1)
        b = int(b - np.mod(b-1,image_width) + 1)
        if merged_image[a,b,0] != 0:
            continue
        image_address = image_names[counter]
        img = np.asarray(Image.open(image_address).resize((image_width, image_width)))
        merged_image[a:a+image_width, b:b+image_width,:] = img[:,:,:3]
    else:
        b = int(np.mod(counter, np.sqrt(no_of_images)))
        a = int(np.mod(counter//np.sqrt(no_of_images), np.sqrt(no_of_images)))
        image_address = image_names[index]
        img = np.asarray(Image.open(image_address).resize((image_width, image_width)))
        merged_image[a*image_width:(a+1)*image_width, b*image_width:(b+1)*image_width,:] = img[:,:,:3]


merged_image = Image.fromarray(merged_image)

merged_image.save('tsne_results.png')

plt.imshow(merged_image)
plt.show()



