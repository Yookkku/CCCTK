import csv


def mem_csv(thinglist):
    with open('localdata.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['class_', 'thingid', 'thingname', 'predate', 'ddl'])
        writer.writeheader()
        writer.writerows(thinglist)


def read_csv():
    with open('localdata.csv', 'r') as f:
        reader = csv.DictReader(f)
        ret = []
        for row in reader:
            # print(row)
            dic = {'class_': row['class_'], 'thingid': row['thingid'], 'thingname': row['thingname'],
                   'predate': row['predate'], 'ddl': row['ddl']}
            ret.append(dic)
        return ret


if __name__ == '__main__':
    a = [
            {
                "class_": "药品",
                "ddl": "678954",
                "predate": "10978934",
                "thingid": 1,
                "thingname": "999感冒灵"
            },
            {
                "class_": "食品",
                "ddl": "166970432",
                "predate": "16697342",
                "thingid": 3,
                "thingname": "果冻"
            }
        ]

    # mem_csv(a)
    print(read_csv())
