B238-异质信息网络表示
./data_raw 下载的原始数据存放位置
./data  处理后的数据存放位置

同质网络可以直接运行Main.py --input ,--output ,--methon 主要需要这三个参数
method 有如下几种。
'node2vec','deepWalk','line''gcn','grarep','tadw', 'lle','hope','lap','gf','sdne'

异质网络可以转换为同质网络数据edgelist格式，使用.utils/HinData2EdgeFile.py 参数见该文件
之后直接运行Main.py如上

