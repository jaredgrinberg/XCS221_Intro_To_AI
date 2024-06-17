cards = (5,4,5,7,2)
for i in range(len(cards)):
    cards_list = list(cards)
    cards_list[i] -= 1
    cards = tuple(cards_list)
    print(cards)