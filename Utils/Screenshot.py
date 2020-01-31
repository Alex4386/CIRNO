# The ScreenCapture Stuff
import matplotlib.pyplot as plt
import time
import numpy as np

# Image Processing Stuff
import cv2

# Platform Specific Initialization
from OSHandler import runByOS, isWindows, isLinux

if isWindows():
    from PIL import ImageGrab
elif isLinux():
    import gi
    gi.require_version("Gdk", "3.0")

    from gi.repository import Gdk
    from gi.repository import GdkPixbuf
else:
    raise OSError("Unsupported Operating System")


class ImageLoader():
    window = None
    img = None
    scale = 1

    def __init__(self, scale):
        self.scale = scale

    def getScreenshot(self):
        pass

    def setWindow(self):
        pass

    @staticmethod
    def imageProcess(img):
        if np.dtype == np.dtype('float32'):
            if np.max(img) > 1:
                return img / 255

        return img


class WindowsImageLoader(ImageLoader):
    def __init__(self, scale):
        super().__init__(scale)

    def setWindow(self):
        # Since I work in Linux, I don't want this to botter me.

        # pylint: disable=import-error
        import win32gui
        windowHandle = win32gui.GetForegroundWindow()

        if windowHandle == None:
            raise Exception(
                "System API Call Error! Unable to get Foreground Window!")

        self.window = windowHandle

        return windowHandle

    def getScreenshot(self):
        # will fix it later. but, currently, it is just a disgusting code. with pylint errors.

        # pylint: disable=undefined-variable
        rect = win32gui.GetWindowRect(self.window)

        self.img = ImageGrab.grab(
            bbox=(rect[0]*self.scale, rect[1]*self.scale, rect[2]*self.scale, rect[3]*self.scale))

        return self.img


class LinuxImageLoader(ImageLoader):
    def __init__(self, scale):
        super().__init__(scale)

    def setWindow(self):
        # Since I work in Linux, I don't want this to botter me.

        self.window = Gdk.get_default_root_window().get_screen().get_active_window()
        return self.window

    def getScreenshot(self):
        # will fix it later. but, currently, it is just a disgusting code. with pylint errors.

        # STACK OVERFLOW CODE START - PREREQUISITIVES
        def array_from_pixbuf(p):
            " convert from GdkPixbuf to numpy array"
            w, h, c, r = (p.get_width(), p.get_height(),
                          p.get_n_channels(), p.get_rowstride())

            assert p.get_colorspace() == GdkPixbuf.Colorspace.RGB
            assert p.get_bits_per_sample() == 8
            if p.get_has_alpha():
                assert c == 4
            else:
                assert c == 3
            assert r >= w * c
            a = np.frombuffer(p.get_pixels(), dtype=np.uint8)
            if a.shape[0] == w*c*h:
                return a.reshape((h, w, c))
            else:
                b = np.zeros((h, w*c), 'uint8')
                for j in range(h):
                    b[j, :] = a[r*j:r*j+w*c]
                return b.reshape((h, w, c))

        '''
        def pixbuf_from_array(z):
            " convert from np array to GdkPixbuf "
            z = z.astype('uint8')
            h, w, c = z.shape
            assert c == 3 or c == 4
            return GdkPixbuf.Pixbuf.new_from_data(z.tobytes(),  GdkPixbuf.Colorspace.RGB, c == 4, 8, w, h, w*c, None, None)
        '''

        window = self.window
        position = window.get_position()

        pb = Gdk.pixbuf_get_from_window(
            window, position.x, position.y-40, window.get_width(), window.get_height())

        self.img = array_from_pixbuf(pb)

        return self.img

        # STACK OVERFLOW CODE END
#
#
