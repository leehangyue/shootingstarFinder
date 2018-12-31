# -*- coding: utf-8 -*-

from c_find_cuts import c_find_cuts


white_thresh = 40  # 亮度大于此数值的像素被认为是连通域成员


def find_cuts(img, thresh=white_thresh):
    # 传入明度图片进行二值化并做连通域分割

    # img.show()
    pix_access = img.load()
    w, h = img.size
    pixdata = [[]] * w
    for x in range(w):
        column = [[]] * h
        for y in range(h):
            column[y] = pix_access[x, y] > thresh
        pixdata[x] = column
    return c_find_cuts(pixdata, w, h)


def pix_thresh(pixval, thresh=white_thresh):
    if pixval > thresh:
        return 255
    else:
        return 0
