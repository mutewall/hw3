# -*- coding: UTF-8 -*-  
#廖沩健
#自动化65
#2160504124

from __future__ import division,print_function
import numpy as np
from matplotlib import pyplot as plt
import cv2
import pdb

def load_file(file):
    x = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
    return x

def hist(pic):
    colour = np.zeros((256,),dtype=int)
    h = pic.shape[0]
    w = pic.shape[1]
    for i in range(h):
        for j in range(w):
            col = pic[i,j].tolist()
            if isinstance(col, int):
                colour[col] += 1
            else:
                c1, c2, c3 = col
                colour[c1] += 1
                colour[c2] += 1
                colour[c3] += 1
    return colour

def prob_hist(hist, level=256):
    prob = np.zeros_like(hist, dtype=np.float).reshape(-1,1)
    last = 0.

    for i in range(level):
        prob[i,0] = last + hist[i]
        last = prob[i,0]
    
    prob /= last
    return prob

def equalization(pic, level=256):
    new_pic = np.zeros_like(pic).astype(np.uint8)
    histogram = hist(pic)
    prob = prob_hist(histogram)
    h = pic.shape[0]
    w = pic.shape[1]

    for i in range(h):
        for j in range(w):
            trans = (level - 1) * prob[pic[i,j], 0]
            new_pic[i,j] = round(trans)
    return new_pic

def intensity_map(dst, src, level=256):
    maps = np.zeros(level, dtype=np.uint8)
    visit_sign = np.zeros(level, dtype=np.int)
    h = src.shape[0]
    w = src.shape[1]
    for i in range(h):
        for j in range(w):
            idx = int(src[i,j])
            if visit_sign[idx] == 0:
                maps[idx] = dst[i,j]
                visit_sign[idx] = 1
            else:
                if np.sum(visit_sign) == 256:
                    return maps
    return maps
            

def global_enhance(pic, match):
    new_pic = np.zeros_like(pic).astype(np.uint8)
    # tmp = np.zeros_like(pic).astype(np.uint8)
    epic = equalization(pic)
    ematch = equalization(match)
    srcmap = intensity_map(epic, pic)
    matchmap = intensity_map(ematch, match)
    
    h = new_pic.shape[0]
    w = new_pic.shape[1]
    for i in range(h):
        for j in range(w):
            sij = pic[i,j]
            intensity = np.argmin(abs(srcmap[sij]-matchmap))
            new_pic[i,j] = np.uint8(intensity)
    return new_pic

def local_enhance(pic, size=7, E=4., k0=0.2, k1=0.05, k2=0.5):
    def local_mean(x, y):
        bound = int((size-1) / 2)
        value = 0
        count = 0
        for i in range(-bound, bound+1):
            indx = x + i
            if indx < 0 or indx > pic.shape[0]-1:
                continue
            for j in range(-bound, bound+1):
                indy = y + j
                if indy < 0 or indy > pic.shape[1]-1:
                    continue
                value += pic[indx,indy]
                count += 1
        return value / count
    
    def local_std(x, y, m):
        bound = int((size-1) / 2)
        value = 0
        count = 0
        for i in range(-bound, bound+1):
            indx = x + i
            if indx < 0 or indx > pic.shape[0]-1:
                continue
            for j in range(-bound, bound+1):
                indy = y + j
                if indy < 0 or indy > pic.shape[1]-1:
                    continue
                value += (pic[indx,indy] - m)**2
                count += 1
        return value / count
    
    new_pic = np.zeros_like(pic, dtype=np.uint8)
    gross_mean = np.mean(pic)
    gross_std = np.std(pic)

    h = pic.shape[0]
    w = pic.shape[1]
    for i in range(h):
        for j in range(w):
            lm = local_mean(i,j)
            ls = local_std(i,j,lm)
            if lm <= k0 * gross_mean and ls >= k1 * gross_std and ls <= k2 * gross_std:
                new_pic[i,j] = E*pic[i,j]
            else:
                new_pic[i,j] = pic[i,j]
    
    return np.clip(new_pic, 0, 255)

def segmented_image(pic, thre):
    mask = np.zeros_like(pic).astype(np.int)
    new_pic = np.zeros_like(pic).astype(np.uint8)
    h = pic.shape[0]
    w = pic.shape[1]

    for i in range(h):
        for j in range(w):
            if pic[i,j] > thre:
                mask[i,j] = 1
    
    for i in range(h):
        for j in range(w):
            if mask[i,j] == 1:
                new_pic[i,j] = 255
            else:
                new_pic[i,j] = 0
    return new_pic


def plot_1(num, name):
    for i in range(num):
        id = str(num)+ '1' + str(i+1)
        plt.subplot(eval(id))
        pic = load_file(name+'{}.bmp'.format(i))
        colour = hist(pic)
        plt.plot(np.arange(256), colour)
        # pic = load_file(name+'{}.bmp'.format(i)).flatten()
        # plt.hist(pic,bins=256,normed=1,facecolor='green',alpha=0.7)
        plt.title(name+'{}'.format(i))
        plt.xlim([0,256])
    plt.show()

def plot_2(num, name):
    for i in range(num):
        id = '1' + str(num) + str(i+1)
        plt.subplot(eval(id))
        pic = load_file(name+'{}.bmp'.format(i))
        npic = equalization(pic)
        plt.imshow(npic, cmap='gray')
        plt.title(name+'{}'.format(i))
    plt.show()

def plot_3(num, name):
    imginit = load_file(name+'0.bmp')
    res = []
    for i in range(num):
        id = '1' + str(num) + str(i+1)
        plt.subplot(eval(id))
        pic = load_file(name+'{}.bmp'.format(i))
        if i != 0:
            pic = global_enhance(pic, imginit)
            res.append(pic)
        histogram = hist(pic)
        plt.plot(np.arange(histogram.shape[0]), histogram)
        plt.title(name+'{}'.format(i))
    return res

if __name__ == "__main__":
  
    fig = plt.figure(1)

    plot_1(3, 'citywall')
    plot_1(4, 'elain')
    plot_1(4, 'lena')
    plot_1(3, 'woman')

    plot_2(3, 'citywall')
    plot_2(4, 'elain')
    plot_2(4, 'lena')
    plot_2(3, 'woman')

    c1m, c2m = plot_3(3, 'citywall')
    cv2.imwrite('./res/c1m.bmp', c1m)
    cv2.imwrite('./res/c2m.bmp', c2m)
    plt.show()
    
    e1m, e2m, e3m = plot_3(4, 'elain')
    cv2.imwrite('./res/e1m.bmp', e1m)
    cv2.imwrite('./res/e2m.bmp', e2m)
    cv2.imwrite('./res/e3m.bmp', e3m)
    plt.show()
    
    l1m, l2m, l3m = plot_3(4, 'lena')
    cv2.imwrite('./res/l1m.bmp', l1m)
    cv2.imwrite('./res/l2m.bmp', l2m)
    cv2.imwrite('./res/l3m.bmp', l3m)
    plt.show()

    w1m, w2m = plot_3(3,'woman')
    cv2.imwrite('./res/w1m.bmp', w1m)
    cv2.imwrite('./res/w2m.bmp', w2m)
    plt.show()

    res = local_enhance(load_file('lena0.bmp'))
    cv2.imwrite('./res/34lena.bmp', res)
    dst = load_file('./res/34lena.bmp')
    src = load_file('lena0.bmp')

    res2 = local_enhance(load_file('lena0.bmp'))
    cv2.imwrite('./res/34lena.bmp', res2)
    dst = load_file('./res/34lena.bmp')
    src = load_file('lena0.bmp')
    
    img = load_file('elain0.bmp')
    seg1 = segmented_image(img, 220)
    cv2.imwrite('./res/35seg_elain.bmp', seg1)

    img = load_file('woman0.bmp')
    seg2 = segmented_image(img, 100)
    cv2.imwrite('./res/35seg_woman.bmp', seg2)
    
