#!/usr/bin/env python
# coding=utf-8

import json

import pandas as pd
import errno
def auto_json_gen(input_file, sheet_name, output_file, param={}):
    """ json自动生成函数
    :param input_file: 输入xlsx名称
    :param sheet_name: 输入sheet名称
    :param output_file: 输出Json文件名
    :param param: 指定某些字段的解析类型（默认为int）
    指定形式为：例如：award字段设置为浮点型的数据，则传入{"award": float}
    label_name字段设置为字符串，则传入{"label_name": str}
    """
    print("generating >> from : %s - %s =>> %s" % (input_file, sheet_name, output_file))
    try:
        data = pd.read_excel(input_file, sheet_name=sheet_name)
    except OSError as e:
        if e.errno == errno.ENOENT:
            print("%s not exist!" % input_file)
            return

    data_list = []
    keys = data.keys()
    for index, row in data.iterrows():
        temp_dic = dict()
        for key in keys:
            if key in param:
                if param[key] == list:
                    # print(key, row[key])
                    tmp_list = list()
                    for line in json.loads(str(row[key])):
                        tmp_dict = dict()
                        inner_keys = line.keys()
                        for inner_key in inner_keys:
                            tmp_dict[inner_key] = line[inner_key]
                        tmp_list.append(tmp_dict)
                    temp_dic[key] = tmp_list
                else:
                    temp_dic[key] = param[key](row[key])
            else:
                try:
                    temp_dic[key] = int(row[key])
                except:
                    print("err ingoried %s" % row[key])
        data_list.append(temp_dic)
    # print(data_list)
    json_file = open(output_file, 'w')
    json_file.write(json.dumps(data_list, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': ')))
    json_file.close()

