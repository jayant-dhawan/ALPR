from skimage.filters import threshold_otsu
from skimage import util
from skimage import measure
from skimage.measure import regionprops
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import cv2


# def DetectPlate(img)
img = cv2.imread("images/car.jpg", 0)  # Reading image
img = img * 255

fig, (ax1, ax2) = plt.subplots(1, 2)
ax1.imshow(img, cmap="gray")

threshold_value = threshold_otsu(img)  # using OTSU Thresholding
binary_img = img > threshold_value

binary_img = util.invert(binary_img)

ax2.imshow(binary_img, cmap="gray")
# plt.show()

label_image = measure.label(binary_img)

# Aspect Ratios of Longer Plates
plate_dimensions = (0.03*label_image.shape[0], 0.08*label_image.shape[0],
                    0.15*label_image.shape[1], 0.3*label_image.shape[1])

# Aspect Ratios of Shorter Plates
plate_dimensions2 = (0.08*label_image.shape[0], 0.2*label_image.shape[0],
                     0.15*label_image.shape[1], 0.4*label_image.shape[1])

min_height, max_height, min_width, max_width = plate_dimensions
plate_objects_cordinates = []
plate_like_objects = []

fig, (ax1) = plt.subplots(1)
ax1.imshow(img, cmap="gray")
flag = 0

for region in regionprops(label_image):
    if region.area < 50:
        # if the region is so small maybe it's not a license plate
        continue

    # the bounding box coordinates
    min_row, min_col, max_row, max_col = region.bbox
    region_height = max_row - min_row
    region_width = max_col - min_col

    # ensuring that the region identified satisfies the condition of a
    # typical license plate
    if region_height >= min_height and region_height <= max_height \
            and region_width >= min_width and region_width <= max_width \
            and region_width > region_height:
        flag = 1
        plate_like_objects.append(binary_img[min_row:max_row,
                                  min_col:max_col])
        plate_objects_cordinates.append((min_row, min_col,
                                        max_row, max_col))
        rectBorder = patches.Rectangle((min_col, min_row), max_col - min_col,
                                       max_row - min_row, edgecolor="red",
                                       linewidth=2, fill=False)
        ax1.add_patch(rectBorder)

if (flag == 0):
    min_height, max_height, min_width, max_width = plate_dimensions2
    plate_objects_cordinates = []
    plate_like_objects = []

    fig, (ax1) = plt.subplots(1)
    ax1.imshow(img, cmap="gray")

    # regionprops creates a list of properties of all the labelled regions
    for region in regionprops(label_image):
        if region.area < 50:
            # if the region is so small then maybe it's not a license plate
            continue

        # the bounding box coordinates
        min_row, min_col, max_row, max_col = region.bbox

        region_height = max_row - min_row
        region_width = max_col - min_col

        # ensuring that the region identified satisfies the condition of a
        # typical license plate
        if (region_height >= min_height and region_height <= max_height
            and region_width >= min_width and
            region_width <= max_width
                and region_width > region_height):
            plate_like_objects.append(binary_img[min_row:max_row,
                                      min_col:max_col])
            plate_objects_cordinates.append((min_row, min_col,
                                            max_row, max_col))
            rectBorder = patches.Rectangle((min_col, min_row), max_col -
                                           min_col, max_row - min_row,
                                           edgecolor="red",
                                           linewidth=2, fill=False)
            ax1.add_patch(rectBorder)
            # let's draw a red rectangle over those regions
ax1.imshow(img, cmap="gray")
# print("Printing")
plt.show()


# DetectPlate()
