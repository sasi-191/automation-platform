import json


def load_rules():
    try:
        with open("rules.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_rules(rules):
    with open("rules.json", "w") as file:
        json.dump(rules, file, indent=4)