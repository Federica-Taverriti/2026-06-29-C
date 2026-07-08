import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._artists = []
        self._bestGroup = []
        self._maxTracks = 0


    def buildGraph(self):
        self._graph.clear()
        self._artists = DAO.getAllArtists()
        self._graph.add_nodes_from(self._artists)

        artistPlaylist = DAO.getArtistPlaylistPairs()
        for artist in self._artists:
            artist.Playlists = set(artistPlaylist.get(artist.ArtistId, set()))

        for i in range (len(self._artists)):
            for j in range (i+1, len(self._artists)):
                a1 = self._artists[i]
                a2 = self._artists[j]
                common = a1.Playlists & a2.Playlists
                if common:
                    peso = len(common)
                    self._graph.add_edge(a1, a2, weight=peso)


    def getArtistMaxDegree(self):
        if len(self._graph.nodes) == 0:
            return None, 0

        maxDegree = -1
        bestArtist = None

        for node, degree in self._graph.degree():
            if degree > maxDegree:
                maxDegree = degree
                bestArtist = node
        return bestArtist, maxDegree

    def getArtistMaxWeightSum(self):
        if len(self._graph.nodes) == 0:
            return None, 0

        maxSum = -1
        bestArtist = None

        for node in self._graph.nodes:
            weightSum = sum(self._graph[node][neighbor]['weight']
                            for neighbor in self._graph.neighbors(node))

            if weightSum > maxSum:
                maxSum = weightSum
                bestArtist = node
        return bestArtist, maxSum

    def getTop10Edges(self):
        if len(self._graph.edges) == 0:
            return []

        edgesPesati = [(u, v , self._graph[u][v]['weight'])
                       for u, v in self._graph.edges]

        edgesSorted = sorted(edgesPesati, key=lambda x:(-x[2], x[0].Name, x[1].Name))
        return edgesSorted[:10]


    def getBestGroup(self, startingArtist, N):
        self._bestGroup = []
        self._maxTracks = 0
        parziale = [startingArtist]

        self._ricorsione(parziale, N)
        return self._bestGroup, self._maxTracks



    def _ricorsione(self, parziale, N):
        if len(parziale) == N:
            total = self._getTotalTracks(parziale)
            if total > self._maxTracks:
                self._maxTracks = total
                self._bestGroup = copy.deepcopy(parziale)
            return

        for n in self._graph.nodes:
            if n in parziale: #se già presente skip
                continue

            #verifico se n è adiacente ad almeno un elemento già presente in parziale
            adjacent = any(self._graph.has_edge(n, present) for present in parziale)
            if not adjacent:
                continue

            #verifico che non sia collegato a nessun elemento con un arco di peso 1
            blocked = any(self._graph.has_edge(n, present) and self._graph[n][present]['weight'] == 1
                          for present in parziale)
            if blocked:
                continue

            parziale.append(n)
            self._ricorsione(parziale, N)
            parziale.pop()


    def getNumNodi(self):
        return len(self._graph.nodes)

    def getNumEdges(self):
        return len(self._graph.edges)

    def _getTotalTracks(self, artists):
        return sum(len(a.Tracks) for a in artists)

    def getAllArtists(self):
        return self._graph.nodes

    def getNumAlbumsForArtist(self, artistId):
        return DAO.getNumAlbumsForArtist(artistId)

