# -*- coding: utf-8 -*-
import numpy as np
import geatpy as ea


class C3_DTLZ4(ea.Problem):  # 继承Problem父类
    def __init__(self, M=3, Dim=None):  # M : 目标维数；Dim : 决策变量维数
        name = 'C3-DTLZ4'  # 初始化name（函数名称，可以随意设置）
        maxormins = [1] * M  # 初始化maxormins（目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标）
        Dim = M + 9  # 初始化Dim（决策变量维数）
        varTypes = [0] * Dim  # 初始化varTypes（决策变量的类型，0：实数；1：整数）
        lb = [0] * Dim  # 决策变量下界
        ub = [1] * Dim  # 决策变量上界
        lbin = [1] * Dim  # 决策变量下边界（0表示不包含该变量的下边界，1表示包含）
        ubin = [1] * Dim  # 决策变量上边界（0表示不包含该变量的上边界，1表示包含）
        # 调用父类构造方法完成实例化
        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)

    def evalVars(self, Vars):  # 目标函数
        alpha = 100
        XM = Vars[:, (self.M - 1):]
        g = np.sum((XM - 0.5) ** 2, 1, keepdims=True)
        ones_metrix = np.ones((g.shape[0], 1))
        f = np.hstack(
            [np.fliplr(np.cumprod(np.cos(Vars[:, :self.M - 1] ** alpha * np.pi / 2), 1)), ones_metrix]) * np.hstack(
            [ones_metrix, np.sin(Vars[:, range(self.M - 2, -1, -1)] ** alpha * np.pi / 2)]) * (1 + g)
        # 计算违反约束程度矩阵的值
        CV = 1 - f**2 / 4 - (np.sum(f**2, axis=1, keepdims=True) - f**2)
        return f, CV

    def calReferObjV(self):  # 设定目标数参考值（本问题目标函数参考值设定为理论最优值，即“真实帕累托前沿点”）
        referenceObjV, ans = ea.crtup(self.M, 10000)  # 生成10000个在各目标的单位维度上均匀分布的参考点
        referenceObjV /= np.sqrt(
            np.sum(referenceObjV ** 2, 1, keepdims=True) - 3 / 4 * np.max(referenceObjV ** 2, 1, keepdims=True))
        return referenceObjV
