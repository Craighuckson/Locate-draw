#python
from math import atan2
from math import degrees
def angle(x1,y1,x2,y2):
	delta_x = x2-x1
	delta_y = y1 - y2
	return atan2(delta_y,delta_x)

print(degrees(angle(8,10,10,12)))