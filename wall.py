from setting import *
from pymunk import Body,Poly,Circle
from random import randint

walls_png=import_sprite("walls/")

class Poly_wall(Poly):
	def __init__(self,body,ver):
		super().__init__(body,ver)
		self.texture=0

class Wall:
	def __init__(self,x,y):
		
		self.body=Body(1,100,Body.STATIC)
		self.body.position=x,y
		self.shape=Poly_wall.create_box(self.body,(100,100))
		self.shape.filter=ShapeFilter(0b00010,0b11111)
		self.shape.collision_type=5
		self.shape.texture=transform.scale(walls_png[randint(0,len(walls_png)-1)],(256,256))
		space.add(self.body,self.shape)