from models.database import Users


def create_user(login, name):
    user, created = Users.get_or_create(login=login, defaults={"name": name})
    if created:
        print(f"Пользователь {login} создан.")
    return user


def get_user(login):
    try:
        return Users.get(Users.login == login)
    except Users.DoesNotExist:
        print("Пользователь не найден")
        return None
