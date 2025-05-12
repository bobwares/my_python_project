def test_crud_flow(client):
    payload = {
        "firstName": "Test",
        "middleName": None,
        "lastName": "User",
        "email": "test.user@example.com",
        "addresses": [{
            "type": "home",
            "street1": "1 Main St",
            "city": "City",
            "state": "ST",
            "postalCode": "12345",
            "country": "US"
        }],
        "phoneNumbers": [{
            "type": "mobile",
            "countryCode": "+1",
            "number": "5551234"
        }],
        "notificationPreferences": {
            "email": True,
            "sms": False,
            "push": False,
            "mail": False
        }
    }
    # Create
    resp = client.post("/customers", json=payload)
    assert resp.status_code == 201
    cust_id = resp.json()["id"]

    # Read
    assert client.get(f"/customers/{cust_id}").status_code == 200

    # List
    assert client.get("/customers").status_code == 200

    # Patch
    updated = client.patch(f"/customers/{cust_id}", json={"email": "updated@example.com"})
    assert updated.status_code == 200
    assert updated.json()["email"] == "updated@example.com"

    # Delete
    assert client.delete(f"/customers/{cust_id}").status_code == 204

    # Confirm deletion
    assert client.get(f"/customers/{cust_id}").status_code == 404
