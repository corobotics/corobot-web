from sys import argv
from corobot import Robot

def main (argv):
    ip = argv[1]
    way_point = argv[2]
    with Robot(ip,15001) as r:
        r.nav_to (way_point).wait()

if __name__ == '__main__':
    main(sys.argv)