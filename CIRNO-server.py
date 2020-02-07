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
    CIRNONet.selectAction(cirnoData['screen'])
    CIRNONet.train()

    cirnoSendData = pickle.dumps({
      "input": {
        "keyboard": {
          "shift": False,
          "z": False,
          "x": False,
          "up": False,
          "left": False,
          "right": False,
          "down": False
        }
      }
    })

    conn.send(cirnoSendData)
    


    
  


