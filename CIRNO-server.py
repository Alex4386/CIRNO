import pickle
import socket
from Utils.Socket import headerLength

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(socket.gethostname(), 9999)
s.listen(5)

isThisMsgNew = True
fullMsg = b''

while True:
  msg = s.recv(headerLength)
  if isThisMsgNew:
    messageLength = int(msg[:headerLength])
    isThisMsgNew = False
  
  fullMsg += msg

  if len(fullMsg)-headerLength == messageLength:
    print("Message Received.")
    print(fullMsg[headerLength:])

    header = fullMsg[:headerLength]
    payload = fullMsg[headerLength:]

    cirnoData = pickle.loads(payload)

    isThisMsgNew = True
    fullMsg = b''


    
  


