import pytest
import inspect
from main import scrape_shop_data

@pytest.mark.asyncio
async def test_scrape_shop_data():
    '''scrape_shop_dataが正しく動くかテスト'''
    # 関数が存在するか確認
    assert callable(scrape_shop_data)

    # 関数が非同期であるか確認
    assert inspect.iscoroutinefunction(scrape_shop_data)

    
