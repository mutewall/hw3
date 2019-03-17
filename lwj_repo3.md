# 第三次作业

廖沩健

自动化65

2160504124

提交日期:  2019年3月17日

摘要:

这次作业聚焦于使用直方图处理图像，包括图像的均衡，匹配，局部增强，分割。其中所有的算法都是用python从头实现的，使用到的辅助库主要有numpy,cv2,matplotlib等。大部分参考的都是课本与ppt的内容。对于所有处理结果的讨论以及对于某些算法的分析，都展示在下面的对应的部分。


## 直方图

在以下图片的标题中，以0结尾的都代表原始图像(未经亮度处理)

### citywall
![citywall](https://raw.githubusercontent.com/mutewall/homework_img/master/31c.png)

### elain
![elain](https://raw.githubusercontent.com/mutewall/homework_img/master/31el.png)

### lena
![lena](https://raw.githubusercontent.com/mutewall/homework_img/master/31le.png)

### woman
![woman](https://raw.githubusercontent.com/mutewall/homework_img/master/31w.png)

从直方图中可以看出，只要经过亮度处理的图片，其直方图都将出现一个非常"尖锐"的峰，表明大部分像素集中在这一个像素值上。

## 直方图均衡

以下展示的均为均衡化以后的图像。

### citywall
![citywall_eq](https://raw.githubusercontent.com/mutewall/homework_img/master/32c.png)

citywall0，即真正的原图，均衡化使图像有所失真，灰度偏白；citywall1的原图有过度曝光的效应，经过均衡化处理后，画面变自然了些，城墙和树林显示出了一点深色；citywall2的原图是整个画面变暗了，应该灰度整体做了一个同尺度的缩小，均衡化以后，画面明显变亮了，但城墙变得过亮，呈现了过多不应有的白色。

### elain
![elain_eq](https://raw.githubusercontent.com/mutewall/homework_img/master/32el.png)

原图均衡化后，整体颜色变深，更加强烈的观感；elain1原图本身有种过度曝光的效果，均衡化后，整体没有多大的改善，但一些细节得到了凸显，比如头发，眼睛，比原来更加生动；elain2原图就是变暗了一点点，均衡化后，背景变亮，人物显示出一点点过度曝光效果，但整体是不错的，细节还比较分明；elain3的原图像是被一个黑色的"布"盖住了一样，但可以看出原图的整体与细节都很好的保留了，因此处理后，有不错的还原，与前一张差不多效果。

### lena
![lena_eq](https://raw.githubusercontent.com/mutewall/homework_img/master/32le.png)

lena真正的源图像经处理后，虽然整体亮度增加，但颜色变化显得非常不自然，一些细节也有丢失，比如肩膀的骨头凸起就没有了；lena1的原图做了类似于黑白二值化的处理，本身表达的灰度值就少，因此即使是均衡化，在不能增加灰度值的情况下效果还是很差的，属于正常现象；lena2的原图像是蒙上了一层雾，处理后，显然这层雾就消失了，人物，背景都清晰展现了出来，效果不错；lena3的原图颜色加深了，处理后，增添了更多的白色，使画面更加均衡。

### woman
![woman_eq](https://raw.githubusercontent.com/mutewall/homework_img/master/32w.png)

woman真正的源图像经处理后，面部，手掌变得更白了;woman1没有多大的改善;woman2的画面变亮了，面部特征得到凸显。

## 直方图匹配
以下图片均是基于未经亮度处理的源图像做匹配，因为要自己构造一个好的图像分布太困难。因此，展示的bmp图片中，只有经亮度处理过的原图的匹配图，展示的直方图中，以0结尾为标题的是匹配源的直方图(即源图像的直方图)，其余的是被处理后的图像的直方图。（由于技术失误，直方图的纵轴范围不一样，需要特别注意）

做直方图匹配时，首先将需要被匹配的图像(目标图像)和用来提供匹配分布的图像(源图像)分别进行均衡化，然后分别对它们建立一个与均衡化前图像的intensity map(IM)，这样一来，只要在源图像的IM里找到与当前目标图像像素相差最小的值的索引，即对应了需要得到的匹配图像像素值在源图像中的映射。这样的做法复杂度为$O$($L$*$H^{2}$)，其中，L为像素级，H为图像大小。由于L通常远小于H，因此这个复杂度还能接受，但肯定是还可以优化的。

### citywall

citywall1

![citywall_match](https://raw.githubusercontent.com/mutewall/homework_img/master/c1m.bmp)

citywall2

![](https://raw.githubusercontent.com/mutewall/homework_img/master/c2m.bmp)

hist

![](https://raw.githubusercontent.com/mutewall/homework_img/master/33c.png)

citywall1在匹配后，整体亮度变低了一点，更接近原始图像，城墙上的细节也得到了一定改善，直方图中也可以看出，低灰度值增加了很多;citywall2匹配后效果很好，之前的灰色状态完全清楚，也保留了细节，城墙与树林的颜色过度自然，从直方图来看，形状确实也比较接近源图像的直方图。

### elain
elain1

![elain_match](https://raw.githubusercontent.com/mutewall/homework_img/master/e1m.bmp)

elain2

![](https://raw.githubusercontent.com/mutewall/homework_img/master/e2m.bmp)

elain3

![](https://raw.githubusercontent.com/mutewall/homework_img/master/e3m.bmp)

hist

![](https://raw.githubusercontent.com/mutewall/homework_img/master/33e.png)

这一组图在匹配后，整体比均衡化后的图更加柔和，对比度降低，但同时有较好的保留了细节，效果不错；但从直方图中可以看出，有些像素值难以改进，上面仍然聚集了大量像素点。

### lena

lena1

![lena_match](https://raw.githubusercontent.com/mutewall/homework_img/master/l1m.bmp)

lena2

![](https://raw.githubusercontent.com/mutewall/homework_img/master/l2m.bmp)

lena3

![](https://raw.githubusercontent.com/mutewall/homework_img/master/l3m.bmp)

hist

![](https://raw.githubusercontent.com/mutewall/homework_img/master/33l.png)

lena1的图像在匹配后，本质上无大的改进，只是画面更加柔和；而lena2的图像匹配得非常好，色调合适，颜色过渡自然，细节也得到了凸显，从直方图来看，其形状也几乎和原来的图相同；lena3匹配得也不错，除了色调稍微偏暗，其他细节都挺好。

### woman

woman1

![woman_match](https://raw.githubusercontent.com/mutewall/homework_img/master/w1m.bmp)

woman2

![](https://raw.githubusercontent.com/mutewall/homework_img/master/w2m.bmp)

hist

![](https://raw.githubusercontent.com/mutewall/homework_img/master/33w.png)

画面相较之前变得明亮柔和，整体效果不错。woman2的直方图除了那个尖峰，整体变化趋势也匹配较好。

## 局部增强
这里使用图像的统计数据，包括全局均值和方差，局部均值和方差，进行增强，公式如下:
$$
g(x,y) = 
\begin{cases}
    E*f(x,y), &\text{$m_{s}$$\leq$$k_{0}$$m_{g}$ 且 $k_{1}\sigma_{g}$$\leq$$\sigma_{s}$$\leq$$k_{2}$$\sigma_{g}$}\\
    f(x,y), &\text{其他}
\end{cases}
$$
其中$f(x,y)$表示原始像素值，$g(x,y)$表示变化后的像素值，$E$是增益系数，$m_{s}$，$\sigma_{s}$，$m_{g}$，$\sigma_{g}$分别表示局部均值标准差和全局均值和标准差，这里的局部指当前像素值周围的7x7局域。$k$都是系数，需要根据图像调整，但由于时间原因，这里我并没有仔细调整。

elain

![elain_local_enhance](https://raw.githubusercontent.com/mutewall/homework_img/master/34elain.bmp)

lena

![lena_local_enhance](https://raw.githubusercontent.com/mutewall/homework_img/master/34lena.bmp)

elain的眼睫毛，手上的痕迹，lena的帽子的纹路有所增强，由于系数并没有经过仔细调整，所以可能效果不是很明显。

## 直方图分割
基于直方图分割的原理就是要在两个单峰的分布之间，找一个像素值，以此为界　将两边的分布分别作为背景和目标。我通过直方图找到elain的分割像素值大致为220，woman的大致为100。

### elain
![elain_seg](https://raw.githubusercontent.com/mutewall/homework_img/master/35seg_elain.bmp)
### woman
![woman_seg](https://raw.githubusercontent.com/mutewall/homework_img/master/35seg_woman.bmp)

elain的图分出一部分帽子，woman的图大致分出了整个人，效果不错。

