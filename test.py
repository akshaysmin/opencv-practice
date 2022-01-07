import numpy as np

origin = np.array((345,180))

pt1 = np.array((347,236)) - origin
pt2 = np.array((456,191)) - origin
pt3 = np.array((570,314)) - origin
pt4 = np.array((457,373)) - origin

print(f'pt1 = {pt1}')
print(f'pt2 = {pt2}')
print(f'pt3 = {pt3}')
print(f'pt4 = {pt4}')

#results, anticlockise
# pt1 = [ 2 56]
# pt2 = [111  11]
# pt3 = [225 134]
# pt4 = [112 193]