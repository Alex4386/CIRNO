import pickle
import socket
from Utils.Socket import headerLength
import matplotlib.pyplot as plt
from PIL import Image

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 9999))
s.listen(5)

isThisMsgNew = True
fullMsg = b''

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
    print(fullMsg[headerLength:])

    header = fullMsg[:headerLength]
    payload = fullMsg[headerLength:]

    cirnoData = pickle.loads(payload)
    plt.imshow(cirnoData['screen'])
    plt.show()
    print("score:", cirnoData['score'])

    isThisMsgNew = True
    fullMsg = b''
    


    
  


