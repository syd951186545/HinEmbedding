@整理的数据集 data
来自于../data_raw的原始数据集，处理后

：方便起见，数据要以csv格式存储便于使用pandas读取
   csv文件中要有标题头如：
	author，     paper
	0，	1
	0，	2
：方便起见，以pickle文件形式保存该数据的networkx.Graph类
（networkx.write_gpickle()/networkx.read_gpickle()）
*********************************************************
#同质网络
	edge.csv : 每一行代表一条边
	（例如标题头可以起名为node1 node2，表示两个节点之间存在边）

	nodec.csv:节点到编号的映射
	（例如标题头可以起名为node identifier）

	label.csv:节点到标签的映射
	（例如标题头可以起名为node label）

	info.txt：必要信息说明，包含节点数量，边数量，标签类别，标签数量等等
	（可以详细点，酌情添加）
#异质网络
	节点和关系比较复杂，能清晰的表示即可
	（可以参考我的1_DBLP数据集）



