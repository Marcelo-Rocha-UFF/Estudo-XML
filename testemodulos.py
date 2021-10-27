t = False

def lock():
	global t
	t = True

def unlock():
	global t
	t = False

print("t", id(t), t)

lock()

print("t", id(t), t)

unlock()

print("t", id(t), t)