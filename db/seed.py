from db.db import add_user, get_all_users


add_user("abdo", "111111", "Abdelrahman Elaraby")
add_user("sara", "222222", "Sara Ali")
add_user("ahmed", "333333", "Ahmed Mohamed")


print("\n=== Users ===")
for user in get_all_users():
    print(user)
