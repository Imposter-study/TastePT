# 맛P.T
🇰🇷 한국어 | [🇺🇸 English](./README-en.md)
## 소개
### 팀
사기꾼 연구회

### 프로젝트
게으른 완벽주의자를 위한 레시피 챗봇
👉 [맛P.T SA 문서](https://www.notion.so/SA-1a97d4611a6f805d8bdbe9ae94405f62?pvs=4)
👉 [맛P.T 웹사이트](https://dev.tastept.store/)

## ✨ 주요 기능
### 👤 회원기능

<details>
  <summary>회원가입, 로그인, 로그아웃, 회원탈퇴</summary>
  
  - **회원가입**
    - **Endpoint**: `POST /api/v1/accounts/`
    - **Request Body**:
      ```json
      {
        "email": "string",
        "password": "string",
        "password_confirm": "string",
        "nickname": "string",
        "role": "string",
        "age": "integer",
        "gender": "string",
        "allergies": ["string"],
        "preferred_cuisine": ["string"],
        "diet": "string"
      }
      ```
    - **Validation**:
      - 비밀번호: 최소 8자 이상
      - 이메일: 유효성 검사
      - 닉네임: 최대 30글자
      - 비밀번호 일치 확인
    - **이메일 인증**:
      - 회원가입 시 자동으로 이메일 인증 메일 발송
      - 인증 링크 클릭 시 계정 활성화
      - 인증 URL: `GET /api/v1/accounts/verify-email/<token>/`
      - **응답**:
        - 201: 회원가입 성공 (이메일 인증 대기)
        - 400: 유효성 검사 실패

  - **로그인**
    - **Endpoint**: `POST /api/v1/accounts/signin/`
    - **Request Body**:
      ```json
      {
        "username": "string",
        "password": "string"
      }
      ```
    - **Response**:
      ```json
      {
        "detail": "로그인 성공",
        "nickname": "string"
      }
      ```
    - **Status Codes**:
      - 200: 로그인 성공
      - 401: 인증 실패

  - **로그아웃**
    - **Endpoint**: `POST /api/v1/accounts/signout/`
    - **Response**:
      ```json
      {
        "detail": "로그아웃 성공"
      }
      ```
    - **Status Codes**:
      - 200: 로그아웃 성공

  - **회원탈퇴**
    - **Endpoint**: `DELETE /api/v1/accounts/`
    - **Request Body**:
      ```json
      {
        "password": "string"
      }
      ```
    - **Response**:
      ```json
      {
        "message": "회원이 비활성화 되었습니다."
      }
      ```
    - **Status Codes**:
      - 200: 탈퇴 성공
      - 400: 비밀번호 불일치
</details>

<details>
  <summary>프로필 조회, 프로필 수정</summary>
  
  - **프로필 조회**
    - **Endpoint**: `GET /api/v1/accounts/<nickname>/`
    - **Response**:
      ```json
      {
        "email": "string",
        "nickname": "string",
        "profile_picture": "string",
        "role": "string",
        "age": "integer",
        "gender": "string",
        "allergies": ["string"],
        "preferred_cuisine": ["string"],
        "diet": "string"
      }
      ```
    - **Status Codes**:
      - 200: 조회 성공
      - 404: 사용자 없음

  - **프로필 수정**
    - **Endpoint**: `PUT /api/v1/accounts/`
    - **Request Body**:
      ```json
      {
        "nickname": "string",
        "profile_picture": "file",
        "age": "integer",
        "gender": "string",
        "allergies": ["string"],
        "preferred_cuisine": ["string"],
        "diet": "string"
      }
      ```
    - **Response**:
      ```json
      {
        "detail": "프로필이 성공적으로 업데이트되었습니다."
      }
      ```
    - **Status Codes**:
      - 200: 수정 성공
      - 400: 유효성 검사 실패
</details>

<details>
  <summary>랜덤 닉네임 생성</summary>
  
  - **Endpoint**: `GET /api/v1/accounts/random_nickname/`
  - **응답**:
    ```json
    {
      "nickname": "random_nickname"
    }
    ```
  - **기능 설명**:
    - 형용사와 명사 조합으로 유니크한 닉네임 생성
    - 자동으로 생성된 닉네임은 즉시 사용 가능
    - 중복 체크 자동 수행
  - **Status Codes**:
    - 200: 랜덤 닉네임 생성 성공
    - 500: 닉네임 생성 실패
</details>

<details>
  <summary>패스워드 변경</summary>
  
  - **Endpoint**: `PUT /api/v1/accounts/password/`
  - **Request Body**:
    ```json
    {
      "current_password": "string",
      "new_password": "string",
      "new_password_confirm": "string"
    }
    ```
  - **Validation**:
    - 현재 비밀번호 확인
    - 새로운 비밀번호:
      - 최소 8자 이상
      - 대소문자, 숫자, 특수문자 포함
    - 비밀번호 일치 확인
  - **Response**:
    ```json
    {
      "detail": "비밀번호가 성공적으로 변경되었습니다."
    }
    ```
  - **Status Codes**:
    - 200: 변경 성공
    - 400: 유효성 검사 실패
</details>

<details>
  <summary>소셜로그인</summary>
  
  - **카카오 로그인**
    - **인증 URL**: `GET /api/v1/accounts/social/signin/kakao/`
    - **Callback**: `GET /api/v1/accounts/social/callback/kakao`
    - **Redirect**: 프론트엔드 도메인

  - **소셜로그인 공통**
    - **인증 흐름**:
      1. 소셜 로그인 URL 요청
      2. 소셜 플랫폼 인증
      3. 콜백 URL로 리다이렉트
      4. 사용자 생성/로그인
    - **인증 상태 확인**:
      ```json
      {
        "authenticated": boolean,
        "user": "nickname",
        "profile_img": boolean
      }
      ```
</details>

### 🤖 챗봇
<details>
  <summary>채팅방 관리</summary>
  
  - **채팅방 생성**
    - **Endpoint**: `POST /api/chatbot/room/`
    - **Body**:
      ```json
      {
        "name": "string"
      }
      ```
    - **Response**:
      ```json
      {
        "id": 1,
        "name": "string",
        "created_at": "2025-04-11T04:17:10+00:00"
      }
      ```
    - **Status Codes**:
      - 201: 채팅방이 성공적으로 생성됨
      - 400: 필요한 파라미터가 누락됨
      - 401: 인증되지 않은 사용자

  - **채팅방 이름 변경**
    - **Endpoint**: `PUT /api/chatbot/room/{room_id}/`
    - **Body**:
      ```json
      {
        "name": "string"
      }
      ```
    - **Response**:
      ```json
      {
        "id": 1,
        "name": "string",
        "created_at": "2025-04-11T04:17:10+00:00"
      }
      ```
    - **Status Codes**:
      - 200: 채팅방 이름이 성공적으로 변경됨
      - 400: 필요한 파라미터가 누락됨
      - 401: 인증되지 않은 사용자
      - 403: 권한이 없는 사용자
      - 404: 채팅방을 찾을 수 없음

  - **채팅방 삭제**
    - **Endpoint**: `DELETE /api/chatbot/room/{room_id}/`
    - **Response**:
      ```json
      {
        "success": true
      }
      ```
    - **Status Codes**:
      - 200: 채팅방이 성공적으로 삭제됨
      - 401: 인증되지 않은 사용자
      - 403: 권한이 없는 사용자
      - 404: 채팅방을 찾을 수 없음
</details>

<details>
  <summary>레시피 챗봇</summary>
  
  - **레시피 질문**
    - **Endpoint**: `POST /api/chatbot/room/{room_id}/message/`
    - **Body**:
      ```json
      {
        "question": "string",
        "user_data": {
          "allergy": ["string"],
          "preferences": ["string"]
        }
      }
      ```
    - **Response**:
      ```json
      {
        "answer": "string"
      }
      ```
    - **Status Codes**:
      - 200: 레시피 추천이 성공적으로 완료됨
      - 400: 필요한 파라미터가 누락됨
      - 401: 인증되지 않은 사용자
      - 404: 채팅방을 찾을 수 없음
      - 500: 레시피 추천 중 오류 발생
</details>

### 📝 커뮤니티
<details>
  <summary>게시글 관리</summary>
  
  - **게시글 목록 조회**
    - **Endpoint**: `GET /api/community/`
    - **Response**:
      ```json
      {
        "count": 1,
        "next": null,
        "previous": null,
        "results": [
          {
            "id": 1,
            "title": "string",
            "content": "string",
            "thumbnail": "string",
            "created_at": "2025-04-11T04:17:10+00:00",
            "updated_at": "2025-04-11T04:17:10+00:00",
            "author": {
              "id": 1,
              "nickname": "string"
            },
            "comments": [
              {
                "id": 1,
                "content": "string",
                "created_at": "2025-04-11T04:17:10+00:00",
                "updated_at": "2025-04-11T04:17:10+00:00",
                "author": {
                  "id": 1,
                  "nickname": "string"
                },
                "reply_comments": []
              }
            ]
          }
        ]
      }
      ```
    - **Status Codes**:
      - 200: 게시글 목록 조회 성공
      - 400: 잘못된 요청 파라미터

  - **게시글 생성**
    - **Endpoint**: `POST /api/community/`
    - **Body**:
      ```json
      {
        "title": "string",
        "content": "string",
        "thumbnail": "string"  // optional
      }
      ```
    - **Status Codes**:
      - 201: 게시글이 성공적으로 생성됨
      - 400: 필요한 파라미터가 누락됨
      - 401: 인증되지 않은 사용자

  - **게시글 수정**
    - **Endpoint**: `PUT /api/community/{post_id}/`
    - **Body**:
      ```json
      {
        "title": "string",
        "content": "string",
        "thumbnail": "string"  // optional
      }
      ```
    - **Status Codes**:
      - 200: 게시글이 성공적으로 수정됨
      - 400: 필요한 파라미터가 누락됨
      - 401: 인증되지 않은 사용자
      - 403: 권한이 없는 사용자
      - 404: 게시글을 찾을 수 없음

  - **게시글 삭제**
    - **Endpoint**: `DELETE /api/community/{post_id}/`
    - **Status Codes**:
      - 204: 게시글이 성공적으로 삭제됨
      - 401: 인증되지 않은 사용자
      - 403: 권한이 없는 사용자
      - 404: 게시글을 찾을 수 없음
</details>

<details>
  <summary>댓글 관리</summary>
  
  - **댓글 작성**
    - **Endpoint**: `POST /api/community/{post_id}/comment/`
    - **Body**:
      ```json
      {
        "content": "string"
      }
      ```
    - **Status Codes**:
      - 201: 댓글이 성공적으로 생성됨
      - 400: 필요한 파라미터가 누락됨
      - 401: 인증되지 않은 사용자
      - 404: 게시글을 찾을 수 없음

  - **댓글 수정**
    - **Endpoint**: `PUT /api/community/comment/{comment_id}/`
    - **Body**:
      ```json
      {
        "content": "string"
      }
      ```
    - **Status Codes**:
      - 200: 댓글이 성공적으로 수정됨
      - 400: 필요한 파라미터가 누락됨
      - 401: 인증되지 않은 사용자
      - 403: 권한이 없는 사용자
      - 404: 댓글을 찾을 수 없음

  - **댓글 삭제**
    - **Endpoint**: `DELETE /api/community/comment/{comment_id}/`
    - **Status Codes**:
      - 204: 댓글이 성공적으로 삭제됨
      - 401: 인증되지 않은 사용자
      - 403: 권한이 없는 사용자
      - 404: 댓글을 찾을 수 없음
</details>

<details>
  <summary>대댓글 관리</summary>
  
  - **대댓글 작성**
    - **Endpoint**: `POST /api/community/{post_id}/comment/{comment_id}/reply/`
    - **Body**:
      ```json
      {
        "content": "string"
      }
      ```
    - **Status Codes**:
      - 201: 대댓글이 성공적으로 생성됨
      - 400: 필요한 파라미터가 누락됨
      - 401: 인증되지 않은 사용자
      - 404: 게시글 또는 댓글을 찾을 수 없음

  - **대댓글 수정**
    - **Endpoint**: `PUT /api/community/comment/{reply_id}/`
    - **Body**:
      ```json
      {
        "content": "string"
      }
      ```
    - **Status Codes**:
      - 200: 대댓글이 성공적으로 수정됨
      - 400: 필요한 파라미터가 누락됨
      - 401: 인증되지 않은 사용자
      - 403: 권한이 없는 사용자
      - 404: 대댓글을 찾을 수 없음

  - **대댓글 삭제**
    - **Endpoint**: `DELETE /api/community/comment/{reply_id}/`
    - **Status Codes**:
      - 204: 대댓글이 성공적으로 삭제됨
      - 401: 인증되지 않은 사용자
      - 403: 권한이 없는 사용자
      - 404: 대댓글을 찾을 수 없음
</details>

<details>
  <summary>신고 기능</summary>
  
  - **게시글 신고**
    - **Endpoint**: `POST /api/community/{post_id}/report/`
    - **Body**:
      ```json
      {
        "type": "post"
      }
      ```
    - **Status Codes**:
      - 201: 게시글이 성공적으로 신고됨
      - 400: 필요한 파라미터가 누락됨
      - 401: 인증되지 않은 사용자
      - 403: 이미 신고한 게시글
      - 404: 게시글을 찾을 수 없음

  - **댓글 신고**
    - **Endpoint**: `POST /api/community/comment/{comment_id}/report/`
    - **Body**:
      ```json
      {
        "type": "comment"
      }
      ```
    - **Status Codes**:
      - 201: 댓글이 성공적으로 신고됨
      - 400: 필요한 파라미터가 누락됨
      - 401: 인증되지 않은 사용자
      - 403: 이미 신고한 댓글
      - 404: 댓글을 찾을 수 없음
</details>

## 🚀 설치 및 실행 방법
```sh
# 프로젝트 클론
git clone https://github.com/Imposter-study/TastePT

# 의존성 설치
pip install -r requirements.txt

# 데이터베이스 마이그레이션
python manage.py migrate

# 개발 서버 실행
python manage.py runserver
```

## 🔧 환경 변수 설정
`.env` 파일을 생성하고 다음과 같이 설정하세요.

```
# Django
SECRET_KEY=
DEBUG=True

# Allowed Hosts
ALLOWED_HOSTS=localhost,127.0.0.1

# OpenAI
OPENAI_API_KEY=

# Database
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=

# Langfuse
LANGFUSE_SECRET_KEY=
LANGFUSE_PUBLIC_KEY=

#Redis
REDIS_HOST=
REDIS_PASSWORD=

# social
KAKAO_CLIENT_ID=
REDIRECT_DOMAIN=

# email
DOMAIN=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

#FRONT
FRONT_DOMAIN=
```

## 🛠 기술 스택
<p align="center">
  <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django"/>
  <img src="https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"/>
  <img src="https://img.shields.io/badge/nginx-009639?style=for-the-badge&logo=nginx&logoColor=white" alt="Nginx"/>
  <img src="https://img.shields.io/badge/Amazon_AWS-FF9900?style=for-the-badge&logo=Amazon-AWS&logoColor=white" alt="Amazon AWS"/>
</p>
<p align="center">
  <img src="https://img.shields.io/badge/git-F05032?style=for-the-badge&logo=git&logoColor=white" alt="Git"/>
  <img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"/>
  <img src="https://img.shields.io/badge/Daphne-003366?style=for-the-badge&logoColor=white" alt="Daphne"/>
  <img src="https://img.shields.io/badge/Gunicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white" alt="Gunicorn"/>
  <img src="https://img.shields.io/badge/Celery-378a3e?style=for-the-badge&logo=celery&logoColor=white" alt="Celery"/>
  <img src="https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white" alt="Redis"/>
</p>
<p align="center">
  <img src="https://img.shields.io/badge/langchain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white" alt="LangChain"/>
  <img src="https://img.shields.io/badge/django_channels-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django Channels"/>
  <img src="https://img.shields.io/badge/django_ninja-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django Ninja"/>
  <img src="https://img.shields.io/badge/ChromaDB-6E40C9?style=for-the-badge&logoColor=white" alt="ChromaDB"/>
</p>


## 📁 폴더 구조
```
📂 프로젝트 루트
├── 📂 accounts
├── 📂 chatbot
├── 📂 community
├── 📂 config
│    ├── 📜 asgi.py
│    ├── 📜 celery.py
│    ├── 📜 settings.py
│    ├── 📜 urls.py
│    └── 📜 wsgi.py
├── 📂 node_server
├── 📜 .env
├── 📜 .gitignore
├── 📜 Dockerfile
├── 📜 docker-compose.yml
├── 📜 manage.py
├── 📜 requirements.txt
├── 📜 README.md
```

## 🤝 기여 방법

    1.이슈를 확인하고 작업할 항목을 선택하세요.
    2.새로운 브랜치를 생성하고 작업을 수행하세요.
    3. Pull Request를 생성하여 변경 사항을 공유하세요.


## 📄 라이선스
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## 📬 문의 및 연락처
프로젝트에 대한 문의사항은 다음으로 연락주세요:
- 이메일: imposterstudy@gmail.com
- 깃허브 이슈: [Open an issue](https://github.com/Imposter-study/TastePT/issues/new)
