import os, re
import pandas as pd


def get_data(folder):
    p = os.path.join("data", folder)

    titles = []
    views = []
    for filename in os.listdir(p):
        # The actual encoding is "us-ascii" according to "file -bi"
        with open(os.path.join(p, filename), encoding="latin-1") as f:
            lines = f.read()
            titles += re.findall(r'class="topictitle">(.*?)</a>', lines)
            views += [int(i) for i in re.findall(r'<td class="row2" width="50" align="center"><p class="topicdetails">(.*?)</p></td>', lines)]
    
    lst = list(zip(titles, views))
    lst.sort(key=lambda x:x[1], reverse=True)
    return pd.DataFrame(lst)


def save_xls(dict_dfs, xls_path):
    with pd.ExcelWriter(xls_path) as writer:
        for sheet_name, df in dict_dfs.items():
            df.to_excel(writer, sheet_name, index=False)
        writer.save()


if __name__ == "__main__":
    mod_releases = get_data("mod_releases")
    scene_releases = get_data("scene_releases")
    older_mods = get_data("older_mods")
    # print(mod_releases)

    save_xls({
        "Mod Releases": mod_releases,
        "Scene Releases": scene_releases,
        "Older Mods": older_mods,
    }, "test.xlsx")