

"""
sec_per_day = 86400
sec_per_hour = 3600
sec_per_min = 60

sec_input = 90060

day = int(sec_input/sec_per_day)
hour = int((sec_input - day*sec_per_day)/sec_per_hour)
min = int((sec_input - day * sec_per_day - hour * sec_per_hour)/sec_per_min)
sec = int(sec_input - day*sec_per_day - hour*sec_per_hour - min* sec_per_min)

output = f'{day} day {hour} hour {min} min {sec} sec'

print (output)
"""

panel_stack = []

panel_stack.append('line1')
panel_stack.append('line2')
panel_stack.append('line3')
panel_stack.append('line4')
panel_stack.append('line5')

print (len(panel_stack))
print (panel_stack.pop())
print (panel_stack[len(panel_stack) - 1])