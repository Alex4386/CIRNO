def conv2DOutsize(size, kernel_size = 5, stride = 2):
  return (size - (kernel_size - 1) - 1) // stride  + 1