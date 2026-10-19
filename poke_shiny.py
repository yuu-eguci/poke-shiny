"""PokeShiny

色違いイーブイが何個目の卵で生まれるかシミュレートするだけのクソの役にも立たんプログラム。
しかし作るのは楽しい。
"""

import random
import tkinter as tk
from pathlib import Path

IMAGE_DIR = Path(__file__).resolve().parent / 'image'

WINNING_RATE_TABLE = {
    1: 'With nothing 1/4096',
    3: 'With hikaoma 1/1365',
    6: 'International hatching 1/683',
    8: "Int'l hatching with hikaoma 1/512",
}


def poke_shiny(x):
    """
    疑似色違い孵化を行います。
    色違いが生まれるまでに何個の卵が割られたかを返します。

    Parameters
    ----------
    x : int
        孵化の条件を指定。 x/4096 の確率で生まれる。

    Returns
    -------
    brother_num : int
        色違いが生まれるまでに割られた卵の数。
    """

    # 確率がゼロとか None では計算にならない。エラーを発生させます。
    if not x:
        raise ValueError(f'{x} is invalid value.')

    # x/4096 の確率で何度もトライし、成功したところでトライ回数を返します。
    brother_num = 0
    while 1:
        brother_num += 1
        if random.randint(1, 4096) <= x:
            return brother_num


def ordinal(n):
    """数値を英語の序数 (1st, 2nd, 3rd, 4th ...) にします。"""

    suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    # 11, 12, 13 は 1, 2, 3 で終わっていても th になります。
    if n % 100 in (11, 12, 13):
        suffix = 'th'
    return f'{n}{suffix}'


class TkRoot(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)

        # インスタンス変数: 結果メッセージ。
        self.result_text = tk.StringVar()
        self.result_text.set('')

        # インスタンス変数: Radiobutton の選択値。
        self.radiobutton_value = tk.IntVar()
        self.radiobutton_value.set(0)

        # インスタンス変数: 画像。
        # NOTE: なぜかわからないが、 Button(image=), Label(image=) に設定する PhotoImage は変数化しないと表示されない。
        self.tk_image_egg = tk.PhotoImage(file=IMAGE_DIR / 'egg.gif')
        self.tk_image_eevee = tk.PhotoImage(file=IMAGE_DIR / 'eevee.gif')

        # Frame の外観を作ります。
        self.__create_frame_appearance()

    def __create_frame_appearance(self):
        """Frame の外観を作ります。構造は以下のとおりです。
        - Root(300x300)
            - Frame
                - Four Radiobuttons
                - Button(egg button)
                - Label(result label)
                - Label(eevee img)
        """

        # Root。
        self.master.geometry('300x300')
        self.master.title('poke-shiny')

        # 4つのラジオボタンです。(4つなのは WINNING_RATE_TABLE が4つだからだけど。)
        for key, value in WINNING_RATE_TABLE.items():
            tk.Radiobutton(self, text=value, value=key, variable=self.radiobutton_value).pack(anchor='w')

        # 卵画像のボタンです。
        tk.Button(self, image=self.tk_image_egg, pady=5, command=self.__on_push_button).pack()

        # 結果を表示するラベルです。
        tk.Label(self, textvariable=self.result_text).pack()

        # 色違いイーブイの画像を表示するラベル。
        # NOTE:
        #   このラベルはボタンが押されたときはじめて画像を表示します。
        #   外部からアクセスするためインスタンス変数にします。
        self.tk_eevee_image_label = tk.Label(self)
        self.tk_eevee_image_label.pack()

    def __on_push_button(self):
        """ボタンが押されたときのイベントです。"""

        # すでに表示されている色違いイーブイ画像を取り払います。
        self.tk_eevee_image_label.config(image='')

        # 選択されている条件で孵化実験を行い、何番目の兄弟で色違いが生まれたか取得します。
        try:
            brother_num = poke_shiny(self.radiobutton_value.get())
        except ValueError:
            self.result_text.set('Select valid option!')
            return

        # 結果メッセージを表示します。
        self.result_text.set(f"\n\nHey! I'm {ordinal(brother_num)} brother.")

        # 色違いイーブイ画像を表示します。
        self.tk_eevee_image_label.config(image=self.tk_image_eevee)


def main():
    tkroot = TkRoot()
    tkroot.pack()
    tkroot.mainloop()


if __name__ == '__main__':
    main()
