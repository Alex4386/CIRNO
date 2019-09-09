## The ScreenCapture Stuff
import matplotlib.pyplot as plt
import platform
import time
import numpy as np

if platform.system() == "windows" or platform.system() == "Darwin":
    from PIL import ImageGrab
elif platform.system() == "Linux":
    import gi
    from gi.repository import Gdk
    from gi.repository import GdkPixbuf
    gi.require_version('Gtk','3.0')

    ## STACK OVERFLOW CODE

    def array_from_pixbuf(p):
        " convert from GdkPixbuf to numpy array"
        w,h,c,r=(p.get_width(), p.get_height(), p.get_n_channels(), p.get_rowstride())
        assert p.get_colorspace() == GdkPixbuf.Colorspace.RGB
        assert p.get_bits_per_sample() == 8
        if  p.get_has_alpha():
            assert c == 4
        else:
            assert c == 3
        assert r >= w * c
        a=np.frombuffer(p.get_pixels(),dtype=np.uint8)
        if a.shape[0] == w*c*h:
            return a.reshape( (h, w, c) )
        else:
            b=np.zeros((h,w*c),'uint8')
            for j in range(h):
                b[j,:]=a[r*j:r*j+w*c]
            return b.reshape( (h, w, c) )

    def pixbuf_from_array(z):
        " convert from np array to GdkPixbuf "
        z=z.astype('uint8')
        h,w,c=z.shape
        assert c == 3 or c == 4
        return GdkPixbuf.Pixbuf.new_from_data(z.tobytes(),  GdkPixbuf.Colorspace.RGB, c==4, 8, w, h, w*c, None, None)


    ## STACK OVERFLOW CODE


else:
    print("Undefined System")


## Image Processing Stuff
import cv2

## The Screen Capture Stuff
window = None
img = None
scale = 1

## Frame Count
currentFrame = 0

# Basically gets Window Handle and save at img
def getImageZone():
    #print("start get image zone")
    global window
    global img
    global scale
    if platform.system() == "Windows":
        #print("platform checked, its windows")
        import win32gui
        rect = win32gui.GetWindowRect(window)
        #print("rectangle checked")
        #print(rect)
        #print("Patching with scale")
        #print((rect[0]*scale, rect[1]*scale, rect[2]*scale, rect[3]*scale))
        #print("ImageGrab call")
        img = ImageGrab.grab(bbox=(rect[0]*scale, rect[1]*scale, rect[2]*scale, rect[3]*scale))
        #print("finished get image zone")
        return img
    elif platform.system() == "Linux":
        pb = Gdk.pixbuf_get_from_window(window, window.get_position().x, window.get_position().y-40, window.get_width(), window.get_height());
        img = array_from_pixbuf(pb)
        return img
    else:
        print("So, You are not running on Windows, Too bad. Manually write getImage")
        print("If you can get coordinates in macOS, Please feel free to PR.")
        print("Because I have no idea to fix this. and I am also the Macbook user.")
        return

# Basically Get Window Handle
def getWindowHandle():
    print("called getWindowHandle")
    global window
    if platform.system() == "Windows":
        import win32gui
        windowHandle = win32gui.GetForegroundWindow()
        if windowHandle == None:
            print("FUCK")
            exit()
        window = windowHandle
        print("finished window handle")
        return
    elif platform.system() == "Linux":
        print("Fallback to GDK Method")

        window = Gdk.get_default_root_window().get_screen().get_active_window()

    else:
        print("So, You are not running on Windows, Too bad. Manually write getImage")
        print("If you can get coordinates in macOS, Please feel free to PR.")
        print("Because I have no idea to fix this. and I am also the Macbook user.")
        return

# Test Logic for Get Window handle
print("Please Enter your GUI Scale")
scale = float(input("Scale: "))
print("Please Launch Desired touhou project version")
input("Press Enter, then it will capture the Active Window Automatically after 5 seconds ")
time.sleep(5)
getWindowHandle()
print("Got: Window Handle")
print(window)
getImageZone()
print("Matplotlib export trial:")
plt.imshow(img)
plt.show()
print("Test Complete")

## Image Process for ROI
def getPOI(img):
    # TH12
    poi_game = np.float32(img)[int(37 * scale):int(477 * scale), int(40 * scale):int((418 * scale))]

    # TH17
    #poi_game = np.float32(img)[int(40 * scale):int(500 * scale), int(40 * scale):int((425 * scale))]

    return poi_game

def processResize(img, x, y):
    #resize = cv2.resize(np.float32(img), dsize=(x,y), interpolation=cv2.INTER_AREA)
    return img


plt.ion()

while True:
    start_time = time.time()
    train = processResize(getPOI(getImageZone()), 200, 200)
    
    ## Test Zone
    #plt.imshow(train / 255)
    #plt.show()
    #plt.pause(0.01)
    print("Update: ",1.0 / (time.time() - start_time),"fps")
    currentFrame += 1



## Lets do some Deep Learning Stuff
import tensorflow as tf

keras = tf.keras

model = keras.Sequential()
model.add(keras.layers.Conv2D(200,5,5,input_shape=(200,200,3),activation='relu'))
model.add(keras.layers.MaxPooling2D(pool_size=(4,4), strudes=None, padding='valid', data_format=None))

model.add(keras.layers.Conv2D(150,5,5,input_shape=(200,200,3),activation='relu'))
model.add(keras.layers.MaxPooling2D(pool_size=(4,4), strudes=None, padding='valid', data_format=None))

model.add(keras.layers.Conv2D(100,5,5,input_shape=(200,200,3),activation='relu'))
model.add(keras.layers.MaxPooling2D(pool_size=(4,4), strudes=None, padding='valid', data_format=None))

model.add(keras.layers.Dense(9))

model.compile(sgd(lr=.01), "mse")
# Input
# left, right, up, down, Shift+left, Shift+right, Shift+up, Shift+down, X
# Z is constantly pressed.

