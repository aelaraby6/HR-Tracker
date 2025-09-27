from db import create_tables, add_group, add_mentor, get_all_groups, get_all_mentors

def seed_groups():
    groups = [
        (1, "Technical Team", "https://t.me/+GUPRuwMJRdJlMTY0"),
        (2, "level 0", "https://t.me/+EqvK_VCJetxkZWM0"),
        (3, "level 1", "https://t.me/+Wog9T2AvN9FhZmM0"),
        (4, "level 2", "level2_group")
    ]
    for group_id, group_name, telegram_id in groups:
        add_group(group_id, group_name, telegram_id)

def seed_mentors():
    mentors = [
      (1, "Zeyad_Zahran", "Zeyad Zahran", 1),
        (2, "Moham6dFathy", "Mohamed Fathy", 1),
        (3, "Eman7arery", "Eman Elharery", 2),
        (4, "Zeeyad_x", "Zeyad Rafat", 2),
        (5, "Yansoon_the_orginal", "Anis Emad", 3),
        (6, "AbdoElkamed", "Abdulrahman Ibrahim", 3),
        (7, "Mesh_SpongeBob", "Basma Fawzy", 1),
        (8, "Rashadalsharpini", "Rashad Alsharpini", 1),
        (9, "mennatawfiq", "Menna Tawfiq", 2),
        (10, "a_3idinho", "Ahmed Elaidy", 2),
        (11, "schizofman", "Islam Ali", 2),
        (12, "Omar_sxmeh", "Omar Sameh", 2),
        (13, "Mostafa_754", "Mostafa Mahmoud", 3),
        (14, "aya_at11", "Aya Atef", 3),
        (15, "basmala01010", "Basmala Abdelhakim", 3),
        (16, "m_e_n_n_a712", "Menna Elgharabawii", 3),
        (17, "Tahany30", "Tahany Emad", 3),
        (18, "ahmedtarekzaher", "Ahmed Tarek", 1),
        (19, "ShamsAlalfy", "Shams Yasser", 1),
        (20, "omarkhaled710", "Omar Khaled", 1),
        (21, "ebmuhmd", "Ibrahim Mohamed", 2),
        (22, "Oxsiso", "Maximus Helmy", 2),
        (23, "meedoomostafa", "Mohamed Ahmed", 2),
        (24, "noursaberrr", "Nour Saber", 3),
        (25, "sundus_said", "Sondos Said", 3),
        (26, "Mohamed_Said03", "Mohamed Said", 3)
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
