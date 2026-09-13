import struct
from xar_dom_engine import XarDocument

doc = XarDocument(r"C:\Users\Lenovo\Downloads\TEST_REK_ANTIGRAVITY.xar")
print(f"{'Row':4s} | {'Nominal':15s} | {'Nom X':8s} | {'Nom W':8s} | {'Nom Right':10s} | {'Balance':15s} | {'Bal X':8s} | {'Bal W':8s} | {'Bal Right':10s}")
print("-" * 105)
for t in doc.get_transactions():
    ns = t["nom_story"]
    bs = t["bal_story"]
    nom_txt = t["nominal"]
    bal_txt = t["balance"]
    nom_x, nom_w, nom_r = 0, 0, 0
    if ns and ns["line_indices"]:
        nom_x = ns["x"]
        lrec = doc.records[ns["line_indices"][0]]
        nom_w = struct.unpack("<i", lrec["payload"][:4])[0]
        nom_r = nom_x + nom_w
    bal_x, bal_w, bal_r = 0, 0, 0
    if bs and bs["line_indices"]:
        bal_x = bs["x"]
        lrec = doc.records[bs["line_indices"][0]]
        bal_w = struct.unpack("<i", lrec["payload"][:4])[0]
        bal_r = bal_x + bal_w
    print(f"{t['row']:4d} | {nom_txt:15s} | {nom_x:8d} | {nom_w:8d} | {nom_r:10d} | {bal_txt:15s} | {bal_x:8d} | {bal_w:8d} | {bal_r:10d}")
