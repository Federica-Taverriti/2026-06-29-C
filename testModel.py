from model.model import Model

mymodel = Model()

mymodel.buildGraph()
nNodi = mymodel.getNumNodi()
nArchi = mymodel.getNumEdges()
print(f"{nNodi} nodi e {nArchi} archi")

bestArtist, maxDegree = mymodel.getArtistMaxDegree()
print(f"Artista con grado maggiore: {bestArtist} (grado: {maxDegree})")

artist, maxSum = mymodel.getArtistMaxWeightSum()
print(f"Artista somma pesi incidenti massima: {artist} (somma: {maxSum})")

topEdges = mymodel.getTop10Edges()
print("Top 10 archi:")
for i, (a, b, peso) in enumerate(topEdges, 1):
    print(f"{i}. {a} -- {b}  (peso: {peso}) ")