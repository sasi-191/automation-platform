from fastapi import APIRouter, HTTPException, Depends
from models import Rule, RuleUpdate
from storage import load_rules, save_rules
from sqlalchemy.orm import Session
from database import get_db
from db_models import RuleTable

router = APIRouter()
rules = load_rules()

highest_id = 0

for rule in rules:
    if rule["id"] > highest_id:
        highest_id = rule["id"]
next_id = highest_id + 1


@router.get("/")
def home():
    return {"message": "Automation API is running"}

@router.post("/rules")
def create_rule(rule : Rule):
    global next_id
    rule_data = rule.model_dump()
    rule_data["id"] = next_id
    next_id = next_id + 1
    rules.append(rule_data)
    save_rules(rules)
    return rule_data

@router.get("/rules/{rule_id}")
def get_rule(rule_id : int):
    for rule in rules:
        if rule["id"] == rule_id:
            return rule
    raise HTTPException(status_code=404, detail="Rule not found")

@router.get("/rules")
def get_rules():
    return rules

@router.put("/rules/{rule_id}")
def update_rule(rule_id : int, rule_update: RuleUpdate):
    for rule in rules:
        if rule["id"] == rule_id:
            update_data  = rule_update.model_dump(exclude_unset= True)
            for key, value in update_data.items():
                rule[key] = value
            save_rules(rules)
            return rule

@router.delete("/rules/{rule_id}")
def delete_rule(rule_id : int):
    for rule in rules:
        if rule["id"] == rule_id:
            rules.remove(rule)
            save_rules(rules)
            return {"message": "Rule deleted"}