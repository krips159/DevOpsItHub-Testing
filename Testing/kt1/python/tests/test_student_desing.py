from gilded_rose import Item, GildedRose


def test_ordinary_item_before_sell_date():
    item = Item("ordinary", 5, 10)
    GildedRose([item]).update_quality()

    assert item.sell_in == 4
    assert item.quality == 9


def test_ordinary_item_on_sell_date_boundary():
    item = Item("ordinary", 0, 10)
    GildedRose([item]).update_quality()

    assert item.sell_in == -1
    assert item.quality == 8


def test_conjured_item_before_sell_date():
    item = Item("Conjured Mana Cake", 5, 10)
    GildedRose([item]).update_quality()

    assert item.sell_in == 4
    assert item.quality == 8


def test_sulfuras_does_not_change():
    item = Item("Sulfuras, Hand of Ragnaros", 5, 80)
    GildedRose([item]).update_quality()

    assert item.sell_in == 5
    assert item.quality == 80
