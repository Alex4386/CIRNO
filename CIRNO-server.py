import pickle
import socket
import matplotlib.pyplot as plt
from CIRNO.DeepQNetwork import DeepQNetwork
from Utils.Socket import headerLength, imageSize
from PIL import Image

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 9999))
s.listen(5)

isThisMsgNew = True
fullMsg = b''

# This should be same with the client
CIRNONet = DeepQNetwork(
  screenWidth=imageSize[0],
  screenHeight=imageSize[1],
  batchSize=128,
  gamma=0.999,
  epsilonStart=0.9,
  epsilonEnd=0.05,
  epsilonDecay=200,
  action=14
  #       up, down, left, right
  #     Z+up, down, left, right
  # Shift+up, down, left, right
  #        X, nothing
)

print("CIRNO Server Online!")
conn, addr = s.accept()
while True:
  try:
    msg = conn.recv(headerLength)
    print("New Message Received!")
  except:
    conn.close()
    continue

  if isThisMsgNew:
    try:
      messageLength = int(msg[:headerLength])
      print("messageLength Parsed: ", messageLength)
    except ValueError:
      continue

    isThisMsgNew = False
  
  fullMsg += msg

  if len(fullMsg)-headerLength == messageLength:
    print("Message Received.")

    header = fullMsg[:headerLength]
    payload = fullMsg[headerLength:]

    cirnoData = pickle.loads(payload)
""" 
    plt.imshow(cirnoData['screen'])
    plt.show()
    print("score:", cirnoData['score']) 
"""

    isThisMsgNew = True
    fullMsg = b''

    # DQN Processing Stuff
    x = CIRNONet.selectAction(cirnoData['screen'])
    CIRNONet.train()
    
    confidence, index = x.max(0)
    print("Operation Index:", index, "with confidence:", confidence)

    # Input Handling

    keyboardInput = {
      "shift": False,
      "z": False,
      "x": False,
      "up": False,
      "left": False,
      "right": False,
      "down": False
    }

    if index / 4 < 3:
      if index % 4 == 0:
        keyboardInput['up'] = True
      elif index % 4 == 1:
        keyboardInput['left'] = True
      elif index % 4 == 2:
        keyboardInput['right'] = True
      elif index % 4 == 3:
        keyboardInput['down'] = True
    
    if index // 4 == 1:
      keyboardInput['z'] = True
    
    if index // 4 == 2:
      keyboardInput['shift'] = True

    if index // 4 == 3:
      if index == 12:
        keyboardInput['x'] = True
      
    # Send Client a data

    cirnoSendData = pickle.dumps({
      "input": {
        "keyboard": keyboardInput
      }
    })

    conn.send(cirnoSendData)
    


    
  


