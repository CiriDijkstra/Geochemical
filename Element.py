from scipy.stats import *
import numpy as np


class ElementList(list):
    """
    用一个list存储某个元素的一系列含量，此外还添加了以下功能：
    记录元素名称
    剔除离群值
    检测元素含量值是否服从算数正态分布或对数正态分布
    计算剔除离群值之后的稳健均值和稳健均方差
    根据元素含量服从正态分布或算术正态分布用不同的公式计算其背景上限
    """
    def __init__(self, element_name='', element_content=[]):
        """
        :param element_name: 该元素的名称，字符串
        :param element_content: 该元素的含量序列
        """
        list.__init__([])
        self.element_name = element_name
        self.extend(element_content)

    def robust_data(self, k=3):
        """
        用逐步截尾法剔除一个元素含量list的离群点
        :param k: 置信区间为（c-k*s，c+k*s），k默认为3
        :return: 剔除离群值后的元素含量list
        """
        origin_data = self
        robust_data = []
        len1 = len(origin_data)
        len2 = len(robust_data)
        while len1 > len2:
            c = np.array(origin_data).mean()
            s = np.array(origin_data).std(ddof=1)
            robust_data = list(filter(lambda x: c-k*s < x < c+k*s, origin_data))
            len1 = len(origin_data)
            len2 = len(robust_data)
            origin_data = robust_data
        return robust_data

    def robust_mean(self):
        """
        计算一个元素含量list的稳健均值
        :return: 该元素序列的稳健均值（算术正态分布）
        """
        return np.array(self.robust_data()).mean()

    def robust_std(self):
        """
        计算一个元素含量序列的稳健均方差
        :return: 该元素含量序列的稳健均方差（算术正态分布）
        """
        return np.array(self.robust_data()).std(ddof=1)

    def distribution_pattern(self):
        """
        正态检验，比较元素含量服从算数正态分布或对数正态分布的p值来判断
        :return: 若元素含量服从算数正态分布的概率更大，返回字符串'norm'；
                 否则认为其服从对数正态分布，返回字符串'lognorm'
        """
        if kstest(self.robust_data(), 'norm')[1] > kstest(np.log(self.robust_data()), 'norm')[1]:
            return 'norm'
        else:
            return 'lognorm'

    def c_a(self, k=2):
        """
            计算一个元素序列的背景上限，根据不同的分布模式采用不同的公式（正态分布或对数正态分布）
        :param k: 背景上限定义为均值+k倍均方差，k值默认为2
        :return: 该元素序列的背景上限
        """
        if self.distribution_pattern() == 'norm':
            c = self.robust_mean()
            s = self.robust_std()
        else:
            u = np.log(self.robust_data()).mean()
            var = np.log(self.robust_data()).var(ddof=1)
            c = np.exp(u + var/2)
            s = np.sqrt(np.exp(2*u + var)*(np.exp(var) - 1))
        return c + k*s
