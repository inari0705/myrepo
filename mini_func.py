import pymysql
import random

# 전역 변수 설정
conn = 0
curs = 0


# DB 연결 함수
def db_connect():
    global conn, curs  # 전역변수 지정

    try:
        conn = pymysql.connect(host='비밀', user='SBA_02', password='123qwe',
                               db='SBA_02', charset='utf8')
    except:
        print("DB 연결을 실패했습니다.")
        return False

    curs = conn.cursor(pymysql.cursors.DictCursor)
    return True


# DB 종료 함수
def db_close():
    curs.close()
    conn.close()


# ID, password가 일치 확인하는 함수
def check_user(user_id, user_pw):
    sql = f'select pw from user_t where id = "{user_id}"'
    curs.execute(sql)
    row = curs.fetchone()
    if row is None:
        return False
    if row['pw'] == user_pw:
        return True
    else:
        return False


# 유저 id, pw 입력 받아 유효성 확인 후, 유저 정보 반환
def get_user():
    # ID 입력
    user_id = input("ID : ")
    user_pw = input("PASSWORD : ")
    # ID 유효성 확인
    if check_user(user_id, user_pw) is False:
        return None
    # 학생정보 user 딕셔너리 정리
    user = {'id': user_id, 'pw': user_pw}
    return user


# 1. 유저 생성 함수
def create_user():
    while (True):
        print("id는 10자리 이상이 될 수 없습니다.")
        user_id = input('등록하실 id> ')
        if len(user_id) >= 10:
            print("자릿수를 초과하였습니다. 다시 입력해주세요!")
            continue
        print("password는 20자리 이상이 될 수 없습니다.")
        user_pw = input('등록하실 password> ')
        if len(user_pw) >= 20:
            print("자릿수를 초과하였습니다. 다시 입력해주세요!")
            continue
        sql = f'select id from user_t where id = "{user_id}"'
        curs.execute(sql)
        row = curs.fetchone()
        if row == None:
            sql = f'insert into user_t (id, pw) values ("{user_id}", "{user_pw}")'
            curs.execute(sql)
            conn.commit()
            sql = f'insert into score_t (id, score) values ("{user_id}", 0)'
            curs.execute(sql)
            conn.commit()
            print("등록 되었습니다.")
            return True
        else:
            print("id가 중복됩니다. 다시 입력해주세요!")


# 2. 유저 ID및 점수 조회 함수
def show_users(num):
    if num == 1:  # USER ID만 조회하는 경우
        sql = f'select id from user_t'
        curs.execute(sql)
        rows = curs.fetchall()
        for row in rows:
            print(f"USER ID: {row['id']:^10}")
    else:  # ID와 점수 모두 출력인 경우
        type2 = input("출력할 type 문자를 입력하세요(a.전체 USER ID와 점수, b.특정 USER ID와 점수): ")
        if type2 == 'a':  # 전체 조회인 경우
            print("점수는 가위바위보와 숫자맞추기 합산입니다")
            sql = f'select id, score from score_t order by score desc'
            curs.execute(sql)
            rows = curs.fetchall()
            for row in rows:
                print(f"USER ID: {row['id']:^10}, USER SCORE: {row['score']:^10}")
            return True
        elif type2 == 'b':  # 특정 유저 조회인 경우
            show_indiv = input("조회할 ID를 입력하세요: ")
            sql = f'select id, score from score_t'
            curs.execute(sql)
            rows = curs.fetchall()
            for row in rows:
                if row['id'] == show_indiv:
                    print(f"User ID: {show_indiv:^10}, USER SCORE: {row['score']:^10}")
                    return True  # 특정 유저 조회 성공
            print("조회할 ID가 존재하지 않습니다")
            return False  # 조회할 ID가 없는 경우
        else:
            print("a와 b 중 하나를 입력하세요")
            return False


# 3. 유저 비밀번호 변경 함수
def edit_user(inquiry_user):
    if inquiry_user is None:
        return False
    new_pw = input("새로 지정할 비밀번호를 입력하세요: ")
    temp_id = inquiry_user['id']
    # 가져온 id,pw를 update 문으로 pw 변경
    sql = f'update user_t set pw = "{new_pw}" where id = "{temp_id}"'
    curs.execute(sql)
    conn.commit()

    return True


# 4. 유저 삭제 함수
def delete_user():
    while True:
        print("주의! 점수도 같이 삭제됩니다!")
        user_id = input("삭제하실 id> ")
        user_pw = input("password> ")
        sql = f'select * from user_t where id = "{user_id}" and pw = "{user_pw}"'
        curs.execute(sql)
        row = curs.fetchone()
        if row is None:
            print("id 또는 password가 잘 못 되었습니다.")
            continue
        else:
            sql = f'delete from score_t where id = "{user_id}"'
            curs.execute(sql)
            conn.commit()
            sql = f'delete from user_t where id = "{user_id}"'
            curs.execute(sql)
            conn.commit()
            print("삭제 되었습니다.")
            return True


# 5. 게임 실행
def play_game():
    score = 0
    result = ["가위", "바위", "보"]
    user = input("가위, 바위, 보 중 하나를 선택하세요: ")
    if user == '가위':
        if random.choice(result) == '가위':
            print("무승부")
            print('점수=', score)
        elif random.choice(result) == '바위':
            print("패배!")
            print('점수=', score)
        else:
            score = score + 1
            print("승리!")
            print('점수=', score)
    elif user == '바위':
        if random.choice(result) == '가위':
            print("무승부")
            print('점수=', score)
        elif random.choice(result) == '보':
            print("패배!")
            print('점수=', score)
        else:
            score = score + 1
            print("승리!")
            print('점수=', score)
    elif user == '보':
        if random.choice(result) == '보':
            print("무승부")
            print('점수=', score)
        elif random.choice(result) == '가위':
            print("패배!")
            print('점수=', score)
        else:
            score = score + 1
            print("승리!")
            print('점수=', score)
    else:
        print("선택이 잘못되었습니다.")
    return score

def play_game2():
    score = 0
    number = random.randint(1, 20)
    print('1부터 20까지의 숫자가 있습니다.')
    print('지금부터 5번의 기회를 드립니다 맞추면 +1 점수입니다.')

    # 5번의 추측기회.
    for i in range(1, 6):
        print('예상하는 숫자를 입력하세요.')
        guess = int(input())

        if guess <number :
            print('예상한 숫자가 너무 작습니다.')
        elif guess > number:
            print('예상한 숫자가 너무 큽니다.')
        else:
            break
    if guess == number:
        print(f'예상한 숫자 {guess}는 정답입니다.')
        score += 1
        print(f'축하합니다 1점을 획득했습니다.')
        return score
    else:
        print(f'아쉽습니다. 정답은  {number} 입니다.')
        return score



# 5'. 유저 정보와 점수를 받아 DB에 저장
def get_score(user_info, score):
    # 기존 점수 받아오기
    sql = f'''select score from score_t where id = "{user_info['id']}"'''
    curs.execute(sql)
    row = curs.fetchone()
    if row is None:
        sql = f'''update score_t set score = {score}
                where id = "{user_info['id']}"'''
    else:
        temp = int(row['score'])
        sql = f'''update score_t set score = {score + temp} where id = "{user_info['id']}"'''
    if curs.execute(sql) == 0:
        return False
    conn.commit()
    return True
