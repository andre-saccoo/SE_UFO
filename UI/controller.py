import flet as ft

class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

        self.anno_selezionato=None
        self.forma_selezionata=None

    def populate_dd(self):
        """ Metodo per popolare i dropdown """
        self._view.dd_year.options.clear()
        self._view.dd_shape.options.clear()

        lista_anni=self._model.load_anni()
        lista_forme = self._model.load_forme()

        for elemento in lista_anni:
            self._view.dd_year.options.append(ft.dropdown.Option(elemento))

        for elemento in lista_forme:
            self._view.dd_shape.options.append(ft.dropdown.Option(elemento))

        self._view.page.update()

    def on_change_anno(self,e):
        self.anno_selezionato=e.control.value

    def on_change_forma(self,e):
        self.forma_selezionata=e.control.value

    def handle_graph(self, e):
        """ Handler per gestire creazione del grafo """
        if self.anno_selezionato is None or self.forma_selezionata is None:
            self._view.show_alert("riempire le dropdown")
            return
        else:
            grafo=self._model.built_graph(self.anno_selezionato,self.forma_selezionata)
            self._view.lista_visualizzazione_1.controls.clear()

            for elemento in grafo.nodes:
                vicini=grafo.neighbors(elemento)
                somma=0
                for elemento in vicini:
                    somma+=elemento.num_avvistamenti
                #somma_pesi_su_archi=grafo.degree(elemento,weight='weight')
                self._view.lista_visualizzazione_1.controls.append(ft.Text(f"{elemento.name} {elemento.id}, somma pesi su archi = {somma} "))
            self._view.page.update()

    def handle_path(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        # TODO
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
