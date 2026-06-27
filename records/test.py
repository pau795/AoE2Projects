from mgz.fast.header import parse

with open("in/rec_smurf_2.aoe2record", "rb") as f:
    header = parse(f)

for player in header["players"]:
    print(player["name"])
    print(player["civilization_id"])
    print(player["color_id"])
    print(player["position"])     # {"x": ..., "y": ...}