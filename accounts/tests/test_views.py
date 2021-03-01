from django.contrib.auth import get_user_model
from django.test import TestCase


class TestAccountsView(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='user1', email='user1@example.com',
                                                         password='p@ssZaq12wsx')

    def test_get_signup(self):
        """ [SignUpView] ユーザ登録画面に遷移できることを検証 """
        res = self.client.get("/accounts/signup/")

        # アクセスに成功する
        self.assertEqual(res.status_code, 200)
        # フォームにエラーが出ていない
        self.assertFalse(res.context['form'].errors)
        # 利用テンプレートの検証
        self.assertTemplateUsed(res, 'registration/signup.html')

    def test_post_signup(self):
        """ 新規ユーザの登録処理ができることを検証 """
        res = self.client.post("/accounts/signup/", {
            'username': 'user2',
            'email': 'user2@example.com',
            'password1': 'p@ssZaq12wsx',
            'password2': 'p@ssZaq12wsx'
        })

        # ユーザ登録に成功すると メインコンテンツの top へリダイレクトする
        self.assertRedirects(res, '/myapp/')
        # ユーザが正しく登録されている
        self.assertTrue(get_user_model().objects.filter(username='user2').exists())

    def test_post_signup_error(self):
        """ 誤った入力値で新規ユーザの登録処理が失敗することを検証 """
        # すでに登録済みのメールアドレスを入力
        post_same_mail = self.client.post("/accounts/signup/", {
            'username': 'user3',
            'email': 'user1@example.com',
            'password1': 'p@ssZaq12wsx',
            'password2': 'p@ssZaq12wsx'
        })
        # エラーメッセージの検証
        self.assertFormError(post_same_mail, 'form', 'email', 'User with this Email already exists.')

    def test_login(self):
        """ 登録済みユーザでログインできることを検証 """
        logged_in = self.client.login(username=self.user.email, password='p@ssZaq12wsx')
        self.assertTrue(logged_in)
