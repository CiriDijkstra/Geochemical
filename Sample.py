import numpy as np


class Sample:
    """
    Sample类的实例用于存储一个样品的一些信息
    成员变量包括：
    样品号（从1开始编号）
    微量元素含量
    微量元素的“变差衬度值”
    常量元素含量（用于做分类或聚类，用一个list存储）
    类标号（默认未分类为-1，类标号从1开始到k）
    成员函数包括：
    dist：计算两个样品常量元素含量之间的欧氏距离（二范数）
    describe：输出该样品的一些描述信息
    is_adjacency：判断两个样品在高斯网格上是否相邻
    """
    next_id = 1
    max_edge = 0.03    #高斯网格上相邻网格点的高斯坐标距离约为0.02，取一个比0.02的根号2倍稍大的数即可

    def __init__(self, XX, YY, W , Sn, Pb, Zn, class_id = -1):
        """
        :param XX， YY: 该样品的高斯坐标值
        :param W, Sn, Pb, Zn: 该样品的对应元素含量值
        :param class_id: 该样品的类标号
        :param *_contrast: 该样品对应元素的变差衬度值
        """
        self.sample_id = Sample.next_id
        Sample.next_id += 1
        self.XX = XX
        self.YY = YY
        self.W = W
        self.Sn = Sn
        self.Pb = Pb
        self.Zn = Zn
        self.macro_element = []       #常量元素含量
        self.class_id = class_id    #未分类时类标号默认为-1
        self.W_contrast = 0     #衬度值初始化为0
        self.Sn_contrast = 0
        self.Pb_contrast = 0
        self.Zn_contrast = 0

    def describe_sample(self):
        """
        输出一个样品的一些描述信息，包括样品号、高斯坐标、元素含量和类标号
        """
        print('id=%d' %self.sample_id)
        print('Gauss grid=(%lf,%lf)' %(self.XX,self.YY))
        print('W=%.2f, Sn=%.2f, Pb=%.2f, Zn=%.2f'%(self.W, self.Sn, self.Pb, self.Zn))
        print('Macro element content=',self.macro_element)
        print('Class_id = ',self.class_id)

    def dist(self, another_sample):
        """
        计算两个样品常量元素含量间的欧氏距离（二范数）
        :param another_sample: 另一个Sample类的实例
        :return: 两个Sample类实例常量元素含量的欧氏距离
        """
        v1 = np.array(self.macro_element)
        v2 = np.array(another_sample.macro_element)
        return np.linalg.norm(v1-v2)

    def is_adjacency(self,another_sample):
        """
        判断两个样品是否在高斯网格上相邻
        :param another_sample: 另一个Sample类的实例
        :return: 若两者相邻，返回True；否则返回False
        """
        v1 = np.array([self.XX, self.YY])
        v2 = np.array([another_sample.XX, another_sample.YY])
        edge = np.linalg.norm(v1-v2)
        if edge < Sample.max_edge:
            return True
        else:
            return False
