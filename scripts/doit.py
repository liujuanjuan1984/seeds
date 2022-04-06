import os
import datetime
import json
from officy import JsonFile, Dir, File, Stime

father_dir = os.path.dirname(os.path.dirname(__file__))
seedsfile = os.path.join(father_dir, "data", "seeds.json")
infofile = os.path.join(father_dir, "data", "groupsinfo.json")


def search_groups(blocks_num=50, last_update_days=-30):
    groupsinfo = JsonFile(infofile).read()
    last_update = f"{Stime.days_later(datetime.date.today(),last_update_days)}"
    gids = []
    for group_id in groupsinfo:
        if groupsinfo[group_id]["highest_height"] >= blocks_num:
            if groupsinfo[group_id]["last_update"] >= last_update:
                gids.append(group_id)
    return gids


def _check_name(name):
    names = ["测试", "test", "mytest", "去中心"]
    for i in names:
        if i in name:
            return False
    return True


def init_mdfile(gids):
    seeds = JsonFile(seedsfile).read()
    groupsinfo = JsonFile(infofile).read()

    lines = []
    for gid in gids:
        seed = seeds.get(gid)
        if not seed:
            continue

        name = seed["group_name"]
        if not _check_name(name):
            continue

        if groupsinfo[gid]["abandoned"]:
            continue

        lines.extend(
            [
                f'### {seed["group_name"]}\n\n',
                f'{seed["app_key"]} | 区块高度: {groupsinfo[gid]["highest_height"]}\n\n',
                f'{Stime.ts2datetime(seed["genesis_block"]["TimeStamp"]).date()} 创建 | {groupsinfo[gid]["last_update"][:10]} 更新\n\n',
                "```seed\n",
                json.dumps(seed, ensure_ascii=False),
                "\n```\n\n",
            ]
        )

    File("seeds_toshare.md").writelines(lines)
    otherfile = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "docs",
        "rum-app",
        "README.md",
    )
    print(otherfile)
    data = File(otherfile).read()
    flag = "\n## 更多种子\n"
    lines = [data.split(flag)[0], flag, "\n"] + lines
    File(otherfile).writelines(lines)


if __name__ == "__main__":
    groupseeds = search_groups(blocks_num=20, last_update_days=-14)
    init_mdfile(groupseeds)
