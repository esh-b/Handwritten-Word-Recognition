import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('image/mba.jpg',0)
r,c = img.shape
hist,bins = np.histogram(img.flatten(),256,[0,256])
cdf = hist.cumsum()
cdf_m = np.ma.masked_equal(cdf,0)
cdf_m = (cdf_m - cdf_m.min())*255/(cdf_m.max()-cdf_m.min())
cdf = np.ma.filled(cdf_m,0).astype('uint8')
img = cdf[img]
plt.imshow(img,cmap='gray')
ret,img = cv2.threshold(img,140,255,cv2.THRESH_BINARY_INV)

row = []
col = []
m=0
for i in range(r):
    if(m==1):
        row.append(i)
    for j in range(c):
        if(img[i][j]>30):
            m=0
            continue
        else:
            m=1
            break
final = [0]

for i in range(1,len(row)):
    if((row[i]-row[i-1])!=1):
        final.append(i-1)
        final.append(i)
    else:
        continue
img1 = img[row[final[2]]:row[final[3]],:]
img1 = img1.T
plt.imshow(img1,cmap='gray')
r,c =img1.shape
row = []
col = []
m=7
for i in range(r):
    if(m==1):
        col.append(i-1)
    for j in range(c):
        if(img1[i][j]>30):
            m=0
            continue
        else:
            m=1
            break
final1 = [0]

for i in range(1,len(col)):
    if((col[i]-col[i-1])>4):
        final1.append(i-1)
        final1.append(i)
    else:
        continue
img_f = img1[col[final1[6]]:col[final1[7]],:].T
#plt.imshow(img_f,cmap='gray')