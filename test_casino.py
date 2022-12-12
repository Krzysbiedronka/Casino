from casino import Casino, Player
from pytest import raises


def test_player_typical():
    jacek = Player("Jacek")
    assert jacek.get_name() == 'Jacek'


def test_set_name_typical():
    jacek = Player("Jacek")
    assert jacek.get_name() == 'Jacek'
    jacek.set_name('Jacuś')
    assert jacek.get_name() == 'Jacuś'


def test_player_invalid():
    with raises(ValueError):
        Player()


def test_create_invalid_player():
    jacek = Player("Jacek")
    assert jacek.get_name() == 'Jacek'
    with raises(ValueError):
        jacek.set_name('')


def test_player_result_zero(monkeypatch):
    def fake_dice_roll(casino, player):
        player.set_dice([1, 2, 3, 4])
    monkeypatch.setattr('casino.Casino.throw_dice', fake_dice_roll)
    jacek = Player("Jacek")
    casino = Casino([jacek])
    casino.game([jacek])
    assert jacek.player_result() == 0


def test_player_result_only_evens(monkeypatch):
    def fake_dice_roll(casino, player):
        player.set_dice([2, 4, 6, 2])
    monkeypatch.setattr('casino.Casino.throw_dice', fake_dice_roll)
    jacek = Player("Jacek")
    casino = Casino([jacek])
    casino.game([jacek])
    assert jacek.player_result() == 16


def test_player_result_only_odds(monkeypatch):
    def fake_dice_roll(casino, player):
        player.set_dice([1, 3, 5, 1])
    monkeypatch.setattr('casino.Casino.throw_dice', fake_dice_roll)
    jacek = Player("Jacek")
    casino = Casino([jacek])
    casino.game([jacek])
    assert jacek.player_result() == 13


def test_player_result_pair(monkeypatch):
    def fake_dice_roll(casino, player):
        player.set_dice([1, 3, 4, 1])
    monkeypatch.setattr('casino.Casino.throw_dice', fake_dice_roll)
    jacek = Player("Jacek")
    casino = Casino([jacek])
    casino.game([jacek])
    assert jacek.player_result() == 2


def test_player_result_three(monkeypatch):
    def fake_dice_roll(casino, player):
        player.set_dice([1, 4, 4, 4])
    monkeypatch.setattr('casino.Casino.throw_dice', fake_dice_roll)
    jacek = Player("Jacek")
    casino = Casino([jacek])
    casino.game([jacek])
    assert jacek.player_result() == 16


def test_player_result_four_and_only_evens(monkeypatch):
    def fake_dice_roll(casino, player):
        player.set_dice([4, 4, 4, 4])
    monkeypatch.setattr('casino.Casino.throw_dice', fake_dice_roll)
    jacek = Player("Jacek")
    casino = Casino([jacek])
    casino.game([jacek])
    assert jacek.player_result() == 24


def test_player_result_three_and_only_odds(monkeypatch):
    def fake_dice_roll(casino, player):
        player.set_dice([3, 3, 3, 1])
    monkeypatch.setattr('casino.Casino.throw_dice', fake_dice_roll)
    jacek = Player("Jacek")
    casino = Casino([jacek])
    casino.game([jacek])
    assert jacek.player_result() == 13


def test_create_casino_typica():
    jacek = Player("Jacek")
    lidka = Player("Lidka")
    casino = Casino([jacek, lidka])
    assert casino.get_list_of_players() == [jacek, lidka]


def test_set_list_of_players():
    jacek = Player("Jacek")
    lidka = Player("Lidka")
    casino = Casino([jacek, lidka])
    assert casino.get_list_of_players() == [jacek, lidka]
    paweł = Player("Paweł")
    casino.set_list_of_players([jacek, paweł])
    assert casino.get_list_of_players() == [jacek, paweł]


def test_add_players():
    jacek = Player("Jacek")
    lidka = Player("Lidka")
    casino = Casino([jacek, lidka])
    assert casino.get_list_of_players() == [jacek, lidka]
    paweł = Player("Paweł")
    casino.add_player(paweł)
    assert casino.get_list_of_players() == [jacek, lidka, paweł]


def test_remove_players():
    jacek = Player("Jacek")
    lidka = Player("Lidka")
    paweł = Player("Paweł")
    casino = Casino([jacek, lidka, paweł])
    assert casino.get_list_of_players() == [jacek, lidka, paweł]
    casino.remove_player(paweł)
    assert casino.get_list_of_players() == [jacek, lidka]


def test_game_no_winner(monkeypatch):
    def fake_dice_roll(a, b):
        return [1, 2, 3, 4]
    monkeypatch.setattr('casino.Casino.throw_dice', fake_dice_roll)
    jacek = Player("Jacek")
    lidka = Player("Lidka")
    casino = Casino([jacek, lidka])
    assert casino.game([jacek, lidka]) == 0
    assert casino.play() == 'The game is unresolved.'


def test_game_winner(monkeypatch):
    def fake_dice_roll(casino, player):
        if player.get_name() == "Jacek":
            player.set_dice([1, 2, 3, 4])
        else:
            player.set_dice([2, 2, 2, 2])
    monkeypatch.setattr('casino.Casino.throw_dice', fake_dice_roll)
    jacek = Player("Jacek")
    lidka = Player("Lidka")
    casino = Casino([jacek, lidka])
    assert casino.game([jacek, lidka]) == "Lidka"
    assert casino.play() == "Lidka won the game!"


def test_2_games_same_players(monkeypatch):
    def fake_dice_roll_1(casino, player):
        if player.get_name() == "Jacek":
            player.set_dice([1, 2, 3, 4])
        else:
            player.set_dice([2, 2, 2, 2])
    monkeypatch.setattr('casino.Casino.throw_dice', fake_dice_roll_1)
    jacek = Player("Jacek")
    lidka = Player("Lidka")
    casino = Casino([jacek, lidka])
    assert casino.game([jacek, lidka]) == "Lidka"
    assert casino.play() == "Lidka won the game!"

    def fake_dice_roll_2(casino, player):
        if player.get_name() == "Jacek":
            player.set_dice([6, 6, 6, 6])
        else:
            player.set_dice([2, 2, 2, 2])
    monkeypatch.setattr('casino.Casino.throw_dice', fake_dice_roll_2)
    assert casino.game([jacek, lidka]) == "Jacek"
    assert casino.play() == "Jacek won the game!"
