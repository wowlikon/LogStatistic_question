from tabulate import tabulate
import pandas as pd
import statistics
import sys

#Импорт модуля для читаеого вывода массивов
try: import ujson as json #Более быстрая версия библиотеки
except: import json #Стандартная библиотека для работы с JSON

#Чтение файла по строкам
with open(sys.argv[1], 'r', encoding='utf-8') as f:
	content = f.readlines()

#Сохранение строк только после начала сбора статистики
collect = ""
for line in content:
	if ("Statistic gathering started" in line) or collect:
		collect += line

#Отделение заголовков столбцов
collect = collect.split("\n")[1:]
headers = collect[0].split("\t")
#print(f"Headers[{len(headers)}]:", json.dumps(headers, indent=2))

#Получение данных
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

def count_in_range(data: list, field: str, min_val:int, max_val: int) -> int:
    count = 0
    for elem in data:
        if (elem[field] >= min_val) and (elem[field] < max_val): count += 1
    return count

def count_less(data: list, field: str, value: int) -> int:
    count = 0
    for elem in data:
        if elem[field] <= value: count += 1
    return count

def get_column(data: list, field: str) -> list:
    column = []
    for elem in data:
        column.append(elem[field])
    return column

def filter_field(data: list, field: str, value) -> list:
    result = []
    for elem in data:
        if elem[field] == value:
            result.append(elem)
    return result

#Преодбразование в DataFrame
#df = pd.DataFrame.from_records(data)
#print(df)

#Групировка по EVENT
events = set(get_column(data, "EVENT"))
for event in events:
    group = filter_field(data, "EVENT", event)
    value = get_column(group, "AVGTSMR")
    print(f"{event} min={min(value)} max={max(value)} 50%={statistics.median(value)} 90%={value.quantile(0.9)} 99%={value.quantile(0.99)} 99.9%={value.quantile(0.999)}")

#Создание таблицы
table = []
for i in range(110, 151, 5):
    count = count_in_range(data, 'AVGTSMR', i, i+5)
    less = count_less(data, 'AVGTSMR', i)
    table.append([i, count, count/len(df)*100, less/len(df)*100])

print(tabulate(table, headers=["ExecTime", "TransNo", "Weight,%", "Percent"], tablefmt='double_outline'))

