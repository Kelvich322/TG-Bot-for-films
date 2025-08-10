from models.database import Viewed_materials, Users


def add_viewed_material(login, material_name, material_url):
    try:
        user = Users.get(Users.login == login)
        Viewed_materials.create(
            user=user, material_name=material_name, material_url=material_url
        )
        print("Материал добавлен в просмотренные")
    except Users.DoesNotExist:
        print(f"Пользователь {login} не найден")


def get_viewed_materials(login):
    try:
        user = Users.get(Users.login == login)
        viewed_materials = list(
            Viewed_materials.select().where(Viewed_materials.user == user)
        )
        print("Получены просмотренные материалы по логину:", login)
        return viewed_materials
    except Users.DoesNotExist:
        print(f"Пользователь {login} не найден")
