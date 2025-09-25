from db import get_all_groups, get_all_mentors, get_mentors_for_group

print("== Groups in DB ==")
for g in get_all_groups():
    print(g)

print("\n== Mentors in DB ==")
for m in get_all_mentors():
    print(m)

print("\n== Mentors per group ==")
groups = [g[1] for g in get_all_groups()]  # g[1] = group_name
for g in groups:
    mentors = get_mentors_for_group(g)
    print(f"Group: {g} -> Mentors: {mentors}")
