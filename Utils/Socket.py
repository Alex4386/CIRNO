headerLength = 32
imageSize = (378, 440)

def addHeader(a):
  return bytes(f'{len(a):<{headerLength}}', "utf-8") + a
