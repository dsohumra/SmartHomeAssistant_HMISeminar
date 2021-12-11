import matplotlib as plt
import pandas as pd
import numpy as np


def load_multi_data(number):
    '''
    :param number: number of splitted file to use
    :return: dataframe
    '''

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
    '''
    :param house: "HouseA" or "HouseB"
    :param days:  how many days you want to load, 1 day = 86400 lines
    :return: dataframe
    '''
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
    dic = remove_sensors_not_used(dic, house)
    dic = remove_rows_Aras(dic)
    return dic


def remove_sensors_not_used(df, house):
    '''
    :param df: dataframe
    :param house: specify "HouseA" or "HouseB"
    :return: dataframe only with the usable sensor
    '''

    if house == "HouseA":
        return remove_sensors_HouseA(df)
    else:
        return remove_sensors_HouseB(df)


def remove_sensors_HouseA(df):
    '''
    :param df: df
    :return: df with sensor: 4,5,8,12,13,14,16,17,18,20
    '''
    sensors_keep = np.array(["3", "4", "7", "11", "12", "13", "15", "16", "17", "19", "20", "21", "time"])
    return df.loc[:, sensors_keep]


def remove_sensors_HouseB(df):
    '''
    :param df: df
    :return: df with sensor:
    '''
    sensors_keep = np.array(["2", "5", "6", "10", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "time"])
    return df.loc[:, sensors_keep]

def remove_rows_Aras(df):
    '''
    :param df: Aras: HouseA or HouseB
    :return: df without duplicate rows
    '''
    cur = df.iloc[0,:]
    for index,row in df.iterrows():
        if index == 0:
            pass
        else:
            pre = cur
            cur = row
            comp = cur[:-1] == pre[:-1]
            if comp.all():
                df = df.drop([index-1])
    return df