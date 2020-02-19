import os
import json
import sqlite3

def loadData(filePath):
    with open(filePath, 'r') as file:
        return file.read()

def loadJSON(jsonData):
    return json.loads(jsonData)


def main():
    d = loadData('test.json')

    j = loadJSON(d)

    user = j["user"]
    text = j["text"]

    print(user)
    print(text)

main()
