from collections import Counter

with open("day7.txt", 'r') as f:
    input = f.read()


hands = input.split("\n")

card_dict = {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}

def get_hand_value(hand_str):
    hand = list(hand_str.split(" ")[0])
    counts = sorted(list(dict(Counter(hand)).values()), reverse=True)
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