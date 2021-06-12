import json


def test_get_artist(test_app):
    response = test_app.get("/spotify/artist?artist=U2")
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["spid"] == "51Blml2LZPmy7TTiAg47vQ"
    assert response_dict["name"] == "U2"
    assert response_dict["uri"] == "spotify:artist:51Blml2LZPmy7TTiAg47vQ"
    assert response_dict["url"] == "https://open.spotify.com/artist/51Blml2LZPmy7TTiAg47vQ"


def test_get_song(test_app):
    response = test_app.get("/spotify/song?artist=U2&name=Bad")
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["spid"] == "6TQ7XVKcCQcfCEmv0QYYV8"
    assert response_dict["artist"] == "U2"
    assert response_dict["name"] == "Bad - Remastered 2009"
    assert response_dict["tempo"] == 98.7
    assert response_dict["energy"] == 0.681
    assert response_dict["danceability"] == 0.373
    assert response_dict["uri"] == "spotify:track:6TQ7XVKcCQcfCEmv0QYYV8"
    assert response_dict["url"] == "https://open.spotify.com/track/6TQ7XVKcCQcfCEmv0QYYV8"
