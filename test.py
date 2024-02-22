import os

print(os.getcwd())

with os.scandir(r'C:\Users\User\work\gym') as items:
    for item in items:
        if(item.is_dir()):
            print(item.name)

