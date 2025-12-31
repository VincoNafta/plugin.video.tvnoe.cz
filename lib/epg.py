from datetime import datetime, timezone

def getDisplayName(program, zacatek):
    name = program.get("nazev", "")
    cast = program.get("podnazev", "")
    displayedName = zacatek.strftime("%H.%M")
    if cast.strip() == "":
        displayedName += f" - {name}"
    else:
        displayedName += f" - {name} - {cast}"
    return displayedName

def getActualRelation(program_dnes, now_utc):
    for p in program_dnes:
        p["zacatek_dt"] = datetime.fromisoformat(p["zacatek"])

    zacali = [p for p in program_dnes if p["zacatek_dt"] <= now_utc.astimezone(p["zacatek_dt"].tzinfo)]

    if zacali:
        posledny = max(zacali, key=lambda x: x["zacatek_dt"])
        zacatek = posledny["zacatek_dt"]

        return getDisplayName(posledny, zacatek)
    else:
        return "Koniec vysielania"


def getActualProgram(channel, json_data):
    program_dnes = json_data["program"][channel]
    now_utc = datetime.now(timezone.utc)
    displayed_programs_str = f"{getActualRelation(program_dnes, now_utc)}\n"
    for program in program_dnes:

        zacatek = datetime.fromisoformat(program["zacatek"])

        now_local = now_utc.astimezone(zacatek.tzinfo)

        if now_local < zacatek:
            displayedName = getDisplayName(program, zacatek)
            displayed_programs_str += f"{displayedName}\n"
    return displayed_programs_str


def getNameDay(date, count):
    if count == 0:
        return str("Dnes")
    elif count == 1:
        return str("Zajtra")
    else:
        return str(date.strftime("%d.%m"))


def getProgram(channel_name, data):
    epg = []
    chanel_data = data.get("program").get(channel_name)

    for relation in chanel_data:
        nazev = relation.get("nazev")
        zacatek = datetime.fromisoformat(relation.get("zacatek")).strftime("%H:%M")
        epg.append(f"{zacatek} {nazev}")
    return "\n".join(epg)