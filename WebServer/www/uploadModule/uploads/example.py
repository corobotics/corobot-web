"""Simple example showing usage of the Corobot user API."""

from corobot import Robot

def callback():
    print("arrived!")

def main():
    """Test out simple API stuff."""
    with Robot("129.21.69.34", 15001) as r:
        p = r.nav_to("Office3515").then(callback)
        p.wait()
        print("fin")

main()
