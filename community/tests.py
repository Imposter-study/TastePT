from django.test import TestCase
from django.contrib.auth import authenticate, get_user_model
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from sympy import content

from .models import Post, Comment

User = get_user_model()


# Create your tests here.
class PostViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # 사용자 생성
        self.user = User.objects.create_user(
            email="test@test.com",
            password="pwpw1234",
            nickname="test",
        )

        self.user2 = User.objects.create_user(
            email="test2@test.com",
            password="pwpw1234",
            nickname="test2",
        )

        # 게시글 생성
        self.post = Post.objects.create(
            title="test title",
            content="test content",
            thumbnail=None,
            author=self.user,
        )

        # 로그인
        self.client.login(email="test@test.com", password="pwpw1234")

        # community 앱의 base url 설정
        self.base_url = "/api/v1/community/"

    # 게시글 목록 조회
    def test_get_post_list(self):
        self.client.logout()
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 200)

    # 게시글 생성
    def test_create_post(self):
        data = {
            "title": "test title",
            "content": "test content",
        }
        response = self.client.post(self.base_url, data)
        self.assertEqual(response.status_code, 201)

    # 로그인 없이 게시글 생성
    def test_create_post_without_authentication(self):
        self.client.logout()  # 로그아웃
        data = {
            "title": "test title",
            "content": "test content",
        }
        response = self.client.post(self.base_url, data)
        self.assertEqual(response.status_code, 403)

    # 잘못된 데이터로 게시글 생성
    def test_create_post_invalid_data(self):
        # 제목 누락
        data = {
            "content": "test content",
        }
        response = self.client.post(self.base_url, data)
        self.assertEqual(response.status_code, 400)

    # 게시글 상세 조회
    def test_get_post_detail(self):
        self.client.logout()
        response = self.client.get(f"{self.base_url}{self.post.id}/")
        self.assertEqual(response.status_code, 200)

    # 없는 게시글 조회
    def test_get_post_detail_no_post(self):
        self.client.logout()
        response = self.client.get(f"{self.base_url}2314341234/")
        self.assertEqual(response.status_code, 404)

    # 게시글 수정
    def test_edit_post(self):
        # 수정할 데이터
        data = {
            "title": "edit title",
            "content": "edit content",
        }
        response = self.client.put(f"{self.base_url}{self.post.id}/", data)
        self.assertEqual(response.status_code, 200)

    # 작성자가 아닌 유저가 게시글 수정
    def test_edit_post_not_author(self):
        self.client.logout()
        self.client.login(username="test2@test.com", password="pwpw1234")

        data = {
            "title": "edit title",
            "content": "edit content",
        }
        response = self.client.put(f"{self.base_url}{self.post.id}/", data)
        self.assertEqual(response.status_code, 403)

    # 게시글 삭제
    def test_delete_post(self):
        response = self.client.delete(f"{self.base_url}{self.post.id}/")
        self.assertEqual(response.status_code, 204)

    # 작성자가 아닌 유저가 게시글 삭제
    def test_delete_post_not_author(self):
        self.client.logout()
        self.client.login(username="test2@test.com", password="pwpw1234")

        response = self.client.delete(f"{self.base_url}{self.post.id}/")
        self.assertEqual(response.status_code, 403)

    # 댓글 생성
    def test_create_comment(self):
        data = {"content": "test comment", "post": self.post}
        response = self.client.post(f"{self.base_url}{self.post.id}/comment/", data)
        self.assertEqual(response.status_code, 201)

    # 로그인 없이 댓글 작성
    def test_create_comment_not_authenticated(self):
        self.client.logout()
        data = {"content": "test comment", "post": self.post}
        response = self.client.post(f"{self.base_url}{self.post.id}/comment/", data)
        self.assertEqual(response.status_code, 403)


class ComentViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # 사용자 생성
        self.user1 = User.objects.create_user(
            email="test@test.com",
            password="pwpw1234",
            nickname="test",
        )

        self.user2 = User.objects.create_user(
            email="test2@test.com",
            password="pwpw1234",
            nickname="test2",
        )

        self.post = Post.objects.create(
            title="test title",
            content="test content",
            author=self.user1,
        )

        # 댓글 생성
        self.comment = Comment.objects.create(
            content="test comment",
            author=self.user1,
            post=self.post,
        )

        # 댓글의 baseURL
        self.base_url = "/api/v1/community/comment/"

    # 댓글 수정
    def test_edit_comment(self):
        # 로그인
        self.client.login(username="test@test.com", password="pwpw1234")
        data = {"content": "edit comment"}
        response = self.client.put(f"{self.base_url}{self.comment.id}/", data)
        self.assertEqual(response.status_code, 200)

    # 잘못된 데이터로 댓글 수정
    def test_edit_content_invalid_data(self):
        # 로그인
        self.client.login(username="test@test.com", password="pwpw1234")
        data = {"content": ""}
        response = self.client.put(f"{self.base_url}{self.comment.id}/", data)
        self.assertEqual(response.status_code, 400)

    # 작성자가 아닌 유저가 댓글 수정
    def test_edit_content_not_author(self):
        # 로그인
        self.client.login(username="test2@test.com", password="pwpw1234")
        data = {"content": "edit comment"}
        response = self.client.put(f"{self.base_url}{self.comment.id}/", data)
        self.assertEqual(response.status_code, 403)

    # 댓글 삭제
    def test_delete_comment(self):
        # 로그인
        self.client.login(username="test@test.com", password="pwpw1234")
        response = self.client.delete(f"{self.base_url}{self.comment.id}/")
        self.assertEqual(response.status_code, 204)

    # 작성자가 아닌 유저가 댓글 삭제
    def test_delete_content_not_author(self):
        # 로그인
        self.client.login(username="test2@test.com", password="pwpw1234")
        response = self.client.delete(f"{self.base_url}{self.comment.id}/")
        self.assertEqual(response.status_code, 403)
