import json
import glob
from pathlib import Path

def merge_by_name(pattern:str, out_file:str = 'stores.json')->None:
    # 同じnameが来たらgamesを追加していく
    merged: dict[str,dict] = {}

    for file in glob.glob(pattern):
        # jsonファイルを読み込む
        data = json.loads(Path(file).read_text(encoding="utf-8"))

        shops = data["shops"] if isinstance(data, dict) else data

        for shop in shops:
            print("DEBUG file:", file, "shop type:", type(shop), "shop value sample:", shop)
            name = shop['name']

            if name not in merged:
                merged[name] = dict(shop)
            else:
                merged[name]['games'].append(shop['games'][0])
            
    result = list(merged.values())
    
    Path(out_file).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')



if __name__ == "__main__":
    # dataフォルダ内のjsonを全部まとめる
    merge_by_name("./data/*.json", "./result/stores.json")