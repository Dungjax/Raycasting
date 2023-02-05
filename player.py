from setting import *
from pymunk import Body,Circle
from math import atan2,sin,cos,tau
from sprite import Bullet
from weapon import riffle

shotgun_sprite=import_sprite("shotgun/")

class Player:
	def __init__(self):
		self.move_angle=0
		self.is_move=0
		self.speed=10
		self.health=100
		
		self.shoot=0
		#physic
		self.body=Body(1,1)
		self.body.position=-100,0
		self.shape=Circle(self.body,10)
		self.shape.filter=ShapeFilter(0b00001,0b01000)
		self.shape.collision_type=1
		space.add(self.body,self.shape)
		#sprite
		self.weapon=riffle
		self.seg_query=None
		
		self.dx,self.dy=0,0
	
	def get_input(self,down,left_finger,joystick,slide_motion,slide_up):
		if down:
			if left_finger[0]<Half_W:
				self.is_move=1 
				self.move_angle=atan2(left_finger[0]-joystick[0],left_finger[1]-joystick[1])
			
			self.body.angle=(slide_motion+slide_up)/100%tau
		else:
			if left_finger[0]==Half_W:
				self.is_move=0
	
	def update(self):
		self.seg_query=space.segment_query_first(self.body.position,(
		self.body.position[0]-60*cos(self.move_angle-self.body.angle),
		self.body.position[1]+60*sin(self.move_angle-self.body.angle)),1,ShapeFilter(mask=ShapeFilter().ALL_MASKS()^0b01011))
		
		if self.is_move==1:
			self.dx=-self.speed*cos(self.move_angle-self.body.angle)
			self.dy=self.speed*sin(self.move_angle-self.body.angle)
			mx=0
			my=0
			if self.seg_query!=None:
				if self.body.position[0]+self.dx<self.seg_query.point.x:
					mx+=self.dx
				if self.body.position[1]+self.dy<self.seg_query.point.y:
					my+=self.dy
			else:
				mx+=self.dx
				my+=self.dy
			self.body.position+=mx,my
		self.body.velocity=self.body.velocity[0]/2,self.body.velocity[1]/2
				
		self.weapon.update(self.body.position,self.body.angle)
		