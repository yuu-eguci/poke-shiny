import tkinter as tk

import pytest

import poke_shiny


def test_poke_shiny_returns_1_when_first_egg_is_shiny():
    assert poke_shiny.poke_shiny(4096) == 1


def test_poke_shiny_counts_eggs_until_shiny(monkeypatch):
    rolls = iter([4096, 9, 8])
    monkeypatch.setattr(poke_shiny.random, 'randint', lambda a, b: next(rolls))

    assert poke_shiny.poke_shiny(8) == 3


@pytest.mark.parametrize('x', [0, None])
def test_poke_shiny_rejects_invalid_rate(x):
    with pytest.raises(ValueError, match='is invalid value'):
        poke_shiny.poke_shiny(x)


@pytest.mark.parametrize(
    ('n', 'expected'),
    [
        (1, '1st'),
        (2, '2nd'),
        (3, '3rd'),
        (4, '4th'),
        (11, '11th'),
        (12, '12th'),
        (13, '13th'),
        (21, '21st'),
        (112, '112th'),
    ],
)
def test_ordinal(n, expected):
    assert poke_shiny.ordinal(n) == expected


@pytest.fixture
def app(monkeypatch, tmp_path):
    # 画像の読み込みがカレントディレクトリに依存しないことも確認します。
    monkeypatch.chdir(tmp_path)
    root = tk.Tk()
    frame = poke_shiny.TkRoot(master=root)
    frame.pack()
    root.update_idletasks()
    yield frame
    root.destroy()


def children_of(frame, widget_class):
    return [w for w in frame.winfo_children() if isinstance(w, widget_class)]


def test_window_has_title_size_and_rate_options(app):
    radiobuttons = children_of(app, tk.Radiobutton)

    assert app.master.title() == 'poke-shiny'
    assert app.master.geometry().startswith('300x300')
    assert [r.cget('text') for r in radiobuttons] == list(poke_shiny.WINNING_RATE_TABLE.values())


def test_egg_button_without_option_asks_to_select(app):
    children_of(app, tk.Button)[0].invoke()

    assert app.result_text.get() == 'Select valid option!'
    assert str(app.tk_eevee_image_label.cget('image')) == ''


def test_egg_button_shows_brother_number_and_shiny_eevee(app, monkeypatch):
    monkeypatch.setattr(poke_shiny.random, 'randint', lambda a, b: 1)
    children_of(app, tk.Radiobutton)[0].invoke()

    children_of(app, tk.Button)[0].invoke()

    assert app.result_text.get() == "\n\nHey! I'm 1st brother."
    assert str(app.tk_eevee_image_label.cget('image')) == str(app.tk_image_eevee)


def test_cli_hatches_once_with_rate(monkeypatch, capsys):
    monkeypatch.setattr(poke_shiny.random, 'randint', lambda a, b: 1)

    poke_shiny.main(['--rate', '8'])

    assert capsys.readouterr().out == "Hey! I'm 1st brother.\n"


def test_cli_prints_average_with_times(monkeypatch, capsys):
    rolls = iter([1, 4096, 1, 4096, 4096, 1])
    monkeypatch.setattr(poke_shiny.random, 'randint', lambda a, b: next(rolls))

    poke_shiny.main(['--rate', '8', '--times', '3'])

    assert capsys.readouterr().out == 'Average: 2.0 eggs (3 times)\n'


@pytest.mark.parametrize('argv', [['--rate', '2'], ['--rate', '8', '--times', '0'], ['--times', '3']])
def test_cli_rejects_invalid_arguments(argv):
    with pytest.raises(SystemExit):
        poke_shiny.main(argv)
