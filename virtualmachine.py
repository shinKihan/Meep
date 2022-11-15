import os
filename = [f for f in os.listdir('.') if f.endswith('.obj')][0]
file = open(filename,'r')
content = file.readlines()
file.close()

print(content)