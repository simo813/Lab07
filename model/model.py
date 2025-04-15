from database.meteo_dao import MeteoDao


class Model:
    def __init__(self):
        self.meseMO = None
        self.meteo_dao = MeteoDao()
        self.costo = -100
        self.giorniNelleCitta = {
            "Milano": 0,
            "Torino": 0,
            "Genova": 0
        }
        self.rCalcolaCosto = []
        self.contaGiorni = 1

    def handle_umidita_mediaMO(self):
        risultati = self.meteo_dao.get_umidita_media(self.meseMO)
        return risultati




    def calcolaCosto(self):
        self.giorniNelleCitta = {
            "Milano": 0,
            "Torino": 0,
            "Genova": 0
        }
        self.rCalcolaCosto = []
        self.costo = -100  # lo riporto a zero dopo ogni chiamata
        self.contaGiorni = 1
        self.scegliNuovaCitta(self.contaGiorni, 3,"Fittizia")
        return self.costo, self.rCalcolaCosto



    def scegliNuovaCitta(self, giorno, giornoControllo, cittaCorrente):

        """
        Per evitare due casi che renderebbero non ottimale il risultato esamino finestre da 3 giorni ma
        nel caso la città corrente sia ancora la migliore scelta incremento di uno il giorno in esame, altrimenti incremento di 3 il giorno in esame.
        Se non facessi così avrei casi in cui scelgo una città perché in quel determinato giorno era la più conveniente
        ma poi bisogna rimanerci per altri 2 giorni in cui magari l'umidità si alza drasticamente rendendo la scelta non ottimale;
        il secondo caso che evito con questa soluzione è quello in cui potrebbe essere conveniente stare in una città un totale di giorni compreso
        tra 3 e 6, se infatti scalassi sempre di 3 giorni questa opzione non verrebbe considerata
        """

        if giorno >= 14:  # qui inseriamo la condizione terminale

            print(self.costo)

        else:

            #chiedo al dao le situazioni di una finestra di giorni che va dalla variabile "giorno" alla variabile "giornoControllo" che parte dal giorno indicato del mese scelto (da creare)
            #questo con lo scopo di poter gestire la lunghezza della finestra temporale a seconda delle necessita

            situazioni = self.meteo_dao.getSituazioniMeseBloccoGiorni(self.meseMO, giorno, giornoControllo) #estremi dei giorni compresi?ATTENZIONE

            #creao un dizionario in cui inserisco solo le città che hanno ancora giorni liberi
            print(f"stiamo esainando il range {giorno}-{giornoControllo}")

            costiBlocco = {}

            for citta in self.giorniNelleCitta:
                if self.giorniNelleCitta[citta] < 6:
                    costiBlocco[citta] = 0

            #calcolo i costi per ogn città con i 100 aggiuntivi se si cambia

            for situazione in situazioni:
                print(situazione)
                #controllo che la città in esame sia uguale a quella passata come parametro

                if situazione.localita == cittaCorrente:

                    #aggiorno il dizionario con il valore di umidità
                    if situazione.localita in costiBlocco:

                        costiBlocco[situazione.localita] += situazione.umidita
                    else:

                        continue
                else:

                    """
                    In questo caso devo cambiare località e di conseguenza devo verificare che i giorni passati nella località siano minori o uguali a 3,
                    infatti scelta una città bisogna stare almeno 3 giorni di fila non però se è stata riscelta per una seconda volta
                    """
                    if situazione.localita in costiBlocco and costiBlocco[situazione.localita] == 0: #devo introdurre questo ciclo altrimenti inserisci 100 ogni volta
                        costiBlocco[situazione.localita] += (situazione.umidita + 100)
                    else:
                        if situazione.localita in costiBlocco:
                            costiBlocco[situazione.localita] += situazione.umidita

            # determino il costo più basso e la città con il costo più basso per il giorno indicato e le salvo in costoSceltaMigliore e cittaScelta

            cittaScelta = min(costiBlocco, key=costiBlocco.get) #chiave con valore minimo
            costoPrec = self.costo

            if cittaScelta != cittaCorrente:
                self.costo += 100
                for situazione in situazioni:
                    if situazione.localita == cittaScelta:
                        if self.giorniNelleCitta[cittaScelta] == 0:
                            self.rCalcolaCosto.append(situazione)
                            self.costo += situazione.umidita
                        else:
                            if situazione.data.day == giorno:
                                self.rCalcolaCosto.append(situazione)
                                self.costo += situazione.umidita
            else:
                for situazione in situazioni:
                    if situazione.localita == cittaScelta and situazione.data.day == giorno:
                        self.rCalcolaCosto.append(situazione)
                        self.costo += situazione.umidita


            print(f"la citta migliore è {cittaScelta}, e il costo è {self.costo-costoPrec}")
            print(f"il costo per ora è {self.costo}")

            if cittaScelta == cittaCorrente or self.giorniNelleCitta[cittaScelta] >= 3:

                # inserisco i giorni aggiuntivi sulla citta scelta

                self.giorniNelleCitta[cittaScelta] += 1
                print(f"i giorni nella cittò scelta sono {self.giorniNelleCitta[cittaScelta]}")

                # richiamo la funzione con un giorno in più se cittaScelta == cittaCorrente e aggiorno il contatore esterno di giorni

                self.contaGiorni += 1


                # si aggiorna solo giorno così in mySQL il range è per es da 5 a 5 e seleziona solo una data

                giornoControllo = self.contaGiorni + 2
                print(self.contaGiorni)

                self.scegliNuovaCitta(self.contaGiorni, giornoControllo, cittaScelta)

            elif (giornoControllo + 3) > 15 or (giorno + 3) >15:

                # inserisco i giorni aggiuntivi sulla citta scelta

                self.giorniNelleCitta[cittaScelta] += 1
                print(f"i giorni nella cittò scelta sono {self.giorniNelleCitta[cittaScelta]}")

                # richiamo la funzione con un giorno in più se cittaScelta == cittaCorrente e aggiorno il contatore esterno di giorni

                self.contaGiorni += 1

                # si aggiorna solo giorno così in mySQL il range è per es da 5 a 5 e seleziona solo una data
                print(self.contaGiorni)

                self.scegliNuovaCitta( self.contaGiorni, 15, cittaScelta)


            else:

                # richiamo la funzione con 3 giorni in più se cambio città e aggiorno il contatore esterno di giorni

                self.giorniNelleCitta[cittaScelta] += 3
                print(f"i giorni nella cittò scelta sono {self.giorniNelleCitta[cittaScelta]}")

                self.contaGiorni += 3
                giornoControllo = self.contaGiorni + 3

                print(self.contaGiorni)

                self.scegliNuovaCitta(self.contaGiorni, giornoControllo, cittaScelta)


