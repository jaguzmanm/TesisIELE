from PIL import Image
import numpy as np
from skimage import transform, img_as_ubyte
import matplotlib.pyplot as plt

img_gray = Image.open('testgrey2.png')

img_gray_array = np.array(img_gray)
print(img_gray_array.shape)


s_g84 = img_as_ubyte(transform.resize(img_gray_array, (150, 150)))

print(s_g84.shape)

plt.figure(figsize=(12,8))
plt.imshow(s_g84, cmap=plt.get_cmap('gray'))
plt.axis('off')
plt.show()