import csv, sys, re
from DataBase import dbmodule

dbModule = dbmodule.Database()

class Week(object):
	def __init__(self,week):
		self.week = week
		self.foods = []

	def addFood(self,food):
		self.foods.append(food)

	def getWeek(self):
		return self.week

	def getFoods(self):
		return self.foods

class Food(object):
	def __init__(self, meal, nutrient):
		self.meal = meal
		self.nutrient = nutrient
	
	def getMeal(self):
		return self.meal

	def getNutrient(self):
		return self.nutrient

def load(fileName):
	file = open(fileName,'r')
	reader = csv.reader(file, delimiter=',')
	weeks = []
	count = 0
	for line in reader:
		if line[0]:
			if re.search(r'week',line[0]):
				count += 1
				weeks.append(Week(count))
				continue
			if weeks:
				weeks[count-1].addFood(Food(line[0], line[1]))
	for week in weeks:
		num = week.getWeek()
		values=""
		for food in week.getFoods():
			values += '(%s,"%s","%s"),'%(num, food.getMeal(),food.getNutrient())
		values=values.rstrip(',')
		dbModule.insertToDB("insert into foodList values %s"%values)

if __name__=="__main__":
	load(sys.argv[1])
