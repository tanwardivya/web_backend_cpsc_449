from typing import Any, List, Dict
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport


# Select your transport with a defined url endpoint
transport = AIOHTTPTransport(url="http://localhost:4000/graphql")

# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=True)

#Question 1 Albums by the artist “Red Hot Chili Peppers.”
def get_albums(artist_name: str) -> Dict[str, Any]:
    """List of albums by name of the artist

    Args:
        artist_name (str): Name of artist

    Returns:
        Dict[str, Any]: A dictionary object
    """
    # Provide a GraphQL query
    query = gql(
        """
            query{
                artist(where: {name:"arg"}){
                  artistId
                  albums {
                    title
                  }
                } 
              }
       """.replace('arg', artist_name)
    )
    # Execute the query on the transport
    result = client.execute(query)
    return result

def get_genres(artist_name: str) -> Dict[str, Any]:
    """List of genres by name of the artist

    Args:
        artist_name (str): Name of artist

    Returns:
        Dict[str, Any]: Dictionary object
    """
    # Provide a GraphQL query
    query = gql(
        """
          query{

            artist(where: {name:"arg"}){
              artistId
              albums {
                tracks{
                  genreId
                  genre{
                    name
                  }
                }
              }
            } 
          }
       """.replace('arg', artist_name)
    )
    # Execute the query on the transport
    result = client.execute(query)
    return result

def get_tracks(playlist_name: str) -> Dict[str, Any]:
    """Names of tracks on the playlist name and their associated artists and albums.

    Args:
        playlist_name (str): Name of playlist

    Returns:
        Dict[str, Any]: Dictionary object
    """
    # Provide a GraphQL query
    query = gql(
        """
        query{
          playlist(where :{name: "arg"}){
            playlistId
              tracks{
                name
                album{
                  title
                  artist{
                    name
                  }
                }
              }
            }
        }
       """.replace('arg', playlist_name)
    )
    # Execute the query on the transport
    result = client.execute(query)
    return result


if __name__ == '__main__':
    albums = get_albums(artist_name='Red Hot Chili Peppers')
    print(albums)
    genres = get_genres(artist_name='U2')
    print(genres)

    tracks = get_tracks(playlist_name='Grunge')
    print(tracks)
