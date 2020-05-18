import json

with open("./testing/KomkodeAntal_linjer.json", "r") as read_file:
    data = json.load(read_file)
    print(data)
    print(data['0101'])