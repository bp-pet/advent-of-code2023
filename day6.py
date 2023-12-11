with open("day6.txt", 'r') as f:
    input = f.read()


times_str, distances_str = input.split("\n")

times = []
for t in times_str.split(" ")[1:]:
    if len(t) > 0:
        times.append(int(t))

distances = []
for d in distances_str.split(" ")[1:]:
    if len(d) > 0:
        distances.append(int(d))

result = 1

for time, record in zip(times, distances):
    counter = 0
    for hold_time in range(time + 1):
        remaining_time = time - hold_time
        distance = remaining_time * hold_time
        if distance > record:
            counter += 1
    if counter > 0:
        result = result * counter

print(result)