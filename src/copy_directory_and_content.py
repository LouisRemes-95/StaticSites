import os, shutil

def copy_directory_and_content(src_path, dst_path):
    if os.path.exists(dst_path):
        shutil.rmtree(dst_path)
    if os.path.isfile(src_path):
        shutil.copy(src_path, dst_path)
    else:
        os.mkdir(dst_path)
        for element in os.listdir(src_path):
            copy_directory_and_content(os.path.join(src_path, element), os.path.join(dst_path, element))