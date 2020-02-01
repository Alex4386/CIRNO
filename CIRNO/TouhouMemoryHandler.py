from Utils.OSHandler import isWindows

if isWindows():
    from ctypes import windll, c_uint, c_ulong, byref, sizeof
else:
    raise OSError("This OS is not supported for Native Touhou Project Runs")

class THGameMemoryKouma():
    def __init__(self):
        self.OpenProcess = windll.kernel32.OpenProcess
        self.ReadProcessMemory = windll.kernel32.ReadProcessMemory
        self.CloseHandle = windll.kernel32.CloseHandle
        self.pid = -1

        for proc in psutil.process_iter():
            if proc.name() == "th06.exe":
                self.pid = proc.pid

        if self.pid < 0:
            raise OSError("Touhou Project was not detected in OS Level")

        self.hProcess = self.OpenProcess(0x0010, false, self.pid)
            

    def __del__(self):
        self.CloseHandle(self.hProcess)

    def getScore(self):
        buffer = c_uint()
        lpBuffer = byref(buffer)
        nSize = sizeof(buffer)
        lpNumberOfBytesRead = c_ulong(0)
        self.ReadProcessMemory(self.hProcess, 0x0069BCA0, lpBuffer, nSize, lpNumberOfBytesRead)
        return buffer.value


# Basically copypasta-ing code from rensen-connect, duh.
class THGameMemoryRensen():
    def __init__(self):
        self.OpenProcess = windll.kernel32.OpenProcess
        self.ReadProcessMemory = windll.kernel32.ReadProcessMemory
        self.CloseHandle = windll.kernel32.CloseHandle
        self.pid = -1

        for proc in psutil.process_iter():
            if proc.name() == "th12.exe":
                self.pid = proc.pid

        if self.pid < 0:
            raise OSError("Touhou Project was not detected in OS Level")

        self.hProcess = self.OpenProcess(0x0010, false, self.pid)
            

    def __del__(self):
        self.CloseHandle(self.hProcess)

    def getScore(self):
        memAddr = 0x004B0C44
        buffer = c_uint()
        lpBuffer = byref(buffer)
        nSize = sizeof(buffer)
        lpNumberOfBytesRead = c_ulong(0)
        self.ReadProcessMemory(self.hProcess, memAddr, lpBuffer, nSize, lpNumberOfBytesRead)
        return buffer.value

    def getLives(self):
        memAddr = 0x004B0C98
        buffer = c_uint()
        lpBuffer = byref(buffer)
        nSize = sizeof(buffer)
        lpNumberOfBytesRead = c_ulong(0)
        self.ReadProcessMemory(self.hProcess, memAddr, lpBuffer, nSize, lpNumberOfBytesRead)
        return buffer.value

    def isGameOver(self):
        return self.getLives() < 0

    def getBombs(self):
        memAddr = 0x004B0CA0
        buffer = c_uint()
        lpBuffer = byref(buffer)
        nSize = sizeof(buffer)
        lpNumberOfBytesRead = c_ulong(0)
        self.ReadProcessMemory(self.hProcess, memAddr, lpBuffer, nSize, lpNumberOfBytesRead)
        return buffer.value
