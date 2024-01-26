import json
import csv
import pickle


# 读取txt 文本
def read_txt(path):
    with open(path, "r") as f:
        data = f.readlines()
        f.close()
        return data

def write_json(path, json_str):
    f = open(path, 'w')
    f.write(json_str)
    f.close()


def read_json(path):
    with open(path, "r") as f:
        data = f.read()
        f.close()
        return data


def read_csv(path):
    with open(path, "r") as f:
        data = f.read()
        f.close()
        return data


def write_array(path, data):
    f = open(path, 'w')

    for d in data:
        sa = str(d) + "\n"
        f.write(sa)
    f.close


def read_array(path):
    data = []
    for line in read_txt(path):     
        line = line.strip('[')
        line = line.strip('\n')
        line = line.strip(']')
        d = line.split(',')   
        d = [float(x) for x in d]
        data.append(d)
    return data


def write_pkl(path, data):
    with open(path, 'wb') as file:
        pickle.dump(data, file)
    file.close()


def read_pkl(path):
    with open(path, 'rb') as file:
        loaded_data = pickle.load(file)
    file.close()
    return loaded_data
