from scipy.stats import *
import numpy as np

class ElementList(list):
    '''
    用一个list存储某个元素的一系列含量，此外还添加了以下功能：
    记录元素名称
    剔除离群值
    检测元素含量值是否服从算数正态分布或对数正态分布
    计算剔除离群值之后的稳健均值和稳健均方差
    '''
    def __init__(self, element_name='', element_content=[]):
        list.__init__([])
        self.element_name = element_name
        self.extend(element_content)

    def robust_data(self, k=3):
        '''
        剔除一个元素含量list的离群点
        :param k: 置信区间为（c-k*s，c+k*s），k默认为3
        :return: 剔除离群值后的元素含量list
        '''
        origin_data = self
        robust_data = []
        len1 = len(origin_data)
        len2 = len(robust_data)
        while len1 > len2:
            c = np.array(origin_data).mean()
            s = np.array(origin_data).std(ddof=1)
            robust_data = list(filter(lambda x: x > c-k*s and x < c+k*s, origin_data))
            len1 = len(origin_data)
            len2 = len(robust_data)
            origin_data = robust_data
        return robust_data

    def robust_mean(self):
        '''
        计算一个元素含量list的稳健均值
        :return:
        '''
        return np.array(self.robust_data()).mean()

    def robust_std(self):
        '''
        计算一个元素含量序列的稳健均方差
        :return:
        '''
        return np.array(self.robust_data()).std(ddof=1)

    def distribution_pattern(self):
        '''
        正态检验，比较元素含量服从算数正态分布或对数正态分布的p值来判断
        :return: 若元素含量服从算数正态分布的概率更大，返回字符串'norm'；
                 否则认为其服从对数正态分布，返回字符串'lognorm'
        '''
        if shapiro(self.robust_data())[1] > shapiro(np.log(self.robust_data()))[1]:
            return 'norm'
        else:
            return 'lognorm'

    def c_a(self, k=2):
        if self.distribution_pattern() == 'norm':
            c = self.robust_mean()
            s = self.robust_std()
        else:
            u = np.log(self.robust_data()).mean()
            var = np.log(self.robust_data()).var(ddof=1)
            c = np.exp(u + var/2)
            s = np.sqrt(np.exp(2*u + var)*(np.exp(var) - 1))
        return c + k*s
