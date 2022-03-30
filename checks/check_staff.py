import json

def check_staff(ctx):
    with open(".\\checks\\staff.json", "r") as ninjas:
        staff = json.load(ninjas)

    return ctx.author.id in staff
