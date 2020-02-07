import time
import socket
import pickle
import pynput
from CIRNO.TouhouPOIHandler import THGamePOIRensen
from CIRNO.TouhouMemoryHandler import THGameMemoryRensen
from Utils.Screenshot import WindowsImageLoader, LinuxImageLoader
from Utils.OSHandler import isWindows, isLinux, isSupported
from Utils.Socket import addHeader, headerLength, imageSize

# This code will send current screenshot to 
# server.

scale = float(input("Enter GUI Scale:"))

imageLoader = None

# Operating System Check
if not isSupported():
    print("Current platform is not supported, yet.")
    exit(1)

if isWindows():
    imageLoader = WindowsImageLoader(scale)
elif isLinux():
    imageLoader = LinuxImageLoader(scale)
else:
    print("Failed to detect Operating System.")
    print("Most likely your system is not supported, yet.")
    exit(1)

print("Please Launch Touhou Project and Press Enter, then quickly go back to window")
input()

for i in range(5,0,-1):
    print(i)
    time.sleep(1)

# Set Window.
imageLoader.setWindow()

print()
print("Done! now Please Enter the Server address")
remote = input("Enter CIRNO Server address: ")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("Connecting to CIRNO Server @ "+remote+":⑨⑨⑨⑨")
s.connect((remote, 9999))

gamePOI = THGamePOIRensen(scale)
gameMemory = THGameMemoryRensen()

isThisMsgNew = True
fullMsg = b''

while True:
    gameScreen = gamePOI.PointOfInterestProcess(imageLoader.getScreenshot()).resize(imageSize)
    cirnoMsgObj = {
        "score": gameMemory.getScore(),
        "lives": gameMemory.getLives(),
        "screen": gameScreen,
        "bombs": gameMemory.getBombs()
    }
    cirnoMsg = pickle.dumps(cirnoMsgObj)
    cirnoMsg = addHeader(cirnoMsg)
    print("Sending Packet...")

    s.send(cirnoMsg)
    
    print("Receiving Packets")
    msg = s.recv(headerLength)
    if isThisMsgNew:
        messageLength = int(msg[:headerLength])
        isThisMsgNew = False

    cirnoData = None
    
    fullMsg += msg

    if len(fullMsg)-headerLength == messageLength:
        print("Message Received.")
        print(fullMsg[headerLength:])

        header = fullMsg[:headerLength]
        payload = fullMsg[headerLength:]

        cirnoData = pickle.loads(payload)
        
        isThisMsgNew = True
        fullMsg = b''

        if cirnoData['input']['keyboard']['shift']:
            pynput.keyboard.press(pynput.keyboard.Key.shift)
        else:
            pynput.keyboard.release(pynput.keyboard.Key.shift)

        if cirnoData['input']['keyboard']['z']:
            pynput.keyboard.press(pynput.keyboard.Key.z)
        else:
            pynput.keyboard.release(pynput.keyboard.Key.z)

        if cirnoData['input']['keyboard']['x']:
            pynput.keyboard.press(pynput.keyboard.Key.x)
        else:
            pynput.keyboard.release(pynput.keyboard.Key.x)

        if cirnoData['input']['keyboard']['left']:
            pynput.keyboard.press(pynput.keyboard.Key.left)
        else:
            pynput.keyboard.release(pynput.keyboard.Key.left)

        if cirnoData['input']['keyboard']['right']:
            pynput.keyboard.press(pynput.keyboard.Key.right)
        else:
            pynput.keyboard.release(pynput.keyboard.Key.right)

        if cirnoData['input']['keyboard']['up']:
            pynput.keyboard.press(pynput.keyboard.Key.up)
        else:
            pynput.keyboard.release(pynput.keyboard.Key.up)

        if cirnoData['input']['keyboard']['down']:
            pynput.keyboard.press(pynput.keyboard.Key.down)
        else:
            pynput.keyboard.release(pynput.keyboard.Key.down)

    






