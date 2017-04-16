import cv2
import numpy as np
import thinning
from PIL import Image

#Skeletonize the image using opencv
def skeletonize(img):
	size = np.size(img)
	skel = np.zeros(img.shape,np.uint8)
	element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3, 3))
	done = False
	 
	while(not done):
	    eroded = cv2.erode(img, element)
	    temp = cv2.dilate(eroded, element)
	    temp = cv2.subtract(img, temp)
	    skel = cv2.bitwise_or(skel, temp)
	    img = eroded.copy()
	 
	    zeros = size - cv2.countNonZero(img)
	    if zeros == size:
	        done = True
	return skel

#Group nearby columns into a list, thereby producing list of list
def groupCols(arr):
	groupedList = []
	tempLst = []

	#For every element in the original groupedList
	for i in range(len(arr)):

		#Incase the present index is discontinuous from previous indices, then len(templst) will be zero
		if(len(tempLst) == 0):
			tempLst.append(arr[i])
			continue

		#Incase the present column is the next one of the previous column, append it to the tempLst
		if(arr[i - 1] + 1 == arr[i]):
			tempLst.append(arr[i])
		#Incase the present column is discontinuous from the previous columns, put the existing tempLst into groupedList and add the present element
		else:
			groupedList.append(tempLst)
			tempLst = []
			tempLst.append(arr[i])

		if(i == len(arr) - 1):
			groupedList.append(tempLst)
	return groupedList

img = cv2.imread("test2.jpg", 0)
img = cv2.fastNlMeansDenoising(img, h=20)
img = cv2.threshold(img, 160, 255, cv2.THRESH_BINARY_INV)[1]

#unique, counts = np.unique(img, return_counts=True)
#print(dict(zip(unique, counts)))

img = thinning.guo_hall_thinning(img.copy())

#img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)


zerosLst = []
onesLst = []
for i in range(img.shape[1]):
	if(np.sum(img[:, i]) == 0):
		zerosLst.append(i)
	elif(np.sum(img[:, i]) == 255):
		onesLst.append(i)

zerosLst = groupCols(zerosLst)
onesLst = groupCols(onesLst)
finalCols = []
for col in zerosLst:
	if(len(col) < 7):
		continue
	middleElem = col[int(len(col) / 2)]
	finalCols.append(middleElem)

for col in onesLst:
	if(len(col) < 7):
		continue
	middleElem = col[int(len(col) / 2)]
	finalCols.append(middleElem)

for elem in finalCols:
	img[:, elem] = 255
print(finalCols)

#img = np.delete(img, zerosLst, axis=1)
#print(img.shape)

cv2.imshow("skel", img)
cv2.waitKey(0)
cv2.destroyAllWindows()