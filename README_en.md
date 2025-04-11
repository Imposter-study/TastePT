# TastePT
🇰🇷 [Korean](./README-en.md) | 🇺🇸 English
## Introduction
### Team
Imposter Study Club

### Project
Recipe Chatbot for Lazy Perfectionists
👉 [TastePT SA Document](https://www.notion.so/SA-1a97d4611a6f805d8bdbe9ae94405f62?pvs=4)
👉 [TastePT Website](https://dev.tastept.store/)

## ✨ Main Features
### 👤 User Features

<details>
  <summary>Sign up, Login, Logout, Account Deletion</summary>
  
  - **Sign up**
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
      - Password: Minimum 8 characters
      - Email: Validity check
      - Nickname: Maximum 30 characters
      - Password confirmation
    - **Email Verification**:
      - Automatic email verification sent upon signup
      - Account activation by clicking verification link
      - Verification URL: `GET /api/v1/accounts/verify-email/<token>/`
      - **Response**:
        - 201: Successful signup (awaiting email verification)
        - 400: Validation failed

  - **Login**
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
        "detail": "Login successful",
        "nickname": "string"
      }
      ```
    - **Status Codes**:
      - 200: Login successful
      - 401: Authentication failed

  - **Logout**
    - **Endpoint**: `POST /api/v1/accounts/signout/`
    - **Response**:
      ```json
      {
        "detail": "Logout successful"
      }
      ```
    - **Status Codes**:
      - 200: Logout successful

  - **Account Deletion**
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
        "message": "The account has been deactivated."
      }
      ```
    - **Status Codes**:
      - 200: Deletion successful
      - 400: Password mismatch
</details>

<details>
  <summary>Profile View, Profile Edit</summary>
  
  - **Profile View**
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
      - 200: View successful
      - 404: User not found

  - **Profile Edit**
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
        "detail": "Profile successfully updated"
      }
      ```
    - **Status Codes**:
      - 200: Edit successful
      - 400: Validation failed
</details>

<details>
  <summary>Random Nickname Generation</summary>
  
  - **Endpoint**: `GET /api/v1/accounts/random_nickname/`
  - **Response**:
    ```json
    {
      "nickname": "random_nickname"
    }
    ```
  - **Function Description**:
    - Generates unique nickname by combining adjectives and nouns
    - Automatically generated nickname can be used immediately
    - Automatic duplicate check
  - **Status Codes**:
    - 200: Random nickname generation successful
    - 500: Nickname generation failed
</details>

<details>
  <summary>Password Change</summary>
  
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
    - Current password verification
    - New password:
      - Minimum 8 characters
      - Includes uppercase and lowercase letters, numbers, special characters
    - Password confirmation
  - **Response**:
    ```json
    {
      "detail": "Password successfully changed"
    }
    ```
  - **Status Codes**:
    - 200: Change successful
    - 400: Validation failed
</details>

<details>
  <summary>Social Login</summary>
  
  - **Kakao Login**
    - **Authentication URL**: `GET /api/v1/accounts/social/signin/kakao/`
    - **Callback**: `GET /api/v1/accounts/social/callback/kakao`
    - **Redirect**: Frontend domain
</details>

### 🤖 Chatbot
<details>
  <summary>Chat Room Management</summary>
  
  - **Create Chat Room**
    - **Endpoint**: `POST /api/chatbot/room/`
    - **Body**:
      ```json
      {
        "name": "string",
        "user": "string"
      }
      ```
    - **Status Codes**:
      - 201: Chat room created successfully
      - 400: Missing required parameters
      - 401: Unauthorized user

  - **Edit Chat Room Name**
    - **Endpoint**: `PUT /api/chatbot/room/{room_id}/`
    - **Body**:
      ```json
      {
        "name": "string"
      }
      ```
    - **Status Codes**:
      - 200: Chat room name edited successfully
      - 400: Missing required parameters
      - 401: Unauthorized user
      - 403: Unauthorized user
      - 404: Chat room not found

  - **Delete Chat Room**
    - **Endpoint**: `DELETE /api/chatbot/room/{room_id}/`
    - **Response**:
      ```json
      {
        "message": "Chat room deleted successfully"
      }
      ```
    - **Status Codes**:
      - 200: Chat room deleted successfully
      - 401: Unauthorized user
      - 403: Unauthorized user
      - 404: Chat room not found
</details>

<details>
  <summary>Recipe Chatbot</summary>
  
  - **Recipe Question**
    - **Endpoint**: `POST /api/chatbot/room/{room_id}/message/`
    - **Body**:
      ```json
      {
        "query": "string"
      }
      ```
    - **Status Codes**:
      - 200: Recipe recommendation successful
      - 400: Missing required parameters
      - 401: Unauthorized user
      - 404: Chat room not found
      - 500: Error occurred during recipe recommendation
</details>

### 📝 Community
<details>
  <summary>Post Management</summary>
  
  - **Post List**
    - **Endpoint**: `GET /api/community/`
    - **Response**:
      ```json
      {
        "count": "integer",
        "next": "string",
        "previous": "string",
        "results": [
          {
            "id": "integer",
            "title": "string",
            "content": "string",
            "author": "string",
            "created_at": "datetime",
            "updated_at": "datetime",
            "likes_count": "integer",
            "comments_count": "integer"
          }
        ]
      }
      ```
    - **Status Codes**:
      - 200: Post list retrieved successfully
      - 400: Invalid request parameters

  - **Create Post**
    - **Endpoint**: `POST /api/community/`
    - **Body**:
      ```json
      {
        "title": "string",
        "content": "string"
      }
      ```
    - **Status Codes**:
      - 201: Post created successfully
      - 400: Missing required parameters
      - 401: Unauthorized user

  - **Edit Post**
    - **Endpoint**: `PUT /api/community/{post_id}/`
    - **Body**:
      ```json
      {
        "title": "string",
        "content": "string"
      }
      ```
    - **Status Codes**:
      - 200: Post edited successfully
      - 400: Missing required parameters
      - 401: Unauthorized user
      - 403: Unauthorized user
      - 404: Post not found

  - **Delete Post**
    - **Endpoint**: `DELETE /api/community/{post_id}/`
    - **Status Codes**:
      - 204: Post deleted successfully
      - 401: Unauthorized user
      - 403: Unauthorized user
      - 404: Post not found
</details>

<details>
  <summary>Comment Management</summary>
  
  - **Create Comment**
    - **Endpoint**: `POST /api/community/{post_id}/comment/`
    - **Body**:
      ```json
      {
        "content": "string"
      }
      ```
    - **Status Codes**:
      - 201: Comment created successfully
      - 400: Missing required parameters
      - 401: Unauthorized user
      - 404: Post not found

  - **Edit Comment**
    - **Endpoint**: `PUT /api/community/comment/{comment_id}/`
    - **Body**:
      ```json
      {
        "content": "string"
      }
      ```
    - **Status Codes**:
      - 200: Comment edited successfully
      - 400: Missing required parameters
      - 401: Unauthorized user
      - 403: Unauthorized user
      - 404: Comment not found

  - **Delete Comment**
    - **Endpoint**: `DELETE /api/community/comment/{comment_id}/`
    - **Status Codes**:
      - 204: Comment deleted successfully
      - 401: Unauthorized user
      - 403: Unauthorized user
      - 404: Comment not found
</details>

<details>
  <summary>Reply Comment Management</summary>
  
  - **Create Reply Comment**
    - **Endpoint**: `POST /api/community/{post_id}/comment/{comment_id}/reply/`
    - **Body**:
      ```json
      {
        "content": "string"
      }
      ```
    - **Status Codes**:
      - 201: Reply comment created successfully
      - 400: Missing required parameters
      - 401: Unauthorized user
      - 404: Post or comment not found

  - **Edit Reply Comment**
    - **Endpoint**: `PUT /api/community/comment/{reply_id}/`
    - **Body**:
      ```json
      {
        "content": "string"
      }
      ```
    - **Status Codes**:
      - 200: Reply comment edited successfully
      - 400: Missing required parameters
      - 401: Unauthorized user
      - 403: Unauthorized user
      - 404: Reply comment not found

  - **Delete Reply Comment**
    - **Endpoint**: `DELETE /api/community/comment/{reply_id}/`
    - **Status Codes**:
      - 204: Reply comment deleted successfully
      - 401: Unauthorized user
      - 403: Unauthorized user
      - 404: Reply comment not found
</details>

<details>
  <summary>Report Feature</summary>
  
  - **Report Post**
    - **Endpoint**: `POST /api/community/{post_id}/report/`
    - **Body**:
      ```json
      {
        "reason": "string"
      }
      ```
    - **Status Codes**:
      - 201: Post reported successfully
      - 400: Missing required parameters
      - 401: Unauthorized user
      - 403: Already reported post
      - 404: Post not found

  - **Report Comment**
    - **Endpoint**: `POST /api/community/comment/{comment_id}/report/`
    - **Body**:
      ```json
      {
        "reason": "string"
      }
      ```
    - **Status Codes**:
      - 201: Comment reported successfully
      - 400: Missing required parameters
      - 401: Unauthorized user
      - 403: Already reported comment
      - 404: Comment not found
</details>

## 🚀 Installation and Execution
```sh
# Clone the project
git clone https://github.com/Imposter-study/TastePT

# Install dependencies
pip install -r requirements.txt

# Database migration
python manage.py migrate

# Run the development server
python manage.py runserver
```

## 🔧 Environment Variable Settings
Create a `.env` file and set the following variables:

```
# Django
SECRET_KEY=
DEBUG=True
ALLOWED_HOSTS=

# Database
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=

# Email
EMAIL_HOST=
EMAIL_PORT=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_USE_TLS=

# Social Login
KAKAO_APP_KEY=
KAKAO_REDIRECT_URI=

# Frontend
FRONT_DOMAIN=
```

## 🛠 Technology Stack
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

## 📁 Folder Structure
```
📂 Project Root
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
```

## 🤝 Contribution Guidelines

    1. Check the issues and select a task to work on.
    2. Create a new branch and perform the task.
    3. Create a pull request to share the changes.

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## 📬 Contact and Inquiry
For any inquiries or questions about the project, please contact us at:
- Email: imposterstudy@gmail.com
- GitHub Issue: [Open an issue](https://github.com/Imposter-study/TastePT/issues/new)