def explain(skill_data):

    good = []

    bad = []

    for s in skill_data["matched"]:

        good.append(
            f"มีทักษะ {s}"
        )

    for s in skill_data["missing"][:10]:

        bad.append(
            f"ขาด {s}"
        )

    return {

        "good": good,

        "bad": bad

    }