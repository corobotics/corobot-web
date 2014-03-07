from corobot import Robot
way_point = "PatternLab"
with Robot() as r:
	r.nav_to (way_point).wait()