import asyncio
import json
from datetime import datetime
from playwright.async_api import async_playwright
from games import DATA_LIST


async def scrape_shop_data():
    for game_id, game_name in DATA_LIST.items():
        """KONAMI e-amusementページから全ページの店舗データを取得し、JSONで返す"""
        base_url = f"https://p.eagate.573.jp/game/facility/search/p/list.html?gkey={game_id}&paselif=false&finder=ll&latitude=11&longitude=11&page="
        shop_data = []
        page_num = 1

        async with async_playwright() as p:
            # ブラウザを起動
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            try:
                while True:
                    url = f"{base_url}{page_num}"
                    print(f"ページ {page_num} にアクセス中: {url}")

                    # ページにアクセス
                    await page.goto(url, wait_until="networkidle", timeout=30000)

                    # ページが完全に読み込まれるまで少し待機
                    await page.wait_for_timeout(3000)

                    # div class="cl_shop_bloc" 要素を取得
                    shop_blocks = await page.query_selector_all("div.cl_shop_bloc")
                    print(f"ページ {page_num} の店舗ブロック数: {len(shop_blocks)}")

                    # データが取得できない場合は終了
                    if len(shop_blocks) == 0:
                        print(f"ページ {page_num} にデータがありません。終了します。")
                        break

                    # 各店舗ブロックからdata属性を抽出
                    page_shop_data = []
                    for i, shop_block in enumerate(shop_blocks):
                        try:
                            # data属性を取得
                            data_name = await shop_block.get_attribute("data-name")
                            data_operationtime = await shop_block.get_attribute(
                                "data-operationtime"
                            )
                            data_holiday = await shop_block.get_attribute("data-holiday")
                            data_latitude = await shop_block.get_attribute("data-latitude")
                            data_longitude = await shop_block.get_attribute(
                                "data-longitude"
                            )
                            data_tel = await shop_block.get_attribute("data-telno")
                            data_address = await shop_block.get_attribute("data-address")
                            data_access = await shop_block.get_attribute("data-access")

                            # 店舗データを作成
                            shop_info = {
                                "name": data_name,
                                "operation_time": data_operationtime,
                                "holiday": data_holiday,
                                "latitude": data_latitude,
                                "longitude": data_longitude,
                                "tel": data_tel,
                                "address": data_address,
                                "access": data_access,
                                "games":[game_name]
                            }
                            print(shop_info)

                            page_shop_data.append(shop_info)
                            print(f"  店舗 {i + 1}: {data_name}")

                        except Exception as e:
                            print(f"  店舗ブロック {i} でエラー: {e}")
                            continue

                    # ページのデータを全体のリストに追加
                    shop_data.extend(page_shop_data)
                    print(
                        f"ページ {page_num} から {len(page_shop_data)} 個の店舗データを取得しました"
                    )

                    # 次のページボタンが存在するかチェック
                    # より具体的なセレクターで次へボタンを探す
                    next_page_selectors = [
                        'a[href*="page="]:not([href*="page=1"])',  # ページ1以外のページリンク
                        'a:has-text(">")',  # ">" テキストを含むリンク
                        'a:has-text("次へ")',  # "次へ" テキストを含むリンク
                        'a:has-text("Next")',  # "Next" テキストを含むリンク
                        'a[href*="page="]',  # ページリンク全般
                    ]

                    next_page_exists = False
                    print(f"ページ {page_num} の次へボタンを検索中...")

                    for selector in next_page_selectors:
                        try:
                            next_links = await page.query_selector_all(selector)
                            if next_links:
                                print(
                                    f"  セレクター '{selector}' で {len(next_links)} 個のリンクを発見"
                                )
                                # 現在のページ番号より大きいページ番号のリンクがあるかチェック
                                for link in next_links:
                                    href = await link.get_attribute("href")
                                    link_text = await link.inner_text()
                                    if href:
                                        print(f"    リンク: {link_text} -> {href}")
                                        if f"page={page_num + 1}" in href:
                                            next_page_exists = True
                                            print(
                                                f"    次のページ ({page_num + 1}) へのリンクを発見！"
                                            )
                                            break
                                if next_page_exists:
                                    break
                        except Exception as e:
                            print(f"  セレクター '{selector}' でエラー: {e}")
                            continue

                    # 次のページが存在しない場合は終了
                    if not next_page_exists:
                        print(
                            f"ページ {page_num} に次のページへのリンクがありません。最後のページのデータを取得しました。終了します。"
                        )
                        break

                    # 次のページに移動
                    page_num += 1

                    # 安全のため、最大100ページまで制限
                    if page_num > 100:
                        print("最大ページ数（100ページ）に達しました。終了します。")
                        break

                print(f"全ページから合計 {len(shop_data)} 個の店舗データを取得しました")

            except Exception as e:
                print(f"エラーが発生しました: {e}")

            finally:
                await browser.close()
            
        save_to_json(shop_data, filename=f'./data/{game_id}_shop_data.json')

    return shop_data


def save_to_json(data, filename="shop_data.json"):
    """データをJSONファイルに保存"""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"結果を {filename} に保存しました")
    except Exception as e:
        print(f"ファイル保存エラー: {e}")


def main():
    """メイン関数"""
    print("KONAMI e-amusementの全ページから店舗データを取得中...")
    print("データが取得できなくなるまで自動的に次のページに移動します。")
    print(f"取得開始時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 非同期関数を実行
    shop_data = asyncio.run(scrape_shop_data())

    # JSONとして出力
    result = {
        "shops": shop_data,
        "count": len(shop_data),
        "source": "https://p.eagate.573.jp/game/facility/search/p/list.html",
        "timestamp": datetime.now().isoformat(),
        "description": "KONAMI e-amusement店舗検索から取得した全店舗データ",
    }

    # コンソールに出力
    print("\n=== 取得完了 ===")
    print(f"総店舗数: {len(shop_data)}")
    print(f"取得完了時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    return result


if __name__ == "__main__":
    main()