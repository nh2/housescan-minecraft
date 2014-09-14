import mce
from box import BoundingBox

import mmap
import sys
import os
import numpy
from numpy import *

import colours
import time

m = mce.mce()

# Load our world
m.loadWorld("NewWorld")

## Set to stone blocks
#stoneBlockInfo = m.readBlockInfo(["1:0"])
#stoneBox = BoundingBox(origin=(-189, 59, 209), size=(20, 20, 20))
#m.level.fillBlocks(stoneBox, stoneBlockInfo)

# Colour code
c = colours.Colours()

# Read voxels from file and store in intermediate structure
# TODO: Get file from nh2
SIZE = 512

filename = sys.argv[1]
ints = numpy.memmap(filename, uint32)
indices = ints.nonzero()[0]
chars = ints[ints != 0].view(uint8)
bgrs = chars.reshape(-1, 4)[:,:3]
tuple_indices = array(unravel_index(indices, (SIZE, SIZE, SIZE))).T
arr = hstack((tuple_indices, bgrs))
arr = arr[::50]

K = 0
N = 0

bef_t = time.time()

for vox in arr:

    N += 1

    x, y, z = vox[0:3]/4 + (-199, 0, 219)
    r, g, b = vox[3:6]

    blkInfo = m.readBlockInfo([c.find_texture_id((r, g, b))])
    voxBox = BoundingBox(origin=(x, 255 - y, z), size=(1, 1, 1))
    m.level.fillBlocks(voxBox, blkInfo)

    K += 1

    if N % 100 == 0:
        print "%d out of %d (%f%%)" % (N, len(arr), 100 * float(N) / len(arr))
        print "Voxel no. %d" % K

aft_t = time.time()
print "Time taken: %f seconds" % (aft_t - bef_t)

# Save world
m.level.generateLights()
m.level.saveInPlace()
