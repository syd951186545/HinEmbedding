B238-异质信息网络表示
./data_raw 下载的原始数据存放位置
./data  处理后的数据存放位置
./baseline 存放baseline方法源码
./embedding 存放生成的embedding文件
**************************************************************************
!同质网络!  可以直接运行Main.py 主要需要以下三个参数：
--input 主要为edgelist或者adjlist文件格式
--output 生成文件路径（包含名称），请存放于embedding文件中
--method 有如下几种：
'node2vec','deepWalk','line''gcn','grarep','tadw', 'lle','hope','lap','gf','sdne'
#其余参数详见Main.py中

!异质网络!  可以转换为同质网络数据edgelist格式，之后直接运行Main.py如上
# 转换使用.utils/HinData2EdgeFile.py 参数见该文件

!数据集格式转换!   可以对原始数据集的指定节点重新统一编号并保存映射，可以记录映射后的节点连接关系
# 转换使用.utils/trans_data_raw.py  设置参数为文件中nodes_dict和edges_dict两个字典
