import re

with open("c:\\version.txt") as f:
    myString = f.read()
myString_list = [item for item in myString.split(" ")]
for item in myString_list:
    try:
        a = re.search("(?P<url>https?://[^\s]+)", item).group("url")
        if (a[-3:] == "jpg"):
            print(a)
    except:
        pass

