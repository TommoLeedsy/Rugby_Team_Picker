def main(players):
    import names
    import random
    import csv

    with open('players.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        positions = [[[1, 3], [2], [4, 5], [6, 7], [8]], [[9], [10], [11, 14], [12], [13], [15]]]
        for _ in range(players):
            data = []
            data.append(names.get_full_name(gender='male'))
            group = random.randrange(0, 2)
            picks = random.sample(range(len(positions[group])), k=2)
            for i in range(len(picks)):
                for position in positions[group][picks[i]]:
                    data.append(position)
                    data.append((random.randrange(5, 11)))
            writer.writerow(data)
        csv_file.close()


if __name__ == '__main__':
    main(100)
