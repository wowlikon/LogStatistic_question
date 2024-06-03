import datetime, random, sys

def f():
    v = 100
    i = True
    while i:
        i = (random.randint(0, 100) > 10)
        v += random.randint(1, 5)
    return v

val = [
    (1, lambda: random.randint(200, 600)),
    (1, lambda: random.randint(5, 100)),
    (10, lambda: random.randint(0, 10)),
    (1, f),
    (2, lambda: random.randint(0, 10)),
]

events = [
    "ORDER",
    "QUEUE",
    "OTHER"
]

with open(sys.argv[1], "w+", encoding="utf-8") as f:
    f.write(f"[{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S.%f')}] Statistic gathering started\n")
    f.write("TIME	EVENT	CALLCNT	FILLCNT	AVGSIZE	MAXSIZE	AVGFULL	MAXFULL	AVGDLL	MAXDLL	AVGTRIP	MAXTRIP	AVGTEAP	MAXTEAP	AVGTSMR	MAXTSMR	MINTSMR\n")
    for i in range(random.randint(20, 1000)):
        f.write(f"[{datetime.datetime.now().strftime('%H:%M:%S.%f')}]\t")
        f.write(random.choice(events)+"\t")
        v = []
        for c, l in val:
            for _ in range(c):
                v.append(l())
        f.write("\t".join(map(str, v)))
        f.write("\n")
