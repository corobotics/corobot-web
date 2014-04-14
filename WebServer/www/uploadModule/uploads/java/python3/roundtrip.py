"""Simple example showing usage of the Corobot user API."""

from sys import argv

from corobot import Robot

from time import sleep

def callback():
    print("Made it!")

def errcall():
    print("uhoh")

def main():
    if len(argv) < 2:
        print("Usage: python3 roundtrip.py <landmark>")
        return
    with Robot("127.0.0.1", 15001) as r:
        #p = r.go_to_xy(5, 5).then(callback)
        pos = r.get_pos().get()
        r.display_message("Heading to "+argv[1])
        p = r.nav_to(argv[1]).then(callback,errcall)
        p.wait()
        r.request_confirm("Make me some coffee please!",30).wait()
        r.go_to_xy(pos[0],pos[1]).wait()

if __name__ == "__main__":
    main()
