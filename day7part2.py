from collections import Counter

with open("day7.txt", 'r') as f:
    input = f.read()


hands = input.split("\n")

card_dict = {"T": 10, "J": 1, "Q": 12, "K": 13, "A": 14}

def get_hand_value(hand_str):
    hand = list(hand_str.split(" ")[0])
    counts = dict(Counter(hand))
    if hand == ['J'] * 5:
        pass
    elif 'J' in counts:
        max_key = max(counts, key=counts.get)
        if max_key == 'J':
            max_key = sorted(counts, key=counts.get, reverse=True)[1]
        counts[max_key] = counts[max_key] + counts['J']
        del counts['J']
    counts = sorted(list(counts.values()), reverse=True)
    if counts[0] == 5:
        score = 6
    elif counts[0] == 4:
        score = 5
    elif counts[0] == 3 and counts[1] == 2:
        score = 4
    elif counts[0] == 3 and counts[1] != 2:
        score = 3
    elif counts[0] == 2 and counts[1] == 2:
        score = 2
    elif counts[0] == 2 and counts[1] != 2:
        score = 1
    else:
        score = 0
    result = [score]
    for h in hand:
        if h.isdigit():
            result.append(int(h))
        else:
            result.append(card_dict[h])
    return result

hands.sort(key=get_hand_value)

result = 0

for i, hand in enumerate(hands):
    result += (i + 1) * int(hand.split(" ")[1])

print(result)