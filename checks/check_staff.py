import json

def check_staff(ctx):
    with open(".\\checks\\staff.json", "r") as members:
        staff = json.load(members)

    return ctx.author.id in staff
