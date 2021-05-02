import os, re


def get_data(folder):
    p = os.path.join("data", folder)

    titles = []
    views = []
    for filename in os.listdir(p):
        print(filename)
        # The actual encoding is "us-ascii" according to "file -bi"
        with open(os.path.join(p, filename), encoding="latin-1") as f:
            lines = f.read()
            titles += re.findall(r'class="topictitle">(.*?)</a>', lines)
            views += [int(i) for i in re.findall(r'<td class="row2" width="50" align="center"><p class="topicdetails">(.*?)</p></td>', lines)]
    
    lst = list(zip(titles, views))
    lst.sort(key=lambda x:x[1])
    return lst


if __name__ == "__main__":
    mod_releases = get_data("mod_releases")
    print(mod_releases)