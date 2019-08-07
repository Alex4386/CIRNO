import matplotlib.pyplot as plt
import platform
import time
from PIL import ImageGrab

window = None
img = None
scale = 1

def getImageZone():
    print("start get image zone")
    global window
    global img
    global scale
    if platform.system() == "Windows":
        print("platform checked, its windows")
        import win32gui
        rect = win32gui.GetWindowRect(window)
        print("rectangle checked")
        print(rect)
        print("Patching with scale")
        print((rect[0]*scale, rect[1]*scale, rect[2]*scale, rect[3]*scale))
        print("ImageGrab call")
        img = ImageGrab.grab(bbox=(rect[0]*scale, rect[1]*scale, rect[2]*scale, rect[3]*scale))
        print("finished get image zone")
        return
    else:
        print("So, You are not running on Windows, Too bad. Manually write getImage")
        print("If you can get coordinates in macOS and Linux, Please feel free to PR.")
        print("Because I have no idea to fix this. and I am also the Macbook user.")
        return


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
    else:
        print("So, You are not running on Windows, Too bad. Manually write getImage")
        print("If you can get coordinates in macOS and Linux, Please feel free to PR.")
        print("Because I have no idea to fix this. and I am also the Macbook user.")
        return


print("Please Enter your GUI Scale")
scale = float(input("Scale: "))
print("Please Launch Desired touhou project version")
input("Press Enter, then it will capture the Active Window Automatically after 5 seconds ")
time.sleep(5)
getWindowHandle()
print("Got: Window Handle")
print(window)
getImageZone()
print("Image Output:")
print(img)
print("Matplotlib export trial:")
plt.imshow(img)
plt.show()
input("Standby....")


