import hashlib
import random

x = "b"

f = hashlib.md5(x)
print(int(f.hexdigest(), 16))
f2 = hashlib.md5(x)
print(int(f.hexdigest(), 16))
h = hashlib.new('md5')
h.update(x)
print(int(h.hexdigest(), 16))

m = hashlib.md5()
m.update(x)
print(int(m.hexdigest(), 16))