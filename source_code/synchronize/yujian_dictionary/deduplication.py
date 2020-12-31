import os


file_list = os.listdir("./")
for file in file_list:
    new = set()
    if file.endswith("bak"):
        with open(file, "r", encoding="utf-8") as f:
            while True:
                line = f.readline()
                if not line:
                    break
                result = line.split("\n")[0]
                new.add(result+"\n")
        new_file_name = ".".join(file.split(".")[0:2])
        with open(new_file_name, "a", encoding="utf-8") as w:
            w.writelines(new)
