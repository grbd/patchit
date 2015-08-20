"""
Helper class for patching files
"""

# This module uses patchit from https://pypi.python.org/pypi/patchit/1.1

import os
from patchit import PatchSet
from os.path import join, abspath

class PatchitFile(object):
    """Helper class for patching files"""

    def __init__(self, patchfile, startdir, strip = 0):
        self.patchfile = patchfile
        self.startdir = startdir
        self.strip = strip

    def Apply(self):
        """Apply a patch file to a directory"""

        with open(self.patchfile) as patch_hand:
            patches = PatchSet.from_stream(patch_hand)

            for patchitem in patches:
                # Figure out the path of the file to patch
                srcpath = PatchitFile.StripPath(patchitem.source_filename, self.strip)
                srcpath = abspath(join(self.startdir, srcpath))
                
                with open(srcpath) as srcfile_hand:
                    # Get a read handle to the file to patch
                    srcfile_iter = (x.strip('\n') for x in iter(srcfile_hand.readline, ''))
                    # Read in the file and patch in memory
                    outlist = list(patchitem.merge(srcfile_iter))

                    # Overwrite the output file
                    with open(srcpath, 'w') as file:
                        for item in outlist:
                            file.write("{}\n".format(item))
        return

    @staticmethod
    def StripPath(filepath, strip = 0):
        """Strip parts from the front of a relative path, the same as -pX with gnu patch"""

        pathparts = filepath.split(os.sep)
        for x in range(0, strip):
            pathparts.pop(0)
        retpath = join(*pathparts)
        return retpath