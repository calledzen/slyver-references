def seperate_number(nr):
    seperated_nr = ""
    for enu, part_nr in enumerate(str(nr)[::-1]):
        if (enu + 1) % 3 == 0 and enu != len(str(nr)) - 1:
            seperated_nr += part_nr + "."
        else:
            seperated_nr += part_nr
    return seperated_nr[::-1]