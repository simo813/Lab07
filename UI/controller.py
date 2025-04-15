import flet as ft

from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._meseCO = 0

    def handle_umidita_mediaCO(self, e):
        self._view.lst_result.controls = []
        self._view.update_page()
        meseScelto = self._view.dd_mese.value
        self._model.meseMO = meseScelto
        risultati = self._model.handle_umidita_mediaMO()
        titolo = f"Umidità media nelle città presenti nel databse nel mese scelto"
        self._view.lst_result.controls.append(ft.Text(value=f"{titolo}", color="black",
                                                      text_align=ft.TextAlign.LEFT, width=300, weight=ft.FontWeight.BOLD))
        stampa = ""
        for i in risultati:
            stampa += "Località: " + str(i[0]) + "|  Umidità media: " +  str(i[1]) + "\n"
        self._view.lst_result.controls.append(ft.Text(value=f"{stampa}", color="black",
                                                      text_align=ft.TextAlign.LEFT, width=300))
        self._view.update_page()


    def handle_sequenza(self, e):
        self._view.lst_result.controls = []
        self._view.update_page()
        meseScelto = self._view.dd_mese.value
        self._model.meseMO = meseScelto
        costoTotale, listaSituazioni = self._model.calcolaCosto()
        titolo = f"Costo nel mese scelto"
        self._view.lst_result.controls.append(ft.Text(value=f"{titolo}", color="black",
                                                      text_align=ft.TextAlign.LEFT, width=300,
                                                      weight=ft.FontWeight.BOLD))
        stampa = ""
        for i in listaSituazioni:
            stampa += i.__str__() + "\n"

        stampa += f"Costo totale: {costoTotale}\n"
        self._view.lst_result.controls.append(ft.Text(value=f"{stampa}", color="black",
                                                      text_align=ft.TextAlign.LEFT, width=300))

        self._view.update_page()

    def read_mese(self, e):
        self._meseCO = int(e.control.value)

