import datetime
import os
from shutil import copyfile

from PIL import Image, ExifTags


class DirectoryWalker:
    def __init__(self, src_dir, dst_dir):
        if not os.path.isdir(src_dir):
            print("not a directory: ", src_dir)
            raise
        self.src_dir = src_dir
        if not os.path.isdir(dst_dir):
            print("not a directory: ", dst_dir)
            raise
        self.dst_dir = dst_dir

    def copy_files(self):
        for r, d, f in os.walk(self.src_dir):
            for file in f:
                file_name = os.path.join(r, file)
                if self.should_process(file_name):
                    self.process_file(file_name)

    def should_process(self, file_name):
        ext = os.path.splitext(file_name)[1].lower();
        return ext in [".png",".jpg",".jpeg",".avi",".3gp"] and os.path.getsize(file_name) > 1000

    def process_file(self, src_file):
        date = self.get_date_exif(src_file)
        dest_dir = self.dst_dir + '/' + date[0:4] + '/' + date
        os.makedirs(name=dest_dir, exist_ok=True)
        dest_file_name = dest_dir + '/' + os.path.basename(src_file)
        if os.path.exists(dest_file_name):
            print("already exists: ", dest_file_name)
            return

        print("process: ", src_file, ", dest: ", dest_file_name)
        copyfile(src_file, dest_file_name)

    def get_date_exif(self, file_name):
        try:
            exif = {
                ExifTags.TAGS[k]: v
                for k, v in Image.open(file_name)._getexif().items()
                if k in ExifTags.TAGS
            }
            date = exif['DateTimeOriginal']
            if date:
                return str(date[:10]).replace(":", "_")
        except:
            pass
        file_date = datetime.datetime.fromtimestamp(os.path.getctime(file_name))
        return file_date.strftime("%Y_%m_%d")
