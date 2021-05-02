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
            
            titles_of_forum = re.findall(r'class="topictitle">(.*?)</a>', lines)
            
            matches = re.findall(r'" href="../forum_(.*?)/thread_(.*?)/thread_', lines)
            urls_of_forum = []
            for forum_id, thread_id in matches:
                urls_of_forum.append(f"http://forums.datarealms.com/viewtopic.php?f={forum_id}&t={thread_id}")
            
            for url, title in zip(urls_of_forum, titles_of_forum):
                titles.append(make_hyperlink(url, title))

            views += [int(i) for i in re.findall(r'<td class="row2" width="50" align="center"><p class="topicdetails">(.*?)</p></td>', lines)]
    
    lst = list(zip(titles, views))
    lst.sort(key=lambda x:x[1], reverse=True)
    df = pd.DataFrame(lst, columns=[ "Title", "Views" ])
    return df


def make_hyperlink(url, title):
    return f'=HYPERLINK("{url}", "{title}")'


def save_xls(dict_dfs, xls_path):
    with pd.ExcelWriter(xls_path) as writer:
        for sheet_name, df in dict_dfs.items():
            df.to_excel(writer, sheet_name, index=False)
            resize_column(writer, sheet_name, df)


def resize_column(writer, sheet_name, df):
    worksheet = writer.sheets[sheet_name]  # pull worksheet object
    
    idx = 0
    col = "Title"

    series = df[col]
    max_len = max((
        series.astype(str).map(len).max(),  # len of largest item
        len(str(series.name))  # len of column name/header
        )) + 1  # adding a little extra space
    max_len /= 2 # hyperlinks are about twice the width of their text
    
    worksheet.set_column(idx, idx, max_len)  # set column width


if __name__ == "__main__":
    mod_releases = get_data("mod_releases")
    scene_releases = get_data("scene_releases")
    older_mods = get_data("older_mods")

    save_xls({
        "Mod Releases": mod_releases,
        "Scene Releases": scene_releases,
        "Older Mods": older_mods,
    }, "Mods and Scenes on the Data Realms Fan Forums.xlsx")