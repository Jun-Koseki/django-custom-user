# django-custom-user

This is a sample project using the build-in authentication system in Django. 

This projects consists of:
* User login and logout
* Register a new user up with name, email address and password
* The user can change his or her profile and login password
* The user who have forgotten his or her password can reset password.

## DEMO
### Login
![Login](https://raw.githubusercontent.com/wiki/Jun-Koseki/django-custom-user/login_demo.gif)
### Register a new user
![Login](https://raw.githubusercontent.com/wiki/Jun-Koseki/django-custom-user/signup_demo.gif)
### Password reset
![Login](https://raw.githubusercontent.com/wiki/Jun-Koseki/django-custom-user/password_reset.gif)

## Functionality for :
### 1. Forced password change
* In the following cases, the application will forcibly transition to the password change page after the login is executed.
  * The logged-in user is using the initial password
  * The password has expired

### 2. Prohibit password reuse
* In addition to Django's standard password quality verification, this application prohibits the reuse of passwords.
* You can change the number of generations of previously used passwords to be banned from a constant `PASSWORD_HISTORY` in `settings.py`.
