import sys
from pprint import pprint
COL=10
ROW=10

if len(sys.argv) == 4:
    input_file = sys.argv[1]
    list_of_errors = sys.argv[2]
    output_file = sys.argv[3]
else:
    input_file = 'GridWorld-5D-new.POMDP'
    list_of_errors = 'errors.out'
    output_file = 'GridWorld-5D-nothing.POMDP'
    

lines = open(list_of_errors).readlines()

prefix = 'a'
states =  ' '.join([' '.join([' '.join([prefix+str((i*COL+j)*100 + rot) for rot in range(8)]) for j in range(COL)]) for i in  range(ROW)])
states = states.split(' ')

actions = {
        '0': 'straight',
        '1': 'left',
        '2': 'right',
        '3': 'halt'
}

problematic_observations = []
for line in lines:
    try:

        action,rest = line.split(',')
    except:
        print(line)
    rest = rest.strip()
    num = int(rest.split('=')[1])
    state = states[num]
    position = int(state[len(prefix):])//100
    rot = num % 8
    row = position // 10
    col = position % 10

    print(f'{actions[action]} to {state} {num}  ({row}, {col}) w/ rot {rot} ')
    # print(f'{action} ({row}, {col}){rot} ')
    problematic_observations.append([actions[action], state])

template = 'O: {a} : {sj} : {oj}         {p}\n'
# print(problematic_observations[:10])

lines = []
for a,s in problematic_observations:
   lines.append(template.format(
       a=a,prefix=prefix,sj=s,oj='null',p=1.0
       ))
# pprint(lines[:10])

actual_file_lines = open(input_file).readlines()
actual_file_lines.extend(lines)
new_file = open(output_file, 'w')
new_file.writelines(actual_file_lines)
new_file.close()
