from mentor_bot.db import create_tables, add_group, add_mentor, get_all_groups, get_all_mentors

def seed_groups():
    groups = [
        (1, "Technical Team", "https://t.me/+GUPRuwMJRdJlMTY0"),
        (2, "level 0", "https://t.me/+mHTl8iUQ1DwzMmJk"),
        (3, "level 1", "https://t.me/+Eai4LtgcEg1iNzlk"),
        (4, "level 2", "https://t.me/+HE4y8LhjrGFmYjI0")
    ]
    for group_id, group_name, telegram_id in groups:
        add_group(group_id, group_name, telegram_id)

def seed_mentors():
    mentors = [
      (1, "Iplo2", "Abdallh Ashraf", 1),
        (2, "gregorsamsa_0", "Abdullah Maher", 1),
        (3, "yousef_elgendy77", "Yousef Elgendy", 2),
        (4, "abdoshbr3344", "Abdullah Elshebrawy", 2),
        (5, "Mennawalid12", "Menna Walid", 3),
        (6, "Shamsashraaf", "Shams Ashraf", 3),
        (7, "Mesh_SpongeBob", "Basma Fawzy", 1),
        (8, "Rashadalsharpini", "Rashad Alsharpini", 1),
        (9, "mennatawfiq", "Menna Tawfiq", 2),
        (10, "a_3idinho", "Ahmed Elaidy", 2),
        (11, "schizofman", "Islam Ali", 2),
        (12, "Abdulr7man_Alaa", "Abdulrhman Alaa", 2),
        (13, "Mostafa_754", "Mostafa Mahmoud", 3),
        (14, "aya_at11", "Aya Atef", 3),
        (15, "basmala01010", "Basmala Abdelhakim", 3),
        (16, "menna_elgharabawii", "Menna Elgharabawii", 3),
        (17, "Tahany30", "Tahany Emad", 3),
        (18, "ahmedtarekzaher", "Ahmed Tarek", 1),
        (19, "ShamsAlalfy", "Shams Yasser", 1),
        (20, "omarkhaled710", "Omar Khaled", 1),
        (21, "ebmuhmd", "Ibrahim Mohamed", 2),
        (22, "Oxsiso", "Maximus Helmy", 2),
        (23, "meedoomostafa", "Mohamed Ahmed", 2),
        (24, "noursaberrr", "Nour Saber", 3),
        (25, "sundus_said", "Sondos Said", 3),
        (26, "ZiZ0U01", "Ahmed Abdelaziz", 3),
        (27, "token7g", "ibrahem mohamed", 3),
        (28, "asmtar", "Asmaa Tarek", 3),
        (29, "AhmedDi6b", "Ahmed shehta Diab", 3),
    ]
    for user_id, username, full_name, group_id in mentors:
        add_mentor(user_id, username, full_name, group_id)

if __name__ == "__main__":
    create_tables()
    seed_groups()
    seed_mentors()

    print("✅ Groups:")
    for g in get_all_groups():
        print(g)

    print("\n✅ Mentors:")
    for m in get_all_mentors():
        print(m)
