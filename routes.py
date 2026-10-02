from fastapi import APIRouter, HTTPException, Depends
from models import Rule, RuleUpdate, UserCreate
from sqlalchemy.orm import Session
from database import get_db
from db_models import RuleTable, UserTable
from security import hash_password, create_access_token, verify_password, SECRET_KEY
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    db_user = db.query(UserTable).filter(UserTable.username == username).first()
    return db_user


@router.get("/")
def home():
    return {"message": "Automation API is running"}


@router.post("/rules")
def create_rule(rule: Rule, db: Session = Depends(get_db), current_user: UserTable = Depends(get_current_user)):
    new_rule = RuleTable(**rule.model_dump())
    db.add(new_rule)
    db.commit()
    db.refresh(new_rule)
    return new_rule


@router.get("/rules/{rule_id}")
def get_rule(rule_id: int, db: Session = Depends(get_db), current_user: UserTable = Depends(get_current_user)):
    rule = db.query(RuleTable).filter(RuleTable.id == rule_id).first()
    if rule is None:
        raise HTTPException(status_code=404, detail="Rule not found")
    return rule


@router.get("/rules")
def get_rules(db: Session = Depends(get_db), current_user: UserTable = Depends(get_current_user)):
    return db.query(RuleTable).all()


@router.put("/rules/{rule_id}")
def update_rule(rule_id: int, rule_update: RuleUpdate, db: Session = Depends(get_db), current_user: UserTable = Depends(get_current_user)):
    rule = db.query(RuleTable).filter(RuleTable.id == rule_id).first()
    if rule is None:
        raise HTTPException(status_code=404, detail="Rule not found")
    update_data = rule_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(rule, key, value)
    db.commit()
    db.refresh(rule)
    return rule


@router.delete("/rules/{rule_id}")
def delete_rule(rule_id: int, db: Session = Depends(get_db), current_user: UserTable = Depends(get_current_user)):
    rule = db.query(RuleTable).filter(RuleTable.id == rule_id).first()
    if rule is None:
        raise HTTPException(status_code=404, detail="Rule not found")
    db.delete(rule)
    db.commit()
    return {"message": "Rule deleted"}


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    hashed = hash_password(user.password)
    new_user = UserTable(username=user.username, hashed_password=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully", "username": new_user.username}


@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserTable).filter(UserTable.username == user.username).first()
    if db_user is None or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_access_token({"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer"}