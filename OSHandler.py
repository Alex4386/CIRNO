import platform


def getOS(): return platform.system()


def getEasyOS():
    if getOS().lower() == "windows":
        return "Windows"
    elif getOS().lower() == "linux":
        return "Linux"
    elif getOS().lower() == "darwin":
        raise OSError("macOS is not supported!")
    else:
        raise OSError("Unsupported Operating System!")


def runByOS(winFunc, linuxFunc):
    if getOS().lower() == "windows":
        return winFunc()
    elif getOS().lower() == "linux":
        return linuxFunc()


def isLinux(): return getEasyOS() == "Linux"


def isWindows(): return getEasyOS() == "Windows"


def isSupported():
    try:
        return isLinux() or isWindows()
    except:
        return False
