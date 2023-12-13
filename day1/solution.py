import re
file1 = open('lines.txt', 'r')
lines = file1.readlines()

line = lines[0]
line_proto = [lines[0], lines[1], lines[2]]

inc = 0

for l in lines:
    new_arr = re.findall(r'(\d+)', l)
    print('new_arr:', new_arr)
    inc += int(new_arr[0][0] + new_arr[-1][-1])

print('inc', inc)
