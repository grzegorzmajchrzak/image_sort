import sys
import os

from DirectoryWalker import DirectoryWalker

if __name__ == '__main__':
    src_dir = sys.argv[1]
    dst_dir = sys.argv[2]

    walker = DirectoryWalker(src_dir, dst_dir)
    walker.copy_files();

