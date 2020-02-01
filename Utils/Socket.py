headerLength = 32

def addHeader(a):
  return bytes(f'{len(a):<{headerLength}}', "utf-8") + a
