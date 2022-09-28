from os.path import dirname as up


file_loc = up(up(__file__))

with open(f'{file_loc}\\secret.txt', 'r') as f:
    TOKEN = f.read()
    f.close()
