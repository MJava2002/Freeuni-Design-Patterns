from dataclasses import dataclass, field
from typing import Any
from unittest.mock import ANY
from uuid import uuid4

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

    def unit(self, name: str = "") -> dict[str, Any]:
        return {
            "name": name or self.faker.name(),
        }


def test_should_not_read_unknown(client: TestClient) -> None:
    unknown_id = uuid4()
    response = client.get(f"/units/{unknown_id}")
    assert response.status_code == 404
    assert response.json() == {
        "error": {"message": f"Unit with id<{unknown_id}> does not exist."}
    }


def test_should_create(client: TestClient) -> None:
    unit = Fake().unit()

    response = client.post("/units", json=unit)

    assert response.status_code == 201
    assert response.json() == {"unit": {"id": ANY, **unit}}


def test_should_persist(client: TestClient) -> None:
    unit = Fake().unit()

    response = client.post("/units", json=unit)
    unit_id = response.json()["unit"]["id"]

    response = client.get(f"/units/{unit_id}")

    assert response.status_code == 200
    assert response.json() == {"id": unit_id, **unit}


def test_get_all_units_on_empty(client: TestClient) -> None:
    response = client.get("/units")

    assert response.status_code == 200
    assert response.json() == {"units": []}


def test_get_all(client: TestClient) -> None:
    unit = Fake().unit()

    response = client.post("/units", json=unit)
    unit_id = response.json()["unit"]["id"]

    response = client.get("/units")

    assert response.status_code == 200
    assert response.json() == {"units": [{"id": unit_id, **unit}]}
