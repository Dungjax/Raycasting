from pygame import display,image,font,SCALED,FULLSCREEN,time,transform,gfxdraw,mixer
from pymunk import Space,ShapeFilter
from pymunk.pygame_util import DrawOptions
from os import walk
#screen setup
Width=display.Info().current_w//8
Height=display.Info().current_h//8
Half_W=Width//2
Half_H=Height//2
screen=display.set_mode((Width,Height), SCALED | FULLSCREEN)
#color
grey=(50,50,50)
red=(255,0,0)
green=(0,255,0)
black=(0,0,0)
#font & text
font=font.Font(None,20)
def cre_text(name,x,y):
	text=font.render(str(name),1,red)
	screen.blit(text,(x,y))
#image
def import_sprite(folder):
	for _,__,img in walk(folder):
		return [image.load(folder+i).convert_alpha() for i in img]

def import_character(folder):
	l={}
	for name,__,fold in walk(folder):
		if len(fold)!=0:
			sprite=[image.load(name+"/"+img).convert_alpha() for img in fold]
			l[name.split("/")[1]]=sprite
	return l
		
#time
clock=time.Clock()
sprite_swap_rate=0.25
#pymunk setup
space=Space()
options=DrawOptions(screen)
pre_sprite=[]
chracter_group=[]
bullet_group=[]