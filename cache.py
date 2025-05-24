import os, json, time
time.time()

#not in use
def check(method, loc) -> bool:
    print("running check")
    with open("cache.json", "r+") as file:
        cache = json.load(file)
        meth = cache[method]
        t = (time.time() - meth[loc]['location']['localtime_epoch'] )<(900 - meth[loc]['location']['localtime_epoch']%900)
        print(t)
        if loc in meth and t:
            return True
        else: 
            return False

def get(method, loc):
    print("running get")
    with open("cache.json", "r") as file:
        cache = json.load(file)
        meth = cache[method]
        if loc in meth:
            if (time.time()>meth[loc][method]['last_updated_epoch']+900): return {}
            return meth.get(loc)
        else: 
            return {}

def store(method, loc, r):
    print("running store")
    with open("cache.json", "r") as file:
        f = json.load(file)
    with open("cache.json", "w") as file:
        if not f: f = {method:{}}
        f[method][loc] = r
        file.write(json.dumps(f, indent= 4))