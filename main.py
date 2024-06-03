from tabulate import tabulate
import pandas as pd
import sys

try: import ujson as json
except: import json

with open(sys.argv[1], 'r', encoding='utf-8') as f:
	content = f.readlines()

collect = ""
for line in content:
	if ("Statistic gathering started" in line) or collect:
		collect += line

collect = collect.split("\n")[1:]
headers = collect[0].split("\t")

#print(f"Headers[{len(headers)}]:", json.dumps(headers, indent=2))

data = []
content.pop(1)
for line in content:
	if "\t" not in line: continue
	data.append({})
	row = line.split("\t")
	for idx, header in enumerate(headers):
		value = None
		if idx < len(row):
			value = row[idx].replace("\n", "")
			if value.isdigit(): value = int(value)
		data[-1][header] = value

#print(f"Data[{len(data)}]:", json.dumps(data, indent=2))

df = pd.DataFrame.from_records(data)
print(df)

for  event, group in df.groupby("EVENT"):
    value = group['AVGTSMR']
    print(f"{event} min={value.min()} max={value.max()} 50%={value.median()} 90%={value.quantile(0.9)} 99%={value.quantile(0.99)} 99.9%={value.quantile(0.999)}")

table = []
for i in range(110, 151, 5):
    count = len(df[(df['AVGTSMR']>=i) &(df['AVGTSMR']<(i+5))])
    less = len(df[df['AVGTSMR']<=i])
    
    table.append([i, count, count/len(df)*100, less/len(df)*100])

print(tabulate(table, headers=["ExecTime", "TransNo", "Weight,%", "Percent"], tablefmt='double_outline'))