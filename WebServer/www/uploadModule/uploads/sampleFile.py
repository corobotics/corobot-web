import sys
from corobot import Robot

def main(argv):
	if (len(argv) < 2):
		way_point = "PatternLab"
	else:
		way_point = argv[1]
	with Robot() as r:
		r.nav_to (way_point).wait()

if __name__ == "__main__":
	main (sys.argv)