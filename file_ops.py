import os

def openFile(fileLoc, splitLines = True, option = "r", newText = ""):
    if option not in ["r", "a", "w"]:
        raise Exception("File option not supported")

    if option == "r":
        try:
            with open(fileLoc) as reader:
                data = reader.read().strip()
                if splitLines:
                    return data.split("\n")
                else:
                    return data
        except:
            raise Exception("Could not open file: {fileLoc}!")
    else:
        try:
            with open(fileLoc, option) as writer:
                writer.write(newText)
        except:
            raise Exception("Could not modify file: {fileLoc}!")

def pathExists(fileLoc):
    try:
        os.path.exists(fileLoc)
    except:
        raise Exception(f"Path does not exist: {fileLoc}")

