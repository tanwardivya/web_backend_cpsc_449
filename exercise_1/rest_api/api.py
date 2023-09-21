from typing import Any, List, Dict
import requests

API_QUERY_ENDPOINT = "http://localhost:8000/api/transaction"
HEADERS = {
    'accept' : 'application/json',
    'Content-Type' : 'application/json'
}

#Question 1 Albums by the artist “Red Hot Chili Peppers.”
def get_albums(artist_name: str) -> List[Dict]:
    """List of albums by name of the artist

    Args:
        artist_name (str): Name of artist

    Returns:
        List[str]: List of album
    """
    query = f"""SELECT al.title FROM albums al where al.artistid = (SELECT artistid FROM artists where name = '{artist_name}')"""
    data = {
        "transaction" :
        [
            {"query" : query}
        ]
    }
    response = requests.post(headers=HEADERS, url=API_QUERY_ENDPOINT, json = data)
    if response.status_code!=200:
        print(response.json())
        return []
    result = response.json()
    query_result = result["data"][0]
    return query_result

# Question 2 Genres associated with the artist "U2"
def get_genres(artist_name: str) -> List[Dict]:
    """Genres associated with the artist name

    Args:
        artist_name (str): Name of artist

    Returns:
        List[Dict]: List of Genres
    """
    query = f"""SELECT ge.name FROM genres ge where ge.genreid in 
                ( SELECT te.genreid FROM tracks te where te.albumid in 
                    (SELECT al.albumid FROM albums al where al.artistid = 
	                    (SELECT at.artistid FROM artists at  where at.name = '{artist_name}'
	                    )
                    ) 
                )
             """
    
    data = {
        "transaction":
        [
            {"query": query}
        ]
    }
    response = requests.post(headers = HEADERS,url = API_QUERY_ENDPOINT, json = data)
    if response.status_code!= 200:
        print(response.json())
        return[]
    result = response.json()
    query_result = result["data"][0]
    return query_result
        

#Question 3 Names of tracks on the playlist “Grunge” and their associated artists and albums.
def get_tracks(playlist_name:str)-> List:
    """Names of tracks on the playlist name and their associated artists and albums.

    Args:
        
        playlist_name (str): Name of tracks

    Returns:
        List[List]: returns the list of artists and albums associated with playlist 
    """
    query = f"""SELECT s2.name as track_name , s2.title as album_title, ar.name as artist_name FROM artists ar, 
    (SELECT s1.name, al.title, al.artistid FROM albums al, 
    (SELECT tr.name, tr.albumid FROM tracks tr where tr.trackid in 
    (SELECT pt.trackid FROM playlist_track pt where pt.playlistid = 
    (SELECT pl.playlistid FROM playlists pl where name ='{playlist_name}'))) as s1 where al.albumid in 
    (s1.albumid)) as s2 where ar.artistid in (s2.artistid)
"""
    data = {
        "transaction":
        [
            {"query": query}
        ]
    }

    response = requests.post(headers = HEADERS, url = API_QUERY_ENDPOINT, json = data)
    if response.status_code!= 200:
        print(response.json())
        return[]
    result = response.json()
    query_result = result["data"][0]
    return query_result

if __name__ == '__main__':
    albums = get_albums(artist_name='Red Hot Chili Peppers')
    print(albums)

    genres = get_genres(artist_name = 'U2')
    print(genres)

    tracks = get_tracks(playlist_name='Grunge')
    print(tracks)

    