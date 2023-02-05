from pygame import init,event,FINGERDOWN,FINGERMOTION,FINGERUP,gfxdraw,transform,BLEND_RGBA_MULT
init()

from setting import *
from player import Player
from wall import Wall
from sprite import Object_render,Enemy
from math import sin,cos,pi,dist,atan2,tau,degrees
from random import randint

FPS=30

NUM_RAY=150
Half_NUM_RAY=NUM_RAY//2
FOV=pi/3
HALF_FOV=FOV/2
RAY_STEP=FOV/NUM_RAY
SCALE=Width//NUM_RAY
MAX_DEPTH=10000
WALL_HEIGHT_COEFF=25000

TEXTURE_SIZE=256
H_TEXTURE_SIZE=TEXTURE_SIZE//2
TEXTURE_STEP=TEXTURE_SIZE/100

floor=transform.scale(image.load("floor.png"),(Width,Half_H)).convert()
ceiling=transform.scale(image.load("ceiling.png"),(Width,Half_H)).convert()

wargrin_sprite=import_character("wargrin/")

harubus_sprite=import_character("harubus/")

bug_sprite=import_character("bug/")

droid_sprite=import_character("droid/")

class Game:
	def __init__(self):
		self.player=Player()
		#touch
		self.finger_pos=[0,0]
		self.left_finger_pos=[Half_W,Half_W]
		self.right_finger_pos=[Half_W,Half_W]
		self.right_fingerd_pos=[0,0]
		
		self.joystick_pos=[int(Width/8),int(Height//1.4)]
		self.slide_up=0
		self.slide_motion=0
		#wall setup
		for i in range(1000):
			Wall(randint(-50,50)*100,randint(-50,50)*100)
		
	def get_input(self):
		for ev in event.get():
			if ev.type==FINGERDOWN:
				if ev.x*Width>Half_W:
					self.right_fingerd_pos[0]=ev.x*Width
					self.right_fingerd_pos[1]=ev.y*Height
					
			if ev.type==FINGERDOWN or ev.type==FINGERMOTION:
				self.finger_pos[0]=ev.x*Width
				self.finger_pos[1]=ev.y*Height
				
				if ev.x*Width<Half_W:
					self.left_finger_pos[0]=ev.x*Width
					self.left_finger_pos[1]=ev.y*Height
				
				if ev.x*Width>Half_W:
					self.right_finger_pos[0]=ev.x*Width
					self.right_finger_pos[1]=ev.y*Height
					
					self.slide_motion=self.right_finger_pos[0]-self.right_fingerd_pos[0]
					
			if ev.type==FINGERUP:
				if ev.x*Width<Half_W:
					self.left_finger_pos[0]=Half_W
					self.left_finger_pos[1]=Half_W
				
				if ev.x*Width>Half_W: 
					self.right_finger_pos[0]=Half_W
					self.right_finger_pos[1]=Half_W
					self.right_fingerd_pos[0]=Half_W
					self.right_fingerd_pos[1]=Half_W
					
					self.slide_up+=self.slide_motion
					self.slide_motion=0
					
			self.player.get_input(ev.type==FINGERDOWN or ev.type==FINGERMOTION,self.left_finger_pos,self.joystick_pos,self.slide_motion,self.slide_up)
	
	def draw(self):
		screen.fill((15,15,15))
		sky_offset=-5*degrees(self.player.body.angle)%Width
		screen.blit(ceiling,(sky_offset,0))
		if sky_offset>0:
			screen.blit(ceiling,(sky_offset-Width,0))
			
		#screen.blit(floor,(0,Half_H))
		
		#wall 
		start_angle=self.player.body.angle-HALF_FOV
		render_soft=[]
		for ray in range(NUM_RAY):
			seg_query=space.segment_query_first(self.player.body.position,(self.player.body.position[0]+MAX_DEPTH*cos(start_angle),self.player.body.position[1]+MAX_DEPTH*sin(start_angle)),1,ShapeFilter(mask=ShapeFilter().ALL_MASKS()^0b01111))
			if seg_query!=None:
				
				depth_v=abs((seg_query.point.x-self.player.body.position[0])/cos(start_angle))
				depth_h=abs((seg_query.point.y-self.player.body.position[1])/sin(start_angle))
				
				depth=min((depth_v,depth_h))*cos(self.player.body.angle-start_angle)+1
		
				project_height=int(WALL_HEIGHT_COEFF/depth)
				
				offset=int(seg_query.point.x-50)%100 if depth_v<depth_h else int(seg_query.point.y-50)%100
				
				if project_height<Height:
					w1=transform.scale(seg_query.shape.texture.subsurface(offset*TEXTURE_STEP,0,TEXTURE_STEP,TEXTURE_SIZE),(SCALE,project_height)).copy()
				
					y_render=Half_H-project_height//2
				
				else:
					texture_height=TEXTURE_SIZE*Height//project_height
					y_render=0
					try:
						w1=transform.scale(seg_query.shape.texture.subsurface(offset*TEXTURE_STEP,H_TEXTURE_SIZE-texture_height//2,TEXTURE_STEP,texture_height),(SCALE,Height))
					except ValueError:
						raise Exception([offset*TEXTURE_STEP,H_TEXTURE_SIZE-texture_height//2,TEXTURE_STEP,texture_height,offset])
				
				a=255//(20/project_height+1)
				w1.fill((a,a,a,255),None,BLEND_RGBA_MULT)
				
				render_soft.append(Object_render(w1,ray*SCALE,y_render,depth))
				
			start_angle+=RAY_STEP
		#sprite
		for sprite in pre_sprite:
			sprite.depth=dist(sprite.body.position,self.player.body.position)
			render_soft.append(sprite)
		#soft render
		for r in sorted(render_soft,key=lambda r:r.depth,reverse=1):
			if r.__class__==Object_render:
				screen.blit(r.image,r.ren_pos)
			else:
				r_angle=atan2(r.body.position[1]-self.player.body.position[1],r.body.position[0]-self.player.body.position[0])
				delta_angle=self.player.body.angle-r_angle
				
				if delta_angle>pi:
					delta_angle-=tau
				
				delta=delta_angle/RAY_STEP
				if -Half_NUM_RAY<delta<Half_NUM_RAY:
					image_size=int(WALL_HEIGHT_COEFF/r.depth*r.size_scale)
					image_sizex=image_size*r.image.get_width()//100
					image_sizey=image_size*r.image.get_height()//100
					
					if image_size<500:
						ren_image=transform.scale(r.image,(image_sizex,image_sizey))
						 
					else:
						ren_image=transform.scale(r.image,(0,0))
					ren_posx=(Half_NUM_RAY-delta)*SCALE-ren_image.get_width()/2
					ren_posy=Half_H-ren_image.get_height()/2*r.height_shift
					
					screen.blit(ren_image,(ren_posx,ren_posy))
		
		gfxdraw.circle(screen,self.joystick_pos[0],self.joystick_pos[1],2,red)
		gfxdraw.circle(screen,Half_W,Half_H,1,green)
		#space.debug_draw(options)
		#cre_text(clock.get_fps(),0,25)
		#if self.player.seg_query!=None:
		#	cre_text(self.player.seg_query.point,0,0)
	
	def respawn_enemy(self):
		if len(chracter_group)<20:
			
			wargrin=Enemy(wargrin_sprite,26,0.75,0.1,600)
			harubus=Enemy(harubus_sprite,30,1.5,0.8,500)
			
			bug=Enemy(bug_sprite,30,0.75,1,500)
			
			droid=Enemy(droid_sprite,30,1,1,500)
			
			enemys=[droid,bug,harubus,wargrin]
			cy=enemys[randint(0,len(enemys)-1)]
			pre_sprite.append(cy)
			chracter_group.append(cy)
					
	def update(self):
		self.player.update()
		for character in chracter_group:
			character.update(self.player.body.position)
		
		for bullet in bullet_group:
			bullet.update()
		
		self.respawn_enemy()
		space.step(1/60)
	
	def p_bullet_collide_enemy(self,arbiter,space,data):
		
		for bullet in bullet_group:
			if arbiter.shapes[0]==bullet.shape:
				bullet_group.remove(bullet)
				pre_sprite.remove(bullet)
				space.remove(arbiter.shapes[0],arbiter.shapes[0].body)
		
		for enemy in chracter_group:
			if arbiter.shapes[1]==enemy.shape:
				if enemy.health>0 and enemy.seg_query==None:
					enemy.pain=1
					enemy.image_index=0
					enemy.health-=50
				
		return True
	
	def p_bullet_collide_wall(self,arbiter,space,data):
		for bullet in bullet_group:
			if arbiter.shapes[0]==bullet.shape:
				bullet_group.remove(bullet)
				pre_sprite.remove(bullet)
				space.remove(arbiter.shapes[0],arbiter.shapes[0].body)
		return True
	
	def e_bullet_collide_p(self,arbiter,space,data):
		for bullet in bullet_group:
			if arbiter.shapes[0]==bullet.shape:
				bullet_group.remove(bullet)
				pre_sprite.remove(bullet)
				space.remove(arbiter.shapes[0],arbiter.shapes[0].body)
		
		if arbiter.shapes[1]==self.player.shape:
			self.player.health-=50
				
		return True
	
	def e_bullet_collide_wall(self,arbiter,space,data):
		for bullet in bullet_group:
			if arbiter.shapes[0]==bullet.shape:
				bullet_group.remove(bullet)
				pre_sprite.remove(bullet)
				space.remove(arbiter.shapes[0],arbiter.shapes[0].body)
		return True
	
	def loop(self):
		while 1:
			space.add_collision_handler(2,3).begin=self.p_bullet_collide_enemy
			
			space.add_collision_handler(2,5).begin=self.p_bullet_collide_wall
			
			space.add_collision_handler(4,1).begin=self.e_bullet_collide_p
			
			space.add_collision_handler(4,5).begin=self.p_bullet_collide_wall
			
			clock.tick(FPS)
			self.get_input()
			self.draw()
			self.update()
			display.update()

if __name__=="__main__":
	game=Game()
	game.loop()