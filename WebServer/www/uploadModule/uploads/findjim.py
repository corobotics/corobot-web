import sys
from corobot import Robot

def main(argv):
    with Robot() as r:
        r.nav_to("Office3515").wait()
        r.display_message("Hello Prof. Heliotis",15)
        r.nav_to("RNDLab").wait()

if __name__ == "__main__":
    main (sys.argv)
