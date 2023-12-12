def func2():
    print(x)

def func1():
    global x
    x = 1
    
func1()
func2()