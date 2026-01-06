# 실제 DB 대신 사용할 리스트
# 임시 데이터 저장소
users_db = [] 

def save_user(user_data):
    users_db.append(user_data)
    return True

def find_user(email):
    return next((user for user in users_db if user["email"] == email), None)