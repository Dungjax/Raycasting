from setting import *
from math import sin,cos,atan2,dist
from pymunk import Body,Circle,Poly
from random import randint

bullet_sprite=import_sprite("bullets/")

class Object_render:
	def __init__(self,image,rx,ry,depth):
		self.image=image
		self.ren_pos=rx,ry
		self.depth=depth

class Sprite_render:
	def __init__(self,sprite,pos):
		self.image_index=0
		
		self.sprite=sprite
		self.image=self.sprite[self.image_index]
		
		self.body=Body(1,100)
		self.body.position=pos
		self.shape=Poly.create_box(self.body,(150,1))
		self.shape.filter=ShapeFilter(0b01000,0b01110)
		space.add(self.body,self.shape)

class Bullet(Sprite_render):
	def __init__(self,pos,p_angle,collision_type):
		super().__init__(bullet_sprite,pos)
		self.body.angle=p_angle
		self.body.apply_impulse_at_local_point((8000,0))
		self.shape.collision_type=collision_type
		self.p_pos=pos
		self.size_scale=0.2
		self.height_shift=0.75
	
	def update(self):
		depth=dist(self.body.position,self.p_pos)
		if depth>5000:
			space.remove(self.body,self.shape)
			pre_sprite.remove(self)
			bullet_group.remove(self)
			
		self.image_index+=sprite_swap_rate
		if self.image_index>=len(self.sprite):
			self.image_index=0
		self.image=self.sprite[int(self.image_index)]
		
class Enemy:
	def __init__(self,sprites,size,scale,height_shift,attack_dist):
		self.image_index=0
		
		self.sprites=sprites
		self.current_sprite=self.sprites["walk"]
		self.image=self.current_sprite[self.image_index]
		self.size_scale=scale
		self.height_shift=height_shift
		self.depth=0
		
		self.body=Body(1,100)
		self.body.position=randint(0,10000),randint(0,10000)
		self.shape=Circle(self.body,size)
		self.shape.filter=ShapeFilter(0b00100,0b01110)
		self.shape.collision_type=3
		space.add(self.body,self.shape)
		
		self.speed=randint(6,10)
		self.attack_dist=attack_dist
		self.pain=0
		self.health=randint(100,200)
		
		self.seg_query=0
	
	def update(self,p_pos):
		if self.health>0:
			self.seg_query=space.segment_query_first(self.body.position,p_pos,1,ShapeFilter(mask=ShapeFilter().ALL_MASKS()^0b01111))
			self.body.angle=atan2(p_pos[1]-self.body.position[1],p_pos[0]-self.body.position[0])
			
			if self.seg_query!=None or self.depth>self.attack_dist and self.pain==0:
				self.body.position+=self.speed*cos(self.body.angle),self.speed*sin(self.body.angle)
				self.current_sprite=self.sprites["walk"]
			 
			else:
				self.current_sprite=self.sprites["attack"]
			
			if self.pain==1:
				self.current_sprite=self.sprites["pain"]
		else:
			self.current_sprite=self.sprites["death"]
				
		self.image_index+=sprite_swap_rate
		
		if self.image_index>=len(self.current_sprite):
			
			if self.current_sprite==self.sprites["attack"]:
				e_bullet=Bullet(self.body.position,self.body.angle,4)
				pre_sprite.append(e_bullet)
				bullet_group.append(e_bullet)
			
			if self.current_sprite==self.sprites["pain"]:
				self.pain=0
			if self.current_sprite==self.sprites["death"]:
				pre_sprite.remove(self)
				chracter_group.remove(self)
				space.remove(self.shape,self.body)
			self.image_index=0
		self.image=self.current_sprite[int(self.image_index)]
		
		self.body.velocity=self.body.velocity[0]/2,self.body.velocity[1]/2
		