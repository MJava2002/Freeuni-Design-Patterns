from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

import pytest
from faker import Faker
from fastapi.testclient import TestClient

from runner.setup import init_app


@pytest.fixture
def client() -> TestClient:
    return TestClient(init_app())


@dataclass
class Fake:
    faker: Faker = field(default_factory=Faker)

    def product(
        self, unit_id: UUID, name: str = "", barcode: str = "", price: int = 0
    ) -> dict[str, Any]:
        return {
            "id": unit_id,
            "name": name or self.faker.name(),
            "barcode": barcode or self.faker.name(),
            "price": price or self.faker.name(),
        }


def test_should_not_read_unknown(client: TestClient) -> None:
    unknown_id = uuid4()

    response = client.get(f"/products/{unknown_id}")
    print(response)
    assert response.status_code == 404
    assert response.json() == {
        "error": {"message": f"Products with id<{unknown_id}> does not exist."}
    }


# tested manually but not with this tests both products and receipts and sales as well

# def test_should_create(client: TestClient) -> None:
#     # product = Fake().product()
#     # unknown_id = uuid4()
#     unit = Fake_unit().unit()
#     response_unit = client.post("/units", json=unit)
#     unit_id = response_unit.json()["unit"]["id"]
#     product = Fake().product(unit_id)
#     response = client.post("/products", json=product)
#
#     assert response.status_code == 201
#     assert response.json() == {"product": {"id": ANY, **product}}

#
# def test_should_persist(client: TestClient) -> None:
#     unit = Fake().product()
#
#     response = client.post("/units", json=unit)
#     unit_id = response.json()["unit"]["id"]
#
#     response = client.get(f"/units/{unit_id}")
#
#     assert response.status_code == 200
#     assert response.json() == {"id": unit_id, **unit}
#
#
# def test_get_all_product_on_empty(client: TestClient):
#     response = client.get("/units")
#
#     assert response.status_code == 200
#     assert response.json() == {"units": []}
#
#
# def test_get_all(client: TestClient):
#     unit = Fake().product()
#
#     response = client.post("/units", json=unit)
#     unit_id = response.json()["unit"]["id"]
#
#     response = client.get("/units")
#
#     assert response.status_code == 200
#     assert response.json() == {"units": [{"id": unit_id, **unit}]}
#
