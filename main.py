import cv2
import argparse
import math
import progressbar
from pointillism import *

# parser = argparse.ArgumentParser(description='...')
# parser.add_argument('--palette-size', default=20, type=int, help="Number of colors of the base palette")
# parser.add_argument('--stroke-scale', default=0, type=int, help="Scale of the brush strokes (0 = automatic)")
# parser.add_argument('--gradient-smoothing-radius', default=0, type=int, help="Radius of the smooth filter applied to the gradient (0 = automatic)")
# parser.add_argument('--limit-image-size', default=0, type=int, help="Limit the image size (0 = no limits)")
# parser.add_argument('img_path', nargs='?', default="images/lake.jpg")
#
# args = parser.parse_args()
#
# res_path = args.img_path.rsplit(".", -1)[0] + "_drawing.jpg"
def point(mg,colp,l_im_s,strok_s,g_s_r):
    img = cv2.imread(mg)

    if l_im_s > 0:
        img = limit_size(img, l_im_s)

    if strok_s == 0:
        stroke_scale = int(math.ceil(max(img.shape) / 1000))
        print("Automatically chosen stroke scale: %d" % stroke_scale)
    else:
        stroke_scale = strok_s

    if g_s_r == 0:
        gradient_smoothing_radius = int(round(max(img.shape) / 50))
        print("Automatically chosen gradient smoothing radius: %d" % gradient_smoothing_radius)
    else:
        gradient_smoothing_radius = g_s_r

    # convert the image to grayscale to compute the gradient
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    print("Computing color palette...")
    palette = ColorPalette.from_image(img, colp)

    print("Extending color palette...",palette[0])
    palette = palette.extend([(0, 50, 0), (15, 30, 0), (-15, 30, 0)])
    print("Extended color palette...",palette[0])
    # display the color palette
    cv2.imshow("palette", palette.to_image())
    cv2.waitKey(200)

    print("Computing gradient...")
    gradient = VectorField.from_gradient(gray)

    print("Smoothing gradient...")
    gradient.smooth(gradient_smoothing_radius)

    print("Drawing image...")
    # create a "cartonized" version of the image to use as a base for the painting
    res = cv2.medianBlur(img, 11)
    # define a randomized grid of locations for the brush strokes
    grid = randomized_grid(img.shape[0], img.shape[1], scale=3)
    batch_size = 10000

    bar = progressbar.ProgressBar()
    for h in bar(range(0, len(grid), batch_size)):
        # get the pixel colors at each point of the grid
        pixels = np.array([img[x[0], x[1]] for x in grid[h:min(h + batch_size, len(grid))]])
        # precompute the probabilities for each color in the palette
        # lower values of k means more randomnes
        color_probabilities = compute_color_probabilities(pixels, palette, k=9)

        for i, (y, x) in enumerate(grid[h:min(h + batch_size, len(grid))]):
            color = color_select(color_probabilities[i], palette)
            angle = math.degrees(gradient.direction(y, x)) + 90
            length = int(round(stroke_scale + stroke_scale * math.sqrt(gradient.magnitude(y, x))))

            # draw the brush stroke
            cv2.ellipse(res, (x, y), (length, stroke_scale), angle, 0, 360, color, -1, cv2.LINE_AA)

    # cv2.imshow("res", limit_size(res, 1080))
    cl = [i for i in palette]
    return limit_size(res, 1080), cl
    #
    # cv2.imwrite(res_path, res)
    # cv2.waitKey(0)



#file

# image = cv2.imread(path)
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# edged = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) #cv2.Canny(gray, 50, 100)
# # OpenCV represents images in BGR order; however PIL represents
# # images in RGB order, so we need to swap the channels
# image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# # convert the images to PIL format...
# image = Image.fromarray(image)
# edged = Image.fromarray(edged)
# # ...and then to ImageTk format
# image = ImageTk.PhotoImage(image)
# edged = ImageTk.PhotoImage(edged)
# # if the panels are None, initialize them
# if panelA is None or panelB is None:
#     # the first panel will store our original image
#     panelA = Label(image=image)
#     panelA.image = image
#     panelA.pack(side="left", padx=10, pady=10)
#     # while the second panel will store the edge map
#     panelB = Label(image=edged)
#     panelB.image = edged
#     panelB.pack(side="right", padx=10, pady=10)
# # otherwise, update the image panels
# else:
#     # update the pannels
#     panelA.configure(image=image)
#     panelB.configure(image=edged)
#     panelA.image = image
#     panelB.image = edged
