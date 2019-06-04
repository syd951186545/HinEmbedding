@整理的数据集 data
来自于../data_raw的原始数据集，处理后

：方便起见，异质数据要以csv格式存储便于使用pandas读取，同质网络以edgelist或adjlist存储
   csv文件中要有标题头如：
	author，     paper
	0，	1
	0，	2
   csv文件结尾以.edge,.label,.map表示边，标签，名称映射。
*********************************************************
异质网络可以转换为同质网络数据edgelist格式，使用..utils/HinData2EdgeFile.py 参数见该文件



