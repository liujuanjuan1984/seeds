import os
from officepy import JsonFile, Dir

father_dir = os.path.dirname(os.path.dirname(__file__))
seedsfile = os.path.join(father_dir, "data", "seeds.json")


def remove_test_seeds():
    seeds = JsonFile(seedsfile).read()
    newseeds = {}
    for gid in seeds:
        name = seeds[gid]["group_name"]
        if not name.startswith(("mytest", "测试", "test")):
            newseeds[gid] = seeds[gid]
    JsonFile(seedsfile).write(newseeds)


if __name__ == "__main__":
    remove_test_seeds()
