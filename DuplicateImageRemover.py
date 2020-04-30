#!/usr/bin/python

import datetime
from PIL import Image, ImageChops
import sys
from pathlib import Path
import os
import shutil
import imagehash
import time
import sys


def compare_two_files(first_image, second_imageB):
    try:
        i1 = Image.open(first_image)
        i2 = Image.open(second_imageB)

        # if i1.mode != i2.mode:
        #     msg = "Type mismatch: {} and {}".format(first_image, second_imageB)
        #     raise ValueError(msg)
        # if i1.size != i2.size:
        #     msg = "Size mismatch: {} and {}".format(first_image, second_imageB)
        #     raise ValueError(msg)
        if i1.mode != i2.mode or i1.size != i2.size:
            return None

        return imagehash.average_hash(i1) - imagehash.average_hash(i2)
        # return hash1 - hash2
    # except ValueError as err:
    # print("My bad: ====> ", err.args)
    except:
        a = 'Do nothing here'
        #print("Error: ====> ", sys.exc_info()[0])


def process_files(src_dir_path, dest_dir_path):
    start_time = time.time()
    dest_dir_path = os.path.dirname(src_dir_path) + "\\DuplicateData"
    # if not os.path.exists(dest_dir_path):
    #     os.makedirs(dest_dir_path, exist_ok=True)
    path_file_list = Path(src_dir_path).glob('**/*.JPG')
    all_files = list(path_file_list)
    #print (all_files[0])
    count = len(all_files)
    for i in range(0, count):
        source_file = all_files[i]
        if os.path.basename(source_file).startswith('.'):
            continue
        for j in range(i + 1, count):
            compare_file = all_files[j]
            if os.path.basename(compare_file).startswith('.'):
                continue

            print('currently processing files are: ', source_file, '\t\t', compare_file)
            # compare similar extension files but ignore the same file
            # a = os.path.splitext(source_file)
            # b = os.path.splitext(compare_file)
            if source_file != compare_file and os.path.splitext(source_file)[1] == os.path.splitext(compare_file)[1]:
                # if source_file != compare_file:
                difference = compare_two_files(source_file, compare_file)
                if difference is not None and difference <= 5:
                    new_sub_dir_path = str(compare_file).replace(src_dir_path, "")
                    new_dest_file = dest_dir_path + new_sub_dir_path
                    path_to_be_created = os.path.dirname(os.path.abspath(new_dest_file))
                    if not os.path.exists(path_to_be_created):
                        os.makedirs(path_to_be_created, exist_ok=True)
                    shutil.move(compare_file, new_dest_file)
                    print("Removed File ", compare_file, "compared file: ", source_file)
    print("--- %s processing time in minutes ---" % ((time.time() - start_time)/60))

def dhash(image, hash_size=25):
    # Grayscale and shrink the image in one step.
    image = image.convert('L').resize(
        (hash_size + 1, hash_size),
        Image.ANTIALIAS,
    )


    pixels = list(image.getdata())
    # Compare adjacent pixels.
    difference = []
    for row in range(hash_size):
        for col in range(hash_size):
            pixel_left = image.getpixel((col, row))
            pixel_right = image.getpixel((col + 1, row))
            difference.append(pixel_left > pixel_right)
    # Convert the binary array to a hexadecimal string.
    decimal_value = 0
    hex_string = []
    for index, value in enumerate(difference):
        if value:
            decimal_value += 2 ** (index % 8)
        if (index % 8) == 7:
            hex_string.append(hex(decimal_value)[2:].rjust(2, '0'))
            decimal_value = 0
    return ''.join(hex_string)

def hashset_comparison(src_dir_path):
    start_time = time.time()
    dest_dir_path = os.path.dirname(src_dir_path) + "\\DuplicateData"
    # if not os.path.exists(dest_dir_path):
    #     os.makedirs(dest_dir_path, exist_ok=True)
    path_file_list = Path(src_dir_path).glob('**/*.JPG')
    all_files = list(path_file_list)
    # print (all_files[0])
    count = len(all_files)
    image_hash = {}
    for i in range(0, count):
        source_file = all_files[i]
        if os.path.basename(source_file).startswith('.'):
            continue
        new_hash = dhash(Image.open(source_file))
        if image_hash.get(new_hash) is None:
            image_hash[new_hash] = source_file
        else:
            print("Duplicates found new file: ", source_file, "existing file: ", image_hash.get(new_hash))
            archive_file(src_dir_path, source_file)

    print("--- %s processing time in minutes ---" % ((time.time() - start_time) / 60))

def archive_file(src_dir_path, file):
    dest_dir_path = os.path.dirname(src_dir_path) + "\\DuplicateData"
    new_sub_dir_path = str(file).replace(src_dir_path, "")
    new_dest_file = dest_dir_path + new_sub_dir_path
    path_to_be_created = os.path.dirname(os.path.abspath(new_dest_file))
    if not os.path.exists(path_to_be_created):
        os.makedirs(path_to_be_created, exist_ok=True)
    shutil.move(file, new_dest_file)

if __name__ == "__main__":
    # src_dir_path = r"C:\Users\a6pj8zz\Desktop\Greenway\nnn"
    src_dir_path = r"C:\Users\a6pj8zz\Desktop\Greenway\nnn"
    dest_dir_path = r"D:\NitishNaidi\Personal\DuplicateData"
    log_file = os.path.dirname(src_dir_path) + "\\info.log"
    if not os.path.exists(log_file):
        open(log_file, 'a')
    sys.stdout = open(log_file, 'a')
    print("\n\n\n")
    print("Process started at ", datetime.datetime.now(), "on path: ", src_dir_path)
#    sys.exit(process_files(src_dir_path, dest_dir_path))
    sys.exit(hashset_comparison(src_dir_path))
