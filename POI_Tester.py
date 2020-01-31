import time
import matplotlib.pyplot as plt

# Platform Specific Initialization
from Utils.Screenshot import WindowsImageLoader, LinuxImageLoader
from Utils.OSHandler import runByOS, isWindows, isLinux

# Testing Code
if __name__ == "__main__":

    scale = float(input("Enter GUI Scale:"))
    imageLoader = WindowsImageLoader(
        scale) if isWindows() else LinuxImageLoader(scale)

    print("Please Launch Desired touhou project version")
    input("Press Enter, then it will capture the Active Window Automatically after 5 seconds ")
    print()

    print("Waiting for capture")
    time.sleep(5)
    imageLoader.setWindow()
    print()

    print("Window handle:", imageLoader.window)
    print()

    print("Getting image...")
    img = imageLoader.getScreenshot()

    print("Matplotlib export trial:")
    plt.imshow(img)
    plt.show()

    print("Test Complete")

    from CIRNO.TouhouGameHandler import THGameRensen

    rensen = THGameRensen(scale)
    currentFrame = 0

    while True:
        start_time = time.time()
        imgPOI = imageLoader.imageProcess(
            rensen.PointOfInterestProcess(
                imageLoader.getScreenshot() / 255))

        print("Update: ", 1.0 / (time.time() - start_time), "fps")
        currentFrame += 1
