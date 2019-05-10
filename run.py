from NettackerTool import NettackerTool
import time

# YOU CANNOT SCAN LOCALHOST!!! IM PRETTY SURE IT WILL JUST SCAN THE DOCKER CONTAINER THAT ITS IN!
n = NettackerTool(target='10.0.0.44', scan_options='all', timeout=10000)
n.start()

while not n.finished:
    print('waiting')
    time.sleep(1)

f = open('output.txt', 'w')
f.write(n.raw_output)
f.close()

print(n.raw_output)

