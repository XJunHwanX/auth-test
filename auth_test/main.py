from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import db_mock as db
import auth_utils

app = FastAPI()

# 데이터 규격 정의
class UserRegister(BaseModel):
    email: str
    password: str
    nickname: str

class UserLogin(BaseModel):
    email: str
    password: str

@app.get("/")
def home():
    return {"message": "Auth Test Server is Running!"}

# [회원가입]
@app.post("/signup")
def signup(user: UserRegister):
    # 중복 가입 확인
    if db.find_user(user.email):
        raise HTTPException(status_code=400, detail="이미 존재하는 이메일입니다.")
    
    # 임시 DB에 저장
    db.save_user(user.dict())
    return {"message": f"{user.nickname}님, 가입을 축하합니다!"}

# [로그인]
@app.post("/login")
def login(user: UserLogin):
    found = db.find_user(user.email)
    if not found or found["password"] != user.password:
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 틀렸습니다.")
    
    return {
        "message": "로그인 성공!",
        "user_info": {"nickname": found["nickname"], "email": found["email"]}
    }

# [즐겨찾기 테스트용]
@app.get("/bookmarks")
def get_bookmarks():
    # 나중에 실제 DB 연결 시 이 부분을 유저 아이디별로 필터링하도록 수정
    return {"message": "이 기능은 나중에 Postgres와 연결될 예정입니다.", "data": []}