# -*- coding: utf-8 -*-
# ---------------------
# 作者：瓦力冫
# 来源：CSDN
# 原文：https://blog.csdn.net/fox64194167/article/details/80557242
# Modified by Leo李航越 on Dec.30th 2018

# import queue  # a First-In-First-Out data structure with or without(not in C) a max length
# but this library is much too slow


def c_find_cuts(pixdata, w, h):  # 懒得写成C了，欢迎助攻啊！就这个函数占一半的runtime
    min_diameter = 3  # 尺寸不超过min_diameter的连通域被认为是噪点，条件根据需要修改

    visited = set()
    q = MyQueue(initsize=4)  # the queue is 'normally' no longer than 6, <900 for ponttor.jpg
    offset = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    cuts = []
    # qsize_max = 0
    for x in range(w):
        for y in range(h):
            x_axis = []
            y_axis = []
            if (x, y) in visited:
                continue
            elif pixdata[x][y]:
                q.put((x, y))
                # if q.qsize() > qsize_max:
                #     qsize_max = q.qsize()
                visited.add((x, y))
            while not q.empty():
                x_p, y_p = q.get()
                for x_offset, y_offset in offset:
                    x_c, y_c = x_p + x_offset, y_p + y_offset
                    if x_c < 0 or x_c >= w or y_c < 0 or y_c >= h:
                        continue
                    if (x_c, y_c) in visited:
                        continue
                    visited.add((x_c, y_c))
                    if pixdata[x_c][y_c]:
                        q.put((x_c, y_c))
                        # if q.qsize() > qsize_max:
                        #     qsize_max = q.qsize()
                        x_axis.append(x_c)
                        y_axis.append(y_c)
            if x_axis and y_axis:
                min_x, max_x = min(x_axis), max(x_axis)
                min_y, max_y = min(y_axis), max(y_axis)
                if max_x - min_x > min_diameter and max_y - min_y > min_diameter:
                    # 尺寸太小的连通域被认为是噪点，条件根据需要修改
                    cuts.append((min_x, min_y, max_x + 1, max_y + 1), )
    # print('qsize_max = ', qsize_max)
    return cuts


class MyQueue:
    def __init__(self, initsize=1 << 20):
        self._front = 0
        self._rear = -1
        self._maxsize = initsize
        self._size = 0
        self._data = [[]] * initsize

    def put(self, elem):
        if self._size == self._maxsize:
            self.double_size()
        if self._rear == self._maxsize - 1:
            self._rear = 0  # 0 = -1 + 1
        else:
            self._rear += 1
        self._data[self._rear] = elem
        self._size += 1

    def get(self):
        if self._size == 0:
            raise Exception('Error getting element: the queue is empty!')
        elem = self._data[self._front]
        if self._front == self._maxsize - 1:
            self._front = 0
        else:
            self._front += 1
        self._size -= 1
        return elem

    def empty(self):
        return self._size == 0

    def size(self):
        return self._size

    def double_size(self):
        self._data = self._data + [[]] * self._maxsize
        if self._size > 0 and self._front > self._rear:  # if there's a loop back
            for i in range(self._rear + 1):
                self._data[i + self._maxsize] = self._data[i]
            self._rear += self._maxsize
            # i.e. change the queue from
            #     |rear   |front
            # c d e _ _ _ a b
            # 0 1 2 3 4 5 6 7 (indices)
            # to
            #     |rear   |front
            # c d e _ _ _ a b _ _ _ _ _ _ _ _
            # and then
            #             |front  |rear
            # c d e _ _ _ a b c d e _ _ _ _ _
        self._maxsize *= 2
