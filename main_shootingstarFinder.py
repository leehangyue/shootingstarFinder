# -*- coding: utf-8 -*-

"""
Shooting Star Finder

Read all jpg files in the given folder
For each jpg image check if it contains a shooting star

Process:
rgb to gray scale
threshold to black and white: threshold1
find all connected domains
do some extra checking
check if it is diameter is larger than threshold2
if yes, move the image to the destination folder

coded on Dec.24th 2018 by Leo李航越 referring to ResizeTo2000.py by 何悦
Scratch version
"""

from PIL import Image, ImageFilter
from tqdm import tqdm
import os
import shutil
import findConnectedDomains

import sys

if len(sys.argv) != 3:
    print('示例: python shootingstarFinder 源文件夹名称 目标文件夹名称')
    sys.exit()
srcdir = sys.argv[1]
destdir = sys.argv[2]

re_relative_shstar_size = 58  # a shooting star is at least 1 / re_relative_shstar_size as large/long as the image
re_relatice_star_size = 190  # a star is at most 1 / re_relative_star_size as large as the image
shrink_ratio = 0

List = os.listdir(srcdir)
shooting_star_img = []
failed_moving_shstar_img = []

if not srcdir.endswith('\\'):
    srcdir += '\\'
if len(destdir) < 2:
    destdir = srcdir + 'shootingstarsResult\\'
if not destdir.endswith('\\'):
    destdir += '\\'


def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)


if not os.path.exists(destdir):
    create_folder(destdir)

for name in tqdm(List):  # tqdm shows the progress bar
    if not name.lower().endswith('jpg'):
        continue
    path = os.path.join(srcdir, name)
    img = Image.open(path)
    imgL = img.convert("L")
    edges = imgL.filter(ImageFilter.FIND_EDGES)
    w, h = edges.size

    shrink_ratio = (max(w, h) - 100) // 1000
    if shrink_ratio == 0:
        shrink_ratio = 1
    min_sq_shstar_size = (max(w, h) / re_relative_shstar_size) ** 2
    max_sq_star_size = (max(w, h) / re_relatice_star_size) ** 2
    min_sq_shstar_size /= shrink_ratio ** 2
    max_sq_star_size /= shrink_ratio ** 2

    edges = edges.point(findConnectedDomains.pix_thresh)
    edges = edges.resize((int(w/shrink_ratio), int(h/shrink_ratio)), resample=Image.BOX)
    w, h = edges.size
    edges = edges.crop((1, 1, w-1, h-1))
    cuts = findConnectedDomains.find_cuts(edges)
    if cuts:  # if cuts is not empty
        cut_sq_sizes = [(c[2] - c[0]) ** 2 + (c[3] - c[1]) ** 2 for c in cuts]
        cut_sq_candidate = [sq_size for sq_size in cut_sq_sizes if sq_size > min_sq_shstar_size]
        cut_trivial = [sq_size for sq_size in cut_sq_sizes if sq_size < min_sq_shstar_size]
        if len(cut_sq_candidate) > 10:
            # it's almost impossible to have more than 10 shooting stars in one exposure within 15s
            continue  # because this photo is considered blurred
        if len(cut_trivial) > 10 and sum(cut_trivial) / len(cut_trivial) > max_sq_star_size:
            # it's almost impossible that the stars have an excessively large average diameter
            continue  # if so, this photo is considered out of focus
        if cut_sq_candidate:  # if at least one cut is large enough to be a candidate
            shooting_star_img.append(name)
            try:
                shutil.move(srcdir + name, destdir + name)
            except OSError:
                failed_moving_shstar_img.append(name)
                print("\nFailed moving ", name, "!")
    shrink_ratio = 0

# print(shooting_star_img)
print('\n' + str(len(shooting_star_img)) + 'images in ' + srcdir +
      ' with probably a shooting star are moved to ' + destdir + '.\n')
print('Failed moving these images that probably each contain a shooting star: \n' +
      str(failed_moving_shstar_img) + '\n')
