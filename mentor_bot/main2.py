
from db import add_mentor, add_group, get_all_mentors, get_all_groups, get_mentor_by_name

def add_all_mentors():
    mentors = [
        (1, "Zeyad_Zahran", "Zeyad Zahran"),
        (2, "Moham6dFathy", "Mohamed Fathy"),
        (3, "Eman7arery", "Eman Elharery"),
        (4, "Zeeyad_x", "Zeyad Rafat"),
        (5, "Yansoon_the_orginal", "Anis Emad"),
        (6, "AbdoElkamed", "Abdulrahman Ibrahim"),
        (7, "Mesh_SpongeBob", "Basma Fawzy"),
        (8, "Rashadalsharpini", "Rashad Alsharpini"),
        (9, "mennatawfiq", "Menna Tawfiq"),
        (10, "a_3idinho", "Ahmed Elaidy"),
        (11, "schizofman", "islam ali"),
        (12, "Omar_sxmeh", "Omar sameh"),
        (13, "Mostafa_754", "Mostafa Mahmoud"),
        (14, "aya_at11", "Aya Atef"),
        (15, "basmala01010", "Basmala Abdelhakim"),
        (16, "m_e_n_n_a712", "Menna Elgharabawii"),
        (17, "Tahany30", "Tahany Emad"),
        (18, "ahmedtarekzaher", "Ahmed Tarek"),
        (19, "ShamsAlalfy", "Shams Yasser"),
        (20, "omarkhaled710", "Omar Khaled"),
        (21, "ebmuhmd", "Ibrahim Mohamed"),
        (22, "Oxsiso", "Maximus Helmy"),
        (23, "meedoomostafa", "Mohamed Ahmed"),
        (24, "noursaberrr", "Nour Saber"),
        (25, "sundus_said", "Sondos Said"),
        (26, "Mohamed_Said03", "Mohamed Said")
    ]
    
    for user_id, username, full_name in mentors:
        add_mentor(user_id, username, full_name)
        

def add_all_groups():
    groups = [
        (1, "level 0", "level0_group"),
        (2, "level 1", "level1_group"),
        (3, "level 2", "level2_group"),

    ]
    
    for group_id, group_name, telegram_id in groups:
        add_group(group_id, group_name, telegram_id)

def search_mentor():
    name = input("Enter mentor name to search: ")
    mentors = get_mentor_by_name(name)
    
    if mentors:
        print(f"\nFound {len(mentors)} mentor(s):")
        for mentor in mentors:
            print(f"ID: {mentor[0]} | Name: {mentor[2]} | Username: @{mentor[1]}")
    else:
        print("No mentors found with that name.")

if __name__ == "__main__":
    print("Starting data insertion...")
    
    print("\nAdding mentors...")
    add_all_mentors()
    
    print("\nAdding groups...")
    add_all_groups()
    
    print("\nAll mentors:")
    mentors = get_all_mentors()
    for mentor in mentors:
        print(f"ID: {mentor[0]} | Name: {mentor[2]} | Username: @{mentor[1]}")
    
    print("\nAll groups:")
    groups = get_all_groups()
    for group in groups:
        print(f"ID: {group[0]} | Name: {group[1]} | Telegram ID: {group[2]}")
    
    print(f"\nCompleted successfully!")
    print(f"Total mentors: {len(mentors)}")
    print(f"Total groups: {len(groups)}")
    
    print("\n" + "="*50)
    search_mentor()