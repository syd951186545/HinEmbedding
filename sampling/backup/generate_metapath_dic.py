import sys
import os
import random
from collections import Counter

class Generate_MetaPath_Dict:
	def __init__(self):
		self.user_id = dict()
		self.movie_id = dict()
		self.genres_id = dict()

		self.user_userlist = dict()
		self.movie_movielist = dict()
		self.user_movielist = dict()
		self.movie_userlist = dict()
		self.movie_aspectlist = dict()
		self.aspect_movielist = dict()


	def read_data(self, dirpath):
		n_users = 6040
		n_movie = 3952
		n_genres = 18

		# user_user_list
		with open(dirpath + "user_user_list.csv") as user_user_file:
			for line in user_user_file:
				toks = line.strip().split("\t")
				user_0, user_1, sim = toks[0], toks[1], toks[2]
				if user_0 not in self.user_userlist:
					self.user_userlist[user_0] = []
				self.user_userlist[user_0].append([user_1, sim])
				if user_1 not in self.user_userlist:
					self.user_userlist[user_1] = []
				self.user_userlist[user_1].append([user_0, sim])


		# movie_movie_list
		with open(dirpath + "movie_movie_list.csv") as movie_movie_file:
			for line in movie_movie_file:
				toks = line.strip().split("\t")
				movie_0, movie_1, sim = toks[0], toks[1] , toks[2]
				if movie_0 not in self.movie_movielist:
					self.movie_movielist[movie_0] = []
				self.movie_movielist[movie_0].append([movie_1, sim])
				if movie_1 not in self.movie_movielist:
					self.movie_movielist[movie_1] = []
				self.movie_movielist[movie_1].append([movie_0, sim])

		# user_movie_list and movie_user_list
		with open(dirpath + "user_movie_rating_list.csv") as user_movie_file:
			for line in user_movie_file:
				toks = line.strip().split("\t")
				user, movie, rating = toks[0], toks[1] , toks[2]
				if user not in self.user_movielist:
					self.user_movielist[user] = []
				self.user_movielist[user].append([movie, rating])
				if movie not in self.movie_userlist:
					self.movie_userlist[movie] = []
				self.movie_userlist[movie].append([user, rating])

		# movie_aspect_list and aspect_moive_list
		with open(dirpath + "movie_genres_list.csv") as movie_genres_file:
			for line in movie_genres_file:
				toks = line.strip().split("\t")
				movie, aspect, includes = toks[0], toks[1], toks[2]
				if movie not in self.movie_aspectlist:
					self.movie_aspectlist[movie] = []
				self.movie_aspectlist[movie].append([aspect, includes])
				if aspect not in self.aspect_movielist:
					self.aspect_movielist[aspect] = []
				self.aspect_movielist[aspect].append([movie, includes])


	def generate_random_UUM(self, outfilename, numwalks, walklength):
		outfile = open(outfilename, 'w')
		uum_list = list()
		for user in self.user_userlist:
			user_0 = user
			for i in range(0, numwalks):
				outline = user_0
				for j in range(0, walklength):
					# user-user
					users = self.user_userlist[user_0]
					num_u = len(users)
					user_list_index = random.randrange(num_u)
					weight_0 = users[user_list_index][1]
					user_1 = users[user_list_index][0]
					outline += "-" + weight_0 + "-" + user_1

					# user-movie
					movies = self.user_movielist[user_1]
					num_m = len(movies)
					movie_list_index = random.randrange(num_m)
					weight_1 = movies[movie_list_index][1]
					movie_2 = movies[movie_list_index][0]
					outline += "-" + weight_1 + "-" + movie_2
				outfile.write(outline + "\n")
				uum_list.append(outline)
		outfile.close()
		return uum_list


	def generate_random_UMAM(self, outfilename, numwalks, walklength):

		return

	def generate_random_UUMM(self, outfilename, numwalks, walklength):

		return




dirpath = "E://PyCharmProjs//HIN//Data//"



numwalks = 10
walklength = 1


outfilename = dirpath+"UUM.csv"

def main():
	mpg = Generate_MetaPath_Dict()
	mpg.read_data(dirpath)
	mpg.generate_random_UUM(outfilename, numwalks, walklength)


if __name__ == "__main__":
	main()


