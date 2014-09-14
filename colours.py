import numpy, os, re
from PIL import Image

__all__ = ['Colours']

TEX_DIR = "./mcTextures/"

reg = re.compile(r"^(\d+:\d+)\.png$")

class Colours:
    def __init__(self):
        # List all files in textures directory
        paths = os.listdir(TEX_DIR)

        fname = ""
        index = ""
        imgs = []

        for path in paths:
            # Ignore if not file
            if not os.path.isfile(TEX_DIR + path):
                continue

            fname = os.path.basename(path)
            res = reg.match(fname)
            if res:
                index = res.group(1)
                imgs.append((TEX_DIR + path, index))

        self.tex_ids = []
        self.tex_cols = numpy.zeros((len(imgs), 3))

        # Load image per texture and calculate average RGB
        for i, img in enumerate(imgs):
            imarr = numpy.array(Image.open(img[0]), dtype=numpy.float)[:,:,:3]
            avgcs = numpy.concatenate(imarr).mean(axis=0)
            self.tex_ids.append(img[1])
            self.tex_cols[i] = avgcs

    def find_texture_id(self, voxel_colour):
        return self.tex_ids[numpy.argmin(numpy.linalg.norm(self.tex_cols - voxel_colour, axis=1))]


