# encoding:utf-8
import datetime as dt
from scipy.stats import norm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def _cashFlowCalc(termCoupon, strMaturityDate, strNowDate):
    # termCoupon票息 list   strMaturityDate 到期日  strNowDate现在的日期
    dtMaturityDate = dt.datetime.strptime(strMaturityDate, "%Y/%m/%d")
    dtNowDate = dt.datetime.strptime(strNowDate, "%Y/%m/%d")
    numPtmYears = (dtMaturityDate - dtNowDate).days / 365.0  # 计算剩余期限
    n = len(termCoupon)
    numDig, numRound = np.modf(numPtmYears)
    numPayment = int(np.min([numRound + 1, n]))  # 这三行是计算一下哪些票息，本金没付

    cashFlow = termCoupon[-numPayment:]
    cashFlowTime = np.arange(numPayment) + numDig
    # 返回 未来的现金流，和对应的时间，以年为单位
    return cashFlow, cashFlowTime


def _cashFlowDict(termCoupon, strMaturityDate, strNowDate):
    cashFlow, cashFlowTime = _cashFlowCalc(termCoupon, strMaturityDate, strNowDate)
    dictCF = {}
    for i, cash in enumerate(cashFlow):
        dictCF[round((i + 1) * 250)] = i
    return dictCF


def _pv(cashFlow, cashFlowTime, r):
    # 计算贴现现金流
    # 现金流，对应时间，R，算现值
    ret = 0
    for t, cash in enumerate(cashFlow):
        ret += cash / ((1 + r) ** cashFlowTime[t])
    return ret


def _pvCashFlowMC(thisRowEndTime, thisRowValue, dictCF, r):
    cfT = [thisRowEndTime];
    cf = [thisRowValue]
    for time in dictCF:
        if time / 250.0 < thisRowEndTime:
            cfT.append(time / 250.0)
            cf.append(dictCF[time])
    return _pv(cf, cfT, r)


def _monterCarlo(stock, vol, r, numNodes, numToMock=10000):
    # 模拟风险中性世界下的股价
    arrStock = np.ones([numToMock, numNodes + 1])
    dt = 1 / 250.0
    rc = np.log(1 + r)
    arrMock = np.cumprod(
        np.exp((rc - 0.5 * (vol ** 2)) * dt + vol * np.sqrt(dt) * np.random.randn(numToMock, numNodes)), axis=1)
    arrStock[:, 1:] = arrMock
    arrStock *= stock
    return arrStock


def _slicelnMC(array, point, lenth):
    return array[int(max([0, point - lenth])):int(point)]


def isRecall(arr, arrTimeSeries, recall_term):
    # 判断哪些点在赎回期内
    logicTime = np.array(arrTimeSeries[:]) < recall_term[0]
    # 判断哪些点的价格达到要求
    logicPrice = arr[:] > recall_term[-1]
    return 1 if np.sum(1 * logicTime * logicPrice) >= recall_term[1] else 0


def _isResell(arr, arrTimeSeries, resell_term):
    logicTime = np.array(arrTimeSeries[:]) < resell_term[0]
    logicPrice = arr[:] < resell_term[-2]
    return 1 if np.sum(1 * logicTime * logicPrice) >= resell_term[1] else 0


def _processResell(term, row, i, arrTimeSeries):
    if row[i] < term['Resell'][-2]:
        sliceArr = _slicelnMC(row, i, term['Resell'][2])
        sliceArrTimeSeries = _slicelnMC(arrTimeSeries, i, term['Resell'][2])
        isBeResell = _isResell(sliceArr, sliceArrTimeSeries, term['Resell'])
        if isBeResell:
            thisRowEndTime = i / 250.0
            thisRowValue = row[i]  # term["Resell"][-1]
        else:
            thisRowEndTime = None
            thisRowValue = None
        return isBeResell, thisRowEndTime, thisRowValue
    else:
        return None, None, None


def _isRecall(arr, arrTimeSeries, recall_term):
    logicTime = np.array(arrTimeSeries[:]) < recall_term[0]
    logicPrice = arr[:] > recall_term[-1]
    return 1 if np.sum(1 * logicTime * logicPrice) >= recall_term[1] else 0


def _processReCall(term, row, i, arrTimeSeries):
    if row[i] > term["Recall"][-1]:
        sliceArr = _slicelnMC(row, i, term["Recall"][2])
        sliceArrTimeSeries = _slicelnMC(arrTimeSeries, i, term["Recall"][2])
        isBeRecall = _isRecall(sliceArr, sliceArrTimeSeries, term["Recall"])
        if isBeRecall:
            thisRowEndTime = i / 250.0
            thisRowValue = row[i]
        else:
            thisRowEndTime = None
            thisRowValue = None
        return isBeRecall, thisRowEndTime, thisRowValue
    else:
        return None, None, None


def cbProcingMC(stock, term, now, vol, r, numToMock=10000):
    # 字典回吐每天的现金流
    dictCF = _cashFlowDict(term["Coupon"], term["Maturity"], now)
    numNodes = int(max(dictCF))
    arrTimeSeries = [(numNodes - i) / 250.0 for i in range(numNodes)]
    arrMC = _monterCarlo(stock, vol, r, numNodes, numToMock)
    v = []
    for row in arrMC:

        for i in range(numNodes):
            isBeRecall, thisRowEndTime, thisRowValue = _processReCall(term, row, i, arrTimeSeries)
            if isBeRecall:
                v.append(_pvCashFlowMC(thisRowEndTime, thisRowValue, dictCF, r))
                break
            isBeResell, thisRowEndTime, thisRowValue = _processResell(term, row, i, arrTimeSeries)
            if isBeResell:
                v.append(_pvCashFlowMC(thisRowEndTime, thisRowValue, dictCF, r))
                break
            else:
                thisRowEndTime = numNodes / 250.0
                thisRowValue = np.max([row[-1], term["Coupon"][-1]])
                v.append(_pvCashFlowMC(thisRowEndTime, thisRowValue, dictCF, r))
    x = [i for i in range(1, len(arrMC[0]))]
    for row in arrMC:
        plt.plot(x, row[1:])
    plt.show()
    return np.mean(v)


if __name__ == "__main__":
    term = {"ConvPrice": 6.66,
            "Maturity": "2025/3/7",
            "ConvertStart": 5.5,
            "Coupon": [0.4, 0.6, 1.5, 2.0, 2.5, 3.0, 116],
            "Recall": [6, 15, 30, 130],  # 存续期6年，如果公司股票连续30个交易日中至少有十五个交易日的收盘价不低于档期转股价格的%130
            "Resell": [2, 30, 30, 70, 103]  # 最后两个计息年度，连续30个交易日，收盘价格低于转股价的70%，按面值加上当期应计利息的价格回售给公司
            }  # 所以103这个参数没有意义
    stock = 5.77
    now = "2019/03/08"
    vol = 0.5917
    r = 0.0319
    print("上市当天的理论价值为，" + str(cbProcingMC(stock, term, now, vol, r)))

