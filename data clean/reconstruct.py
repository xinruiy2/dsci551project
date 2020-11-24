import pandas as pd

df = pd.read_csv("weather_description.csv")
df["hour"] = ""
df["date"] = ""

for index, row in df.iterrows():
    datetime = row["datetime"]
    datetime = datetime.split(' ')
    if datetime[1][1] == ":":
        row["hour"] = "0" + datetime[1][0]
    else:
        row["hour"] = datetime[1][:2]
    date = datetime[0]
    date = date.split('/')
    if len(date[0]) < 2:
        date[0] = "0" + date[0]
    if len(date[1]) < 2:
        date[1] = "0" + date[1]
    row["date"] = date[2] + "-" + date[0] + "-" + date[1]

del df['datetime']

df.to_csv("sample.csv", index=False)
