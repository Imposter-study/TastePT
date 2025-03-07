# 베이스 이미지
FROM python:3.11

# 작업 디렉토리
WORKDIR /app

# requirements.txt를 컨테이너로 복사 후, 의존성 패키지 설치
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 로젝트 파일을 컨테이너의 /app으로 복사
COPY . /app/

# Django 서버 실행 포트 설정
EXPOSE 8000

# DB가 준비될 때까지 대기
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Run migrations and start the development server
CMD ["/wait-for-it.sh", "db:5432", "--", "python", "manage.py", "runserver", "0.0.0.0:8000"]