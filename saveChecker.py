
#------------#
save = 2
#------------#
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

def listFlags(file_number):
    txt_dir = os.path.join(dir_path, "txt", "save")
    filename = os.path.join(txt_dir, f"{file_number}.txt")

    if not os.path.exists(filename):
        raise ValueError(f"File {filename} does not exist")

    with open(filename, 'r') as f:
        content = f.read()

    flag_names = [
        "0 Marisa - Beaten",
        "1 Robin - Beaten",
        "2 Chrom - Beaten",
        "3 Sekibanki - Beaten",
        "4 Kogasa - Beaten",
        "5 Kurohebi - Beaten",
        "6 Medias - Beaten",
        "7 William - Beaten",
        "8 Neoma - Beaten",
        "9 Alfonse - Beaten",
        "10 Mark - Beaten",
        "11 Chromatik - Beaten",
        "12 Tokken - Beaten",
        "13 Waterhorse928 - Beaten",
        "14 Hakurei Shrine - Explored",
        "15 Hakurei Shrine - Talked",
        "16 Entered Rest Point",
        "17 Marisa - Lost",
        "18 Barracks - Entered",
        "19 Robin - Lost",
        "20 Chrom - Lost",
        "21 Sekibanki - Lost",
        "22 Kogasa - Lost",
        "23 Kurohebi - Lost",
        "24 Medias - Lost",
        "25 William - Lost",
        "26 Neoma - Lost",
        "27 Alfonse - Lost",
        "28 Mark - Lost",
        "29 Human Village - Entered",
        "30 Devanagara - Entered",
        "31 Arcton Fort - Entered",
        "32 My Castle - Entered"
    ]

    flags = []
    for i, value in enumerate(content):
        flag_name = flag_names[i] if i < len(flag_names) else f"Flag {i}"
        flag_value = "1" if value == "1" else "0"
        flags.append(f"{flag_name}: {flag_value}")

    return flags

flags = listFlags(save)
for flag in flags:
    print(flag)
