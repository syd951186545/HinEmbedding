# -*- coding: UTF-8 -*-
import pandas as pd
import os

# 原始数据结构：
# 节点：电影，用户，标签，演员，导演，类型，地址，标签，国家，地点

# 处理思路：1.将所有元素一同加载，统一生成新ID建立映射（map）

cur_dir = "../data_raw/1_Movielens_raw"
target_dir = "../data/1_Movielens"

sep_sign = '\t'

# 节点字典，数据依据此字典进行相应处理，key值为节点名，value值是一个长字符，采用‘||’分为左右两部分，
# 左部记录该节点映射源格式为“来源文件-列名”；右部记录希望加入该节点映射的额外信息，例如节点的具体名字，多个列时可以用‘/’分开（要求文件中含有该节点的ID信息且名称一致）
nodes_dict = {
	"user": "user_ratedmovies.dat-userID",
	"movie": "movies.dat-movieID||movies.dat-title",
	"actor": "movie_actors.dat-actorID"
}

# edges_dict指示连接关系，其字典key为连接的两个节点名称，value指示连接来源
# value中长字符串使用||分为左右两部，由于连接关系来源于单个文件，所以左部由“记录连接关系的文件 key中左节点所在列名 key中右节点所在列名”构成
# 右部由该文件中存在的其他属性组成，用于补充连接的属性；也可以“其它文件名（同种连接关系且列名相同（数量和属性与本文件不同））-列名”作为一个项
edges_dict = {
	"user-movie": "user_ratedmovies.dat userID movieID||user_ratedmovies.dat-rating user_taggedmovies.dat-tagID",
	"movie-actor": "movie_actors.dat movieID actorID||movie_actors.dat-ranking"
}


# labels_dict指示节点和其欲保留的label(暂时未作)
labels_dict = {
	"movie": "movie_actors.dat-actorID"
}


# dataframe_dict: 辅助字典，记录每个使用到的文件的dataframe，为之后程序使用提供遍历
dataframe_dict = {}
# node_df_dict: 辅助字典，记录节点新旧ID映射的dataframe，用于之后edge的转换
node_df_dict = {}

# 为所有的节点统一建立映射关系（所有节点统一计算ID），并将映射后的文件分别保存在目标文件夹中
def build_map_of_all_nodes():
	# 首先对nodes_dict中的文件建立df对象，保存在dataframe_dict中，同时建立一个series，仅记录旧ID（用series的ID作为新的映射值），需追加的属性之后单独添加
	counter_id = 1
	for node in nodes_dict:
		sourceID = nodes_dict[node].split("||")[0].split("-")
		file_name = sourceID[0]
		old_id = sourceID[1]
		# 对nodes_dict中的文件建立df并保存
		if file_name not in dataframe_dict:
			dataframe_dict[file_name] = pd.read_csv(os.path.join(cur_dir, file_name), encoding="ISO-8859-1", sep=sep_sign)
		node_df = pd.DataFrame({old_id: dataframe_dict[file_name][old_id].drop_duplicates().values})
		new_ID = "new_" + node + "ID"
		node_df[new_ID] = range(counter_id, counter_id + len(node_df))
		counter_id += len(node_df)
		if len(nodes_dict[node].split("||")) == 2:
			labels = nodes_dict[node].split("||")[1].split("/")
			for label in labels:
				label_filename = label.split('-')[0]
				label_id = label.split('-')[1]
				if label_filename not in dataframe_dict:
					dataframe_dict[label_filename] = pd.read_csv(os.path.join(cur_dir, label_filename), encoding="ISO-8859-1", sep=sep_sign)
				node_df = node_df.join(dataframe_dict[label_filename][[old_id, label_id]].set_index(old_id), on=old_id)
		print(node_df)
		node_df_dict[node] = node_df
		save_file_name = node + "_csv.map"
		node_df.to_csv(os.path.join(target_dir, save_file_name), index=False, sep=sep_sign)


# 为节点建立连接关系，节点要求在nodes_dict中的key中，节点映射使用edges_dict进行指示(映射中使用的ID为映射后的新ID);主要工作为新旧ID转换
def build_edges_for_nodes():
	for connect in edges_dict:
		extra_attrs = {}
		node1 = connect.split('-')[0]
		node2 = connect.split('-')[1]
		source_connect = edges_dict[connect].split("||")[0]
		edge_file = source_connect.split(' ')[0]
		node1_id = source_connect.split(' ')[1]
		node2_id = source_connect.split(' ')[2]
		# 对edges_dict中的文件建立df并保存
		if edge_file not in dataframe_dict:
			dataframe_dict[edge_file] = pd.read_csv(os.path.join(cur_dir, edge_file), encoding="ISO-8859-1", sep=sep_sign)
		# df_keeped_columns:记录链接文件中需要保存的属性名，最基础的是两列ID
		df_keeped_columns = [node1_id, node2_id]
		df_final_columns = ['new_' + node1 + "ID", "new_" + node2 + "ID"]
		# 查看是否有连接关系的属性需要保留
		if len(edges_dict[connect].split("||")) == 2:
			attrs = edges_dict[connect].split("||")[1].split(' ')
			for attr in attrs:
				attr_file = attr.split('-')[0]
				attr_id = attr.split('-')[1]
				df_final_columns.append(attr_id)
				if attr_file == edge_file:
					df_keeped_columns.append(attr_id)
				else:
					if attr_file not in extra_attrs:
						extra_attrs[attr_file] = []
					extra_attrs[attr_file].append(attr_id)
		# 将连接关系保留，仅保留单个连接关系（若存在重复）
		edge_df = dataframe_dict[edge_file][df_keeped_columns].drop_duplicates()
		# 将edge_df中的id替换为映射出的新id，使用两次join函数最后仅保留新的ID关系对
		node1_df = node_df_dict[node1]
		node2_df = node_df_dict[node2]
		edge_df = edge_df.join(node1_df.set_index(node1_id), on=node1_id)
		edge_df = edge_df.join(node2_df.set_index(node2_id), on=node2_id)
		if extra_attrs:
			for attr_file in extra_attrs:
				if attr_file not in dataframe_dict:
					dataframe_dict[attr_file] = pd.read_csv(os.path.join(cur_dir, attr_file), encoding="ISO-8859-1", sep=sep_sign)
				# 根据edge_df中旧ID添加不同文件中的属性列
				edge_df = edge_df.merge(dataframe_dict[attr_file], on=[node1_id, node2_id], how='left')
		# print(edge_df)
		edge_df = edge_df[df_final_columns]
		print(edge_df)
		save_file_name = node1 + "_" + node2 + "_csv.edge"
		edge_df.to_csv(os.path.join(target_dir, save_file_name), index=False, sep=sep_sign)

if __name__ == "__main__":
	build_map_of_all_nodes()
	build_edges_for_nodes()
