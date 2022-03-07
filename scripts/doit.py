import os
import datetime
import json
from officepy import JsonFile, Dir, File, Stime

father_dir = os.path.dirname(os.path.dirname(__file__))
seedsfile = os.path.join(father_dir, "data", "seeds.json")
infofile = os.path.join(father_dir, "data", "groupsinfo.json")


def remove_test_seeds():
    seeds = JsonFile(seedsfile).read()
    newseeds = {}
    for gid in seeds:
        if "error" in seeds[gid]:
            continue
        name = seeds[gid]["group_name"]
        if not name.startswith(("mytest", "测试", "test")):
            newseeds[gid] = seeds[gid]
    JsonFile(seedsfile).write(newseeds)


def search_groups(blocks_num=50, last_update_days=-30):

    groupsinfo = JsonFile(infofile).read()

    gids = []
    for group_id in groupsinfo:
        if groupsinfo[group_id]["highest_height"] >= blocks_num:
            if (
                groupsinfo[group_id]["last_update"]
                >= f"{Stime.days_later(datetime.date.today(),last_update_days)}"
            ):
                gids.append(group_id)
    return gids


def init_mdfile(gids):
    seeds = JsonFile(seedsfile).read()
    groupsinfo = JsonFile(infofile).read()

    lines = []
    for gid in gids:
        seed = seeds[gid]
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


if __name__ == "__main__":
    remove_test_seeds()
    groupseeds = search_groups()
    init_mdfile(groupseeds)
