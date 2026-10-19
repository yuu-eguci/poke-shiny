"""noVNC 越しにブラウザから GUI を操作する E2E チェックです。

`docker compose up` で GUI を起動した状態で実行します。
引数で指定したディレクトリへ各ステップのスクリーンショットを保存します。
"""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

URL = 'http://127.0.0.1:6080/vnc.html?autoconnect=1'

# 300x300 の仮想ディスプレイ上の座標です。
FIRST_OPTION = {'x': 100, 'y': 12}
EGG_BUTTON = {'x': 150, 'y': 130}


def main(out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 400, 'height': 400})
        page.goto(URL)
        page.wait_for_function("document.querySelector('canvas')?.width === 300", timeout=30_000)
        canvas = page.locator('canvas')

        def shot(name):
            page.wait_for_timeout(1_000)
            return canvas.screenshot(path=out_dir / f'{name}.png')

        start = shot('1-start')

        # 条件を選ばずに卵を押すと、選択を促すメッセージが出ます。
        canvas.click(position=EGG_BUTTON)
        no_option = shot('2-no-option')

        # 条件を選んで卵を押すと、結果と色違いイーブイが出ます。
        canvas.click(position=FIRST_OPTION)
        canvas.click(position=EGG_BUTTON)
        hatched = shot('3-hatched')

        browser.close()

    assert start != no_option, 'Egg button click did not change the screen.'
    assert no_option != hatched, 'Hatching did not change the screen.'
    print(f'OK: screenshots saved to {out_dir}')


if __name__ == '__main__':
    main(Path(sys.argv[1]))
