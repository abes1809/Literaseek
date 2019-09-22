import pytest

def test_home(client):
	res = client.get("/home")
	page = res.data.decode("UTF-8")
	assert "Welcome" in page

