from database.DB_connect import DBConnect
from model.artist import Artist


class DAO():

    @staticmethod
    def getAllArtists():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT a.*
                    FROM Artist a, Album al, Track t 
                    WHERE a.ArtistId = al.ArtistId 
                    AND al.AlbumId = t.AlbumId 
                    ORDER BY a.Name"""

        cursor.execute(query)

        for row in cursor:
            results.append(Artist(**row))

        cursor.close()
        conn.close()

        for artist in results:
            artist.Tracks = DAO.getTracksForArtist(artist.ArtistId)

        return results


    @staticmethod
    def getTracksForArtist(artistId):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT t.TrackId 
                    FROM Album al, Track t 
                    WHERE  al.AlbumId = t.AlbumId 
                    AND al.ArtistId = %s"""

        cursor.execute(query, (artistId,))

        for row in cursor:
            results.append(row["TrackId"])

        cursor.close()
        conn.close()

        return results


    @staticmethod
    def getArtistPlaylistPairs():
        conn = DBConnect.get_connection()

        results = {} #dizionario che ha come chiave l'id artista e come valore id playlist

        cursor = conn.cursor(dictionary=True)
        query = """SELECT distinct a.ArtistId, pt.PlaylistId 
                    FROM Artist a, Album al, Track t, PlaylistTrack pt 
                    WHERE a.ArtistId = al.ArtistId 
                    AND al.AlbumId = t.AlbumId 
                    AND t.TrackId = pt.TrackId """

        cursor.execute(query)

        for row in cursor:
            artistId = row["ArtistId"]
            playlistId = row["PlaylistId"]
            if artistId not in results:
                results[artistId] = []
            results[artistId].append(playlistId)

        cursor.close()
        conn.close()

        return results

    @staticmethod
    def getNumAlbumsForArtist(artistId):
        conn = DBConnect.get_connection()

        cursor = conn.cursor(dictionary=True)
        query = """SELECT count(distinct al.AlbumId) as NumAlbums
                        FROM Album al
                        WHERE al.ArtistId = %s"""

        cursor.execute(query, (artistId,))

        row = cursor.fetchone()

        cursor.close()
        conn.close()

        return row["NumAlbums"] if row else 0
