import pytest
from fastapi.testclient import TestClient


class TestLaunchProbe:
    def test_returns_201_with_probe_at_origin(self, client: TestClient) -> None:
        response = client.post("/probes", json={"x": 5, "y": 5, "direction": "NORTH"})
        assert response.status_code == 201
        data = response.json()
        assert data["x"] == 0
        assert data["y"] == 0
        assert data["direction"] == "NORTH"
        assert "id" in data

    def test_returns_all_valid_directions(self, client: TestClient) -> None:
        for direction in ["NORTH", "SOUTH", "EAST", "WEST"]:
            response = client.post("/probes", json={"x": 5, "y": 5, "direction": direction})
            assert response.status_code == 201
            assert response.json()["direction"] == direction

    def test_invalid_direction_returns_422(self, client: TestClient) -> None:
        response = client.post("/probes", json={"x": 5, "y": 5, "direction": "UP"})
        assert response.status_code == 422

    def test_plateau_x_zero_returns_422(self, client: TestClient) -> None:
        response = client.post("/probes", json={"x": 0, "y": 5, "direction": "NORTH"})
        assert response.status_code == 422

    def test_plateau_y_zero_returns_422(self, client: TestClient) -> None:
        response = client.post("/probes", json={"x": 5, "y": 0, "direction": "NORTH"})
        assert response.status_code == 422

    def test_missing_fields_returns_422(self, client: TestClient) -> None:
        response = client.post("/probes", json={"direction": "NORTH"})
        assert response.status_code == 422

    def test_shrink_plateau_below_existing_probe_returns_409(self, client: TestClient) -> None:
        launch = client.post("/probes", json={"x": 10, "y": 10, "direction": "NORTH"})
        probe_id = launch.json()["id"]
        client.post(f"/probes/{probe_id}/commands", json={"commands": "MMMMM"})

        response = client.post("/probes", json={"x": 3, "y": 3, "direction": "EAST"})
        assert response.status_code == 409
        assert "out of bounds" in response.json()["detail"]


class TestSendCommands:
    def test_moves_probe_forward(self, client: TestClient) -> None:
        launch = client.post("/probes", json={"x": 5, "y": 5, "direction": "NORTH"})
        probe_id = launch.json()["id"]

        response = client.post(f"/probes/{probe_id}/commands", json={"commands": "MM"})
        assert response.status_code == 200
        data = response.json()
        assert data["x"] == 0
        assert data["y"] == 2

    def test_rotates_probe(self, client: TestClient) -> None:
        launch = client.post("/probes", json={"x": 5, "y": 5, "direction": "NORTH"})
        probe_id = launch.json()["id"]

        response = client.post(f"/probes/{probe_id}/commands", json={"commands": "R"})
        assert response.status_code == 200
        assert response.json()["direction"] == "EAST"

    def test_lowercase_commands_are_accepted(self, client: TestClient) -> None:
        launch = client.post("/probes", json={"x": 5, "y": 5, "direction": "NORTH"})
        probe_id = launch.json()["id"]

        response = client.post(f"/probes/{probe_id}/commands", json={"commands": "mm"})
        assert response.status_code == 200
        assert response.json()["y"] == 2

    def test_invalid_command_chars_return_422(self, client: TestClient) -> None:
        launch = client.post("/probes", json={"x": 5, "y": 5, "direction": "NORTH"})
        probe_id = launch.json()["id"]

        response = client.post(f"/probes/{probe_id}/commands", json={"commands": "MXZ"})
        assert response.status_code == 422

    def test_out_of_bounds_returns_422(self, client: TestClient) -> None:
        launch = client.post("/probes", json={"x": 1, "y": 1, "direction": "NORTH"})
        probe_id = launch.json()["id"]

        response = client.post(f"/probes/{probe_id}/commands", json={"commands": "MMM"})
        assert response.status_code == 422

    def test_probe_not_found_returns_404(self, client: TestClient) -> None:
        response = client.post("/probes/nonexistent/commands", json={"commands": "M"})
        assert response.status_code == 404

    def test_empty_commands_returns_422(self, client: TestClient) -> None:
        launch = client.post("/probes", json={"x": 5, "y": 5, "direction": "NORTH"})
        probe_id = launch.json()["id"]

        response = client.post(f"/probes/{probe_id}/commands", json={"commands": ""})
        assert response.status_code == 422


class TestListProbes:
    def test_returns_all_probes(self, client: TestClient) -> None:
        client.post("/probes", json={"x": 5, "y": 5, "direction": "NORTH"})
        client.post("/probes", json={"x": 5, "y": 5, "direction": "EAST"})

        response = client.get("/probes")
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_returns_empty_list_when_no_probes(self, client: TestClient) -> None:
        response = client.get("/probes")
        assert response.status_code == 200
        assert response.json() == []

    def test_response_includes_updated_positions(self, client: TestClient) -> None:
        launch = client.post("/probes", json={"x": 5, "y": 5, "direction": "NORTH"})
        probe_id = launch.json()["id"]
        client.post(f"/probes/{probe_id}/commands", json={"commands": "MMM"})

        probes = client.get("/probes").json()
        probe = next(p for p in probes if p["id"] == probe_id)
        assert probe["y"] == 3


class TestGetProbe:
    def test_returns_probe_by_id(self, client: TestClient) -> None:
        launch = client.post("/probes", json={"x": 5, "y": 5, "direction": "WEST"})
        probe_id = launch.json()["id"]

        response = client.get(f"/probes/{probe_id}")
        assert response.status_code == 200
        assert response.json()["id"] == probe_id
        assert response.json()["direction"] == "WEST"

    def test_nonexistent_probe_returns_404(self, client: TestClient) -> None:
        response = client.get("/probes/nonexistent")
        assert response.status_code == 404


class TestDeleteProbe:
    def test_returns_204_on_success(self, client: TestClient) -> None:
        launch = client.post("/probes", json={"x": 5, "y": 5, "direction": "NORTH"})
        probe_id = launch.json()["id"]

        response = client.delete(f"/probes/{probe_id}")
        assert response.status_code == 204
        assert response.content == b""

    def test_deleted_probe_no_longer_exists(self, client: TestClient) -> None:
        launch = client.post("/probes", json={"x": 5, "y": 5, "direction": "NORTH"})
        probe_id = launch.json()["id"]

        client.delete(f"/probes/{probe_id}")
        assert client.get(f"/probes/{probe_id}").status_code == 404

    def test_deleted_probe_removed_from_list(self, client: TestClient) -> None:
        launch = client.post("/probes", json={"x": 5, "y": 5, "direction": "NORTH"})
        probe_id = launch.json()["id"]

        client.delete(f"/probes/{probe_id}")
        ids = [p["id"] for p in client.get("/probes").json()]
        assert probe_id not in ids

    def test_nonexistent_probe_returns_404(self, client: TestClient) -> None:
        response = client.delete("/probes/nonexistent")
        assert response.status_code == 404



class TestHealthCheck:
    def test_returns_ok(self, client: TestClient) -> None:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"
