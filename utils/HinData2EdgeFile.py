import os
import pandas as pd

dir = "../data/"


def hinData2edgeFile(datasetFolder, edgelistFile, labelFile):
    """
    将异质网络数据转换为同质网络数据并以.edgelist的格式存储，同时存储.label文件

    :param datasetFolder: 异质网络数据集所在的@！文件夹路径！例如 "1_DBLP"
    文件夹中文件名称无所谓，文件后缀需满足../data中的规范，即（边文件.edge，标签文件.label，名称映射文件.map）
    :param edgelistFile:转换后的edgelist存储文件路径
    :param labelFile:转换后的label存储文件路径
    :return:None
    """
    folder = dir + datasetFolder
    for _, _, files in os.walk(folder, topdown=False):
        for file in files:
            if os.path.splitext(file)[1] == ".edge":
                pd_data = pd.read_csv(folder + "/" + file)
                indexx = pd_data.columns
                if len(indexx) > 2:
                    with open(edgelistFile, "a") as ef:
                        for ID1, ID2, Weight in zip(pd_data[indexx[0]], pd_data[indexx[1]], pd_data[indexx[2]]):
                            ef.write(str(ID1) + " " + str(ID2) + " " + str(Weight))
                            ef.write("\n")
                else:
                    with open(edgelistFile, "a") as ef:
                        for ID1, ID2 in zip(pd_data[indexx[0]], pd_data[indexx[1]]):
                            ef.write(str(ID1) + " " + str(ID2))
                            ef.write("\n")
            if os.path.splitext(file)[1] == ".label":
                pd_data2 = pd.read_csv(folder + "/" + file)
                indexx = pd_data2.columns
                with open(labelFile, "a") as lf:
                    for ID, Label in zip(pd_data2[indexx[0]], pd_data2[indexx[1]]):
                        lf.write(str(ID) + " " + str(Label))
                        lf.write("\n")
    return 0


if __name__ == "__main__":
    datasete = "1_DBLP"
    a = hinData2edgeFile(datasete, "../data/1_DBLP.edgelist", "../data/1_DBLP.label")
