"""Simple example showing usage of the Corobot user API."""

from sys import argv

from corobot import Robot

def main():
    if len(argv) < 2:
        print("Usage: python3 nav_to.py <landmark>")
        return
    with Robot("127.0.0.1", 15001) as r:
        #p = r.go_to_xy(5, 5).then(callback)
        print(r.get_pos().get())
        r.nav_to(argv[1])

if __name__ == "__main__":
    main()
