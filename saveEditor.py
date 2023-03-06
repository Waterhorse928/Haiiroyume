clear = []
marisa = [14,15]
robin = [0,14,15,18]
chrom = [0,1,14,15,16,18]
act2 = [0,1,2,14,15,16,18]

#----------------------#
save = 0
update = act2
#----------------------#

import os

dir_path = os.path.dirname(os.path.realpath(__file__))

def updateFile(file_number, positions):
    txt_dir = os.path.join(dir_path, "txt", "save")
    filename = os.path.join(txt_dir, f"{file_number}.txt")

    if not os.path.exists(filename):
        raise ValueError(f"File {filename} does not exist")

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
