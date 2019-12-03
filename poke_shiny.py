# coding: utf-8

'''PokeShiny

tkinterを使ってるのでpython3専用。
色違いイーブイが何個目の卵で生まれるかシミュレートするだけのクソの役にも立たんプログラム。
しかし作るのは楽しい。
'''

import os
import random
import tkinter as Tk


# 擬似色違い孵化
# 0通常出現率1/4096 1ひかおま所持3/same 2国際孵化6/same 3ひかおま国際孵化8/same
def poke_shiny(x):
    success = times = 0
    while success == 0:
        a = random.randint(1, 4096)
        times += 1
        if x == 0:
            if a == 1:
                success = 1
            else:
                continue
        elif x == 1:
            if a <= 3:
                success = 1
            else:
                continue
        elif x == 2:
            if a <= 6:
                success = 1
            else:
                continue
        else:
            if a <= 8:
                success = 1
            else:
                continue
    return '\n\nHey! I\'m %s th brother.' % times


class TkRoot(Tk.Frame):
    def __init__(self, master=None):
        Tk.Frame.__init__(self, master)
        self.master.geometry('300x300')
        self.master.title('TkRoot')

        frame = Tk.Frame(self)
        frame.pack()

        result = Tk.StringVar()
        result.set('')
        m = Tk.IntVar()
        m.set(0)
        eevee = f'image{os.sep}eevee.gif'
        self.img = Tk.PhotoImage(file=eevee)
        egg = f'image{os.sep}egg.gif'
        self.img2 = Tk.PhotoImage(file=egg)

        table = ('With nothing 1/4096', 'With hikaoma 1/1365', 'International hatching 1/683', 'Int\'l hatching with hikaoma 1/512')
        for l, name in enumerate(table):
            Tk.Radiobutton(self, text=name, value=l, variable=m).pack(anchor='w')

        if_second = Tk.IntVar()
        if_second.set(0)

        def foo():
            result.set(poke_shiny(m.get()))
            if if_second.get() < 1:
                Tk.Label(self, image=self.img).pack()
            if_second.set(1)
        Tk.Button(self, image=self.img2, pady=5, command=foo).pack()
        Tk.Label(self, textvariable=result).pack()


if __name__ == '__main__':
    tkroot = TkRoot()
    tkroot.pack()
    tkroot.mainloop()
