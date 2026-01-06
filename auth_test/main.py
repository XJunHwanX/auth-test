from fastapi import FastAPI, HTTPException
# Render 배포 경로를 고려한 절대 경로 임포트
from auth_test import db_mock as db
from auth_test import auth_utils
from auth_test import schemas  # schemas.py를 사용합니다.

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Auth Test Server is Running!"}

# [회원가입] - schemas.UserRegister를 사용하도록 변경
@app.post("/signup")
def signup(user: schemas.UserRegister):
    # 중복 가입 확인
    if db.find_user(user.email):
        raise HTTPException(status_code=400, detail="이미 존재하는 이메일입니다.")
    
    # 비밀번호 암호화 로직 적용
    hashed_password = auth_utils.get_password_hash(user.password)
    
    user_data = user.dict()
    user_data["password"] = hashed_password  # 암호화된 값으로 교체
    
    # 임시 DB에 저장
    db.save_user(user_data)
    return {"message": f"{user.nickname}님, 가입을 축하합니다!"}

# [로그인] - schemas.UserLogin을 사용하도록 변경
@app.post("/login")
def login(user: schemas.UserLogin):
    found = db.find_user(user.email)
    
    # 유저 검증 및 암호화된 비밀번호 비교
    if not found or not auth_utils.verify_password(user.password, found["password"]):
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 틀렸습니다.")
    
    return {
        "message": "로그인 성공!",
        "user_info": {"nickname": found["nickname"], "email": found["email"]}
    }

@app.get("/bookmarks")
def get_bookmarks():
    return {"message": "이 기능은 나중에 Postgres와 연결될 예정입니다.", "data": []}