import matplotlib as plt
import pandas as pd
import numpy as np


def load_multi_data(number):
    temp = "sensor_sample_float_"
    source = "multi/" + temp + "0" + ".csv"
    dic = pd.read_csv(source)
    for i in range(1, number):
        cur = temp + str(i)
        source = "multi/" + cur + ".csv"
        dic_cur = pd.read_csv(source, names=['value_id', 'sensor_id', 'timestamp', 'value'])
        dic = pd.concat([dic, dic_cur])

    dic = prepare_time_multi(dic)
    return dic


def prepare_time_multi(multi):
    hour = pd.DatetimeIndex(multi["timestamp"]).hour
    minute = pd.DatetimeIndex(multi["timestamp"]).minute
    second = pd.DatetimeIndex(multi["timestamp"]).second
    multi['time'] = second + 60 * minute + 3600 * hour

    return multi


def load_aras(house, days):
    temp = "DAY_"
    names = [str(x) for x in range(0, 22)]
    dic = pd.read_csv("Aras/" + house + "/" + "DAY_1" + ".txt", sep=" ", names=names)
    dic['time'] = list(range(1, 86401))
    for i in range(2, days + 1):
        cur = temp + str(i)
        source = "Aras/" + house + "/" + cur + ".txt"
        day_cur = pd.read_csv(source, sep=" ", names=names)
        day_cur['time'] = list(range(1, 86401))
        dic = pd.concat([dic, day_cur])
    return dic
