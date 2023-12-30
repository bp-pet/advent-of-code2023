with open("day6.txt", 'r') as f:
    input = f.read()

times_str, distances_str = input.split("\n")

time = ""
for t in times_str.split(" ")[1:]:
    if len(t) > 0:
        time += t
time = int(time)

record = ""
for d in distances_str.split(" ")[1:]:
    if len(d) > 0:
        record += d
record = int(record)

counter = 0
for hold_time in range(time + 1):
    remaining_time = time - hold_time
    distance = remaining_time * hold_time
    if distance > record:
        counter += 1

print(counter)