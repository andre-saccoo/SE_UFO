from database.DB_connect import DBConnect
from model.connessione import Connessione
from model.state import State

class DAO:
    @staticmethod
    def get_anno():
        conn = DBConnect.get_connection()
        if conn is None:
            print("errore di connessione anni database")
            return None
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT YEAR(s_datetime) as year FROM sighting """
        try:
            cursor.execute(query)
        except Exception as e:
            print("errore nell'esecuzione della query 'anni': ",e)
        for row in cursor:
            result.append(row["year"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_forme():
        conn = DBConnect.get_connection()
        if conn is None:
            print("errore di connessione forme database")
            return None
        result = []
        cursor = conn.cursor(dictionary=True)
        query = " SELECT DISTINCT shape FROM sighting "
        try:
            cursor.execute(query)
        except Exception as e:
            print("errore nell'esecuzione della query 'forme': ", e)
        for row in cursor:
            result.append(row["shape"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_state(anno, forma):
        conn = DBConnect.get_connection()
        if conn is None:
            print("errore di connessione state database")
            return None
        result = []
        cursor = conn.cursor(dictionary=True)
        query = " SELECT s.name,s.id, (SELECT count(id) FROM sighting  WHERE state=s.id AND YEAR(s_datetime) = %s  AND shape=%s) as Num_avvistamenti FROM state s "
        try:
            cursor.execute(query,(anno, forma))
        except Exception as e:
            print("errore nell'esecuzione della query 'stati': ", e)
        for row in cursor:
            stato=State(row["name"], row["id"], row["Num_avvistamenti"])
            print(stato.num_avvistamenti)
            result.append(stato)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_vicini():
        conn = DBConnect.get_connection()
        if conn is None:
            print("errore di connessione vicini database")
            return None
        result = []
        cursor = conn.cursor(dictionary=True)
        query = " SELECT state1,state2  FROM neighbor "
        try:
            cursor.execute(query)
        except Exception as e:
            print("errore nell'esecuzione della query 'connessione': ", e)
        for row in cursor:
            connessione =Connessione(row["state1"],row["state2"])
            result.append(connessione)
        cursor.close()
        conn.close()
        return result

from database.DB_connect import DBConnect
from model.stato import Stato
class DAO:
    #lista di anni per la dd
    @staticmethod
    def anno():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT YEAR(s_datetime) as Anno FROM sighting  """
        cursor.execute(query)
        for row in cursor:
            result.append(row["Anno"])
        cursor.close()
        conn.close()
        return result

    #lista forme per la dd
    @staticmethod
    def forma():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT shape as forma from sighting s   """
        cursor.execute(query)
        for row in cursor:
            result.append(row["forma"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def lista_tutti_nodi():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT id , name from state   """
        cursor.execute(query)
        for row in cursor:
            result.append(Stato(row["id"], row["name"], 0))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def lista_nodi_anno(forma, anno):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT s1.id as id_stato, count(s1.id) as num_avvistamenti from state s1 ,sighting s2
                    where s1.id=s2.state and s2.shape=%s and YEAR(s2.s_datetime )=%s
                    group by s1.id"""
        cursor.execute(query,(forma, anno))
        for row in cursor:
            result.append((row["id_stato"] , row["num_avvistamenti"])) #torna una tupla con id e num di avvistamenti
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def lista_vicini():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT state1, state2 from neighbor """
        cursor.execute(query)
        for row in cursor:
            result.append((row["state1"], row["state2"]))  # torna una tupla con id e num di avvistamenti
        cursor.close()
        conn.close()
        return result
import flet as ft

class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model
        self._anno_selezionato=None
        self._forma_selezionata=None

    #dropdown
    def populate_dd_1(self):
        """ Metodo per popolare i dropdown """
        lista=self._model.get_anno()
        for elemento in lista:
            elemento= str(elemento)
            self._view.dd_year.options.append(ft.dropdown.Option(elemento))
    def on_change_anno(self,e):
        self._anno_selezionato=self._view.dd_year.value

    def populate_dd_2(self):
        """ Metodo per popolare i dropdown """
        lista=self._model.get_forma()
        for elemento in lista:
            elemento= str(elemento)
            self._view.dd_shape.options.append(ft.dropdown.Option(elemento))
    def on_change_forma(self,e):
        self._forma_selezionata=self._view.dd_shape.value

    def handle_graph(self, e):
        """ Handler per gestire creazione del grafo """
        if self._anno_selezionato is None or self._forma_selezionata is None:
            self._view.show_alert("selezionare nelle dd")
        else:
            self._view.lista_visualizzazione_1.controls.clear()
            grafo=self._model.crea_grafo( self._forma_selezionata, self._anno_selezionato)
            for nodo in grafo.nodes:
                somma = grafo.degree(nodo,weight='weight')
                self._view.lista_visualizzazione_1.controls.append(ft.Text(f"{nodo}, somma: {somma}"))

    def handle_path(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        # TODO
