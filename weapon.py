from setting import *
from sprite import Bullet

laser_sound=mixer.Sound("laser.mp3")
reload_sound=mixer.Sound("reload.mp3")

class Weapon:
	def __init__(self,sprites):
		self.sprites=sprites
		self.current_sprite=self.sprites["shoot"]
		self.index=0
		self.h_width=self.current_sprite[0].get_width()/2
		self.height=self.current_sprite[0].get_height()
		
		self.ammo_size=30
		self.ammo=self.ammo_size
	
	def update(self,p_pos,p_angle):
		screen.blit(self.current_sprite[int(self.index)],(
		Half_W-self.h_width,Height-self.height))
		self.index+=1#sprite_swap_rate
		
		shoot_index=2
		if self.index==shoot_index:
			p_bullet=Bullet(p_pos,p_angle,2)
			pre_sprite.append(p_bullet)
			bullet_group.append(p_bullet)
			self.ammo-=1
			
			laser_sound.play()
		
		if self.index>=len(self.current_sprite):
			self.index=0
			if self.current_sprite==self.sprites["reload"]:
				self.current_sprite=self.sprites["shoot"]
				self.ammo=self.ammo_size
			
			
		if self.ammo<=0:
			self.current_sprite=self.sprites["reload"
			]
			if self.index==shoot_index:
				reload_sound.play()

riffle_sprite=import_character("Riffle/")
riffle=Weapon(riffle_sprite)