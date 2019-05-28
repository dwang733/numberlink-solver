import cv2.cv2 as cv
import numpy as np
import statistics

# img = cv.imread('puzzles/regular_5x5_01.png')
img = cv.imread('puzzles/mania_15x15_01.png')
img = img[131:-131, 7:-7]  # Crop image to puzzle

# Threshold puzzle to try to enhance grid lines
gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
_, gray_img = cv.threshold(gray_img, 60, 255, cv.THRESH_TOZERO)
_, gray_img = cv.threshold(gray_img, 80, 255, cv.THRESH_TOZERO_INV)
# cv.imshow('gray image', gray_img)
# cv.waitKey(0)
# cv.destroyAllWindows()

# Detect vertical grid lines
lines = cv.HoughLines(gray_img, 1, np.pi / 180, 200, max_theta=0.01)
lines.sort(axis=0)
line_diff = []
for line1, line2 in zip(lines[:-1], lines[1:]):
    coord1, coord2 = line1[0][0], line2[0][0]
    line_diff.append(coord2 - coord1)

cell_size = statistics.median(line_diff)  # Estimated cell size
n = int(round(img.shape[0] / cell_size))  # Size of board
cell_size = img.shape[0] / n  # Use n to get exact cell size
print(cell_size)
print(n)

colors = set()
for i in range(n):
    x = int(round(cell_size / 2 + i * cell_size))
    for j in range(n):
        y = int(round(cell_size / 2 + j * cell_size))
        unique_color = True
        image_color = tuple(img[x, y])
        for color in colors:
            colors_similar = True
            for channel, image_channel in zip(color, image_color):
                if abs(int(channel) - int(image_channel)) > 10:
                    colors_similar = False
                    break
            if colors_similar:
                unique_color = False
                break
        if unique_color:
            cv.circle(img, (y, x), 2, (0, 0, 0), 3)
            colors.add(image_color)

print(len(colors))
print(colors)

for line in lines:
    rho,theta = line[0]
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))
    cv.line(img,(x1,y1),(x2,y2),(0,0,255),2)
cv.imshow('detected lines', img)
cv.waitKey(0)
cv.destroyAllWindows()

# circles = cv.HoughCircles(gray_img, cv.HOUGH_GRADIENT, dp=1, minDist=12, param1=25, param2=25, minRadius=3, maxRadius=25)
# circles = np.uint16(np.around(circles))[0]
# print(circles)
# for i in circles:
#     # draw the outer circle
#     cv.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
#     # draw the center of the circle
#     cv.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)
#
# cv.imshow('detected circles', img)
# cv.waitKey(0)
# cv.destroyAllWindows()


