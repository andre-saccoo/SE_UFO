import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self.G=nx.Graph()
        self.lista_stati=[]
        self.lista_connessioni=[]
        self.mappa = {} #Mappiamo id->oggetto stato

    @staticmethod
    def load_anni():
        return DAO.get_anno()

    @staticmethod
    def load_forme():
        return DAO.get_forme()

    def built_graph(self, anno, forma):
        self.G.clear()
        self.lista_stati=DAO.get_state(anno, forma) #lista di oggetti stato

        for elemento in self.lista_stati:
            self.mappa[elemento.id]=elemento
            print(elemento.name, elemento.id,elemento.num_avvistamenti)
        self.lista_connessioni=DAO.get_vicini() #lista di oggetto connessione dove si ha id1, id2

        #mettere tutti i nodi
        for elemento in self.lista_stati:
            self.G.add_node(elemento)
            print(elemento.num_avvistamenti)

        #mettere i ponti
        for elemento in self.lista_connessioni:
            oggetto1=self.mappa[elemento.state1]
            oggetto2=self.mappa[elemento.state2]
            somma=int(oggetto1.num_avvistamenti)+(oggetto2.num_avvistamenti)
            self.G.add_edge(self.mappa[elemento.state1], self.mappa[elemento.state2], weight=somma)
        return self.G

from database.dao import DAO
import networkx as nx
class Model:
    def __init__(self):
        self.G=nx.Graph()

    def get_anno(self):
        return DAO.anno()

    def get_forma(self):
        return DAO.forma()

    def crea_grafo(self, forma ,anno):
        self.G.clear()
        lista_nodi=DAO.lista_tutti_nodi()    #lista tutti gli oggetti stato con avvistamenti a 0
        dazionario_stati = {}                  #dizionario che mappa tutti i nodi
        for nodo in lista_nodi:
            dazionario_stati[nodo.id_stato]=nodo
        lista_nodi_anno = [] #per pulire in caso di cambio
        lista_nodi_anno=DAO.lista_nodi_anno(forma, anno) #lista di tuple con id_stato, num avvistamenti
        for elemento in lista_nodi_anno:
            dazionario_stati [elemento[0]].num_avvistamenti=elemento[1]
        self.G.add_nodes_from(lista_nodi)
        collegamenti = DAO.lista_vicini()  # confinanti
        for elemento in collegamenti:
            stato1=dazionario_stati[elemento[0]]
            stato2 = dazionario_stati[elemento[1]]
            try:
                weight=int(stato1.num_avvistamenti)+int(stato2.num_avvistamenti)
            except:
                print("errore")
            if stato1!=stato2:
                self.G.add_edge(stato1,stato2,weight=weight)
        return self.G