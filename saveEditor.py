clear =     []
marisa =    [14,15]
robin =     [0,14,15,18]
chrom =     [0,1,14,15,16,18]
act2 =      [0,1,2,14,15,16,18]
sekibanki = [0,1,2,4,5,6,7,8,9,10,14,15,16,18,29,30,31,32]
kogasa =    [0,1,2,3,5,6,7,8,9,10,14,15,16,18,29,30,31,32]
kurohebi =  [0,1,2,3,4,6,7,8,9,10,14,15,16,18,29,30,31,32]
medias =    [0,1,2,3,4,5,7,8,9,10,14,15,16,18,29,30,31,32]
william =   [0,1,2,3,4,5,6,8,9,10,14,15,16,18,29,30,31,32]
neoma =     [0,1,2,3,4,5,6,7,9,10,14,15,16,18,29,30,31,32]
alfonse =   [0,1,2,3,4,5,6,7,8,10,14,15,16,18,29,30,31,32]
mark =      [0,1,2,3,4,5,6,7,8,9 ,14,15,16,18,29,30,31,32]
act3 =      [0,1,2,3,4,5,6,7,8,9,10,14,15,16,18,29,30,31,32]

#----------------------#
save = 0
update = sekibanki
#----------------------#

import os

dir_path = os.path.dirname(os.path.realpath(__file__))
txt_dir = os.path.join(dir_path, "txt", "save")
if not os.path.exists(txt_dir):
    os.makedirs(txt_dir)

def updateFile(file_number, positions):
    txt_dir = os.path.join(dir_path, "txt", "save")
    filename = os.path.join(txt_dir, f"{file_number}.txt")

    # Check if file exists, if not, create it with 100 zeros
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            f.write("0" * 100)

    # Read the content of the file
    with open(filename, 'r') as f:
        content = f.read()

    # Update the content of the file
    updated_content = ""
    for i in range(len(content)):
        if i in positions:
            updated_content += "1"
        else:
            updated_content += "0"

    # Write the updated content to the file
    with open(filename, 'w') as f:
        f.write(updated_content)


updateFile(save, update)

# v0.0.0.0.0.0.0.0.1-alpha.0.1
