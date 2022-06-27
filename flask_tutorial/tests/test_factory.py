from flaskr import create_app

def test_config():
    """By default, testing should be false"""
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_hello(client):
    """Test the 'hello' view that comes with the app factory"""
    response = client.get('/hello')
    assert response.data == b'Hello, world'