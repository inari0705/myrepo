import mini_func as mf

print('----- 가위바위보 게임 -----')

if mf.db_connect() is False:
    exit(1)

while True:
    try:
        print("""1. Add user \n2. User ID & Score list\n3. User password change
4. Delete user\n5. Game start\n6. Program exit""")
        action = int(input('실행할 메뉴 번호를 입력하세요: '))
        if 1 <= action <= 7:

            # 1. 유저 추가
            if action == 1:
                mf.create_user()

            # 2. 유저 목록, 점수 조회
            elif action == 2:
                print('---User 목록 및 점수 조회---')
                comp = mf.show_users(2)
                if comp is True:
                    print("User 목록 및 점수가 출력되었습니다.")
                else:
                    print("User 목록 및 점수 불러오기에 실패했습니다.")
                    continue

            # 3. 유저 비밀번호 변경
            elif action == 3:
                print('---유저 비밀번호 수정 화면---')
                # show_users() 호출
                mf.show_users(1)
                print("<본인 ID와 PW를 입력하세요>")
                # 수정할 유저 ID와 새로운 비밀번호를 mf.get_user()를 통해서 받는다

                inquiry_user = mf.get_user()
                valid_update = mf.edit_user(inquiry_user)
                if valid_update is True:
                    print("수정이 완료되었습니다")
                else:
                    print("ID나 PW를 잘못입력했습니다.")
                    continue

            # 4. user 정보 삭제
            elif action == 4:
                mf.delete_user()

            # 5. 게임 시작
            elif action == 5:
                # 유저 정보 먼저 받기
                user_info = mf.get_user()
                if user_info is None:
                    print("해당 user 정보가 없습니다. 다시 실행하세요.")
                    continue

                game_type = int(input("어떤 게임을 하시겠습니까?(1. 가위바위보, 2. 숫자맞추기): "))

                if game_type == 1:
                    print('가위바위보 게임 실행 화면')
                    score = mf.play_game()

                elif game_type == 2:
                    print('숫자맞추기 게임 실행 화면')
                    score = mf.play_game2()
                else:
                    print('1번과 2번중에 입력하세요')
                    continue

                if mf.get_score(user_info, score) is True:
                    print("점수 저장이 완료되었습니다.")
                else:
                    print("다시 실행하세요.")

            # 6. 프로그램 종료
            elif action == 6:
                print('프로그램 종료')
                mf.db_close()
                break
        else:
            print('1 ~ 6 사이의 번호를 입력해주세요')
    except KeyboardInterrupt:  # cmd 창에서 ctrl + C를 입력한 경우
        print("Program 을 종료합니다")
        mf.db_close()
        break
