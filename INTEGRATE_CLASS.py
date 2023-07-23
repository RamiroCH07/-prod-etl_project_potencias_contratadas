from DOWNLOADER import Downloader_files
from ESTRACTER import Estracter_data
import os
import pandas as pd

class INTEGRATE_CLASS:
    def __init__(self):
        self.obj_downloader = Downloader_files()
        
    def TEST_GET_EXCEL_WITH_ESTRACT_DATA(self):
        file_names = os.listdir('EXCEL_FILES')
        #AGREGAMOS EL PRIMERO
        print("EXTRAYENDO DATOS DE:",file_names[0])
        obj_estracter = Estracter_data(file_names[0])
        #EXTRAEMOS Y LO GUARDAMOS EN UN EXCEL
        df = obj_estracter.EXTRACT_ALL_DATA_FROM_EXCEL()
        df.to_excel('DATOS_EXTRAIDOS_POTENCIAS_CONTRATADAS.xlsx',sheet_name= file_names[0],index = False)
        for file_name in file_names[1:]:
            print("EXTRAYENDO DATOS DE:",file_name)
            obj_estracter = Estracter_data(file_name)
            df = obj_estracter.EXTRACT_ALL_DATA_FROM_EXCEL()
            with pd.ExcelWriter('DATOS_EXTRAIDOS_POTENCIAS_CONTRATADAS.xlsx',mode = 'a') as writer:
                df.to_excel(writer,sheet_name=file_name,index = False)

    def PRINT_HELLO(self):
        print('HELLO')


    def START_ETL_PROCCESS_JOB(self):
        # ---------------------------- DESCARGA DATOS ---------------------------------------------------
        had_update = self.obj_downloader.DOWNLOADING_LAST_FILE()
        # HUBO ACTUALIZACIÓN ?
        if had_update:
            # SI HUBO ACTUALIZACION DESCARGAMOS ARCHIVO Y EXTREMOS LOS DATOS
            # ------------------- EXTRACCION DE DATOS ----------------------------------------
            obj_estracter = Estracter_data()
            df = obj_estracter.EXTRACT_ALL_DATA_FROM_EXCEL()
            # ------- ELIMINAMOS EL ARCHIVO "EXCEL_FILE_DOWNLOADED.xlsx" --------------------------------
            if os.path.isfile('EXCEL_FILE_DOWNLOADED.xlsx'):
                os.remove('EXCEL_FILE_DOWNLOADED.xlsx')
            # ------------ PRUEBA DE VIZUALIZACIÓN ------------------------------------------------------
            df.to_excel('DATOS_EXTRAIDOS_COES.xlsx',sheet_name= 'POTENCIAS_CONTRATADAS',index = False)
            #--------------------------------------------------------------------------------------------
            # -------------------------- PREPROCESAMIENTO Y LIMPIEZA DE DATOS ---------------------------
            # -------------------------------------------------------------------------------------------
            # ---------------------- CARGA DE DATOS A UNA INSTANCIA DE BASE DE DATOS --------------------
            # -------------------------------------------------------------------------------------------
        else:
            print("NO HUBO ACTUALIZACIÓN RECIENTE")
        


            
