from database.DB_connect import DBConnect
from model.situazione import Situazione


class MeteoDao():

    @staticmethod
    def get_all_situazioni():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s.Localita, s.Data, s.Umidita
                        FROM situazione s 
                        ORDER BY s.Data ASC"""
            cursor.execute(query)
            for row in cursor:
                result.append(Situazione(row["Localita"],
                                         row["Data"],
                                         row["Umidita"]))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_umidita_media(mese):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select s.Localita , avg(s.Umidita) as a
                        from meteo.situazione s 
                        where month(s.`Data`) = COALESCE(%s, month(s.`Data`))
                        group by s.Localita """
            cursor.execute(query, (mese, ))
            for row in cursor:
                localita = row["Localita"]
                umiditaMedia = row["a"]
                risultato = [localita, umiditaMedia]
                result.append(risultato)
            cursor.close()
            cnx.close()
            print(result)
        return result

    @staticmethod
    def getSituazioniMeseBloccoGiorni(giorno, giornoControllo, cittaCorrente):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """ select s.Localita , s.Data, s.Umidita 
                        from meteo.situazione s 
                        where month(s.`Data`) = COALESCE(%s, month(s.`Data`))
                                and day(s.`Data`) >= COALESCE(%s, day(s.`Data`))
                                and day(s.`Data`) <= COALESCE(%s, day(s.`Data`))
                        group by s.Localita, s.Data, s.Umidita """
            cursor.execute(query, (giorno, giornoControllo, cittaCorrente))
            for row in cursor:
                result.append(Situazione(row["Localita"],
                                         row["Data"],
                                         row["Umidita"]))
            cursor.close()
            cnx.close()
        return result


