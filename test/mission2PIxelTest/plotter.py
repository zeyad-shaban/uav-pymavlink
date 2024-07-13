import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def onclick(event):
    if event.xdata is not None and event.ydata is not None:
        x, y = int(event.xdata), int(event.ydata)
        rgb = img[y, x]
        print(f'RGB values at ({x}, {y}): {rgb}')

# Replace 'path_to_your_image' with the actual path to your image file
img_path = './a.JPG'
img = mpimg.imread(img_path)

fig, ax = plt.subplots()
ax.imshow(img)

fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()
