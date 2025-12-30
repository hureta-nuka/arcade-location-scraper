import json
from pathlib import Path
from main import save_to_json
import pytest

@pytest.fixture
def test_data():
    '''テストデータ'''
    return  {
        "shops": [{
            "name": "アミパラ佐世保店",
            "operation_time": "10:00～24:00",
            "holiday": "無し",
            "latitude": "33.15005741",
            "longitude": "129.7804145",
            "tel": "0956-34-8880",
            "address": "佐世保市大塔町18-15",
            "access": "JR大塔駅徒歩3分"
            }
        ],
        "count": 378,
        "source": "https://p.eagate.573.jp/game/facility/search/p/list.html",
        "timestamp": "2025-10-25T22:04:58.788059",
        "description": "KONAMI e-amusement店舗検索から取得した全店舗データ"
    }

def test_save_to_json(tmp_path: Path, test_data: dict):
    '''save_to_jsonが正しく動くかテスト'''
    # 関数が存在するか確認
    assert callable(save_to_json)

    # テスト用ファイルパス
    test_file = tmp_path / "test_shop_data.json"

    # テストデータ保存
    save_to_json(test_data, test_file)

    # ファイル生成確認
    assert test_file.exists(), "ファイルが生成されていません。"

    # ファイル内容確認
    with open(test_file, "r", encoding="utf-8") as f:
        loaded_data = json.load(f)

    assert loaded_data == test_data, "ファイル内容が一致していません。"

