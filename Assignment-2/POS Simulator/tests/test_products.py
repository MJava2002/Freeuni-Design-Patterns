from pos.products import Pack, SingleProduct


def test_product_name() -> None:
    beer_product = SingleProduct("Heineken", 6.5)
    assert beer_product.get_name() == "Heineken"


def test_product_price() -> None:
    beer_product = SingleProduct("Heineken", 6.5)
    assert beer_product.get_price() == 6.5


def test_product_count() -> None:
    beer_product = SingleProduct("Heineken", 6.5)
    assert beer_product.get_product_count() == 1


def test_product_compare() -> None:
    beer_product = SingleProduct("Heineken", 6.5)
    pc_product = SingleProduct("Lenovo", 2500.0)
    assert beer_product != pc_product


def test_pack_size() -> None:
    beer_pack = Pack(SingleProduct("Heineken", 6.5), 6)
    assert beer_pack.get_product_count() == 6


def test_pack_price() -> None:
    beer_pack = Pack(SingleProduct("Heineken", 6.5), 6)
    assert beer_pack.get_price() == 6.5


def test_pack_compare() -> None:
    beer_pack = Pack(SingleProduct("Heineken", 6.5), 6)
    pc_pack = Pack(SingleProduct("Lenovo", 2500.0), 2)
    assert beer_pack != pc_pack
