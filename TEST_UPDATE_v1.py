from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import glob
import os.path
import shutil
import os
from bs4 import BeautifulSoup
import re

## PREPARACIÓN PARA NAVEGAR CON GOOGLE CHROME DE MANERA AUTOMATICA
URL = 'https://www.coes.org.pe/Portal/mercadomayorista/liquidaciones' 
option = webdriver.ChromeOptions()
option.add_argument("--incognito")
# OBJETO Driver
driver = webdriver.Chrome(options=option)
## ACCEDIENDO A LA PÁGINA EN CUESTIÓN CON Goolge Chrome
driver.maximize_window()
driver.get(URL)

##IDENTIFICANDO EL XPATH DEL BOTON "Mercado de Corto Plazo"
xpath = '//*[@id="Mercado Mayorista/Liquidaciones del MME/01 Mercado de Corto Plazo/"]'
## INSTANCIAMOS EL BOTON HACIENDO USO DEL PATH 
button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((
            By.XPATH, xpath)))
## HACEMOS CLICK AL BOTON 
button.click()
sleep(4)

#-> ESTO NOS HA LLEVADO A UNA NUEVA PÁGINA, AHORA LA META ES HACER CLICK AL BOTON LLAMADO "Potencias Contratadas"
#   
xpath = '//*[@id="Mercado Mayorista/Liquidaciones del MME/01 Mercado de Corto Plazo/Potencias Contratadas/"]'
## INSTANCIAMOS EL BOTON HACIENDO USO DEL PATH 
button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((
            By.XPATH, xpath)))
## HACEMOS CLICK AL BOTON 
button.click()
sleep(4)


## RECUPERAMOS EL HTML DE LA SECCIÓN Y UBICAMOS LA ULTIMA CARPETA
body = driver.execute_script("return document.body")
source = body.get_attribute('innerHTML')
soup = BeautifulSoup(source,'html.parser')
ullist = soup.find('ul',class_='infolist list-unstyled')
years = ullist.get_text()
years = years.split()
last_year = years[0]

## ACCEDEMOS AL AÑO MAYOR 

## IDENTIFICAMOS EL XPATH DEL BOTON CON EL AÑO MAYOR

xpath = (r'//a[@id='
                     r'"Mercado Mayorista/'
                     r'Liquidaciones del MME/'
                     r'01 Mercado de Corto Plazo/'
                     r'Potencias Contratadas/'
                     fr'{last_year}/"]')

#xpath = '/html/body/div[3]/div[2]/div/div/div[1]/div[3]/div[3]/ul/li[2]/a'
print(xpath)
## INSTANCIAMOS EL BOTON
button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((
            By.XPATH, xpath)))

## HACER CLICK AL BOTON
button.click()
sleep(5)

## IDENTIFICAMOS EL NOMBRE DEL MES MAYOR
body = driver.execute_script("return document.body")
source = body.get_attribute('innerHTML')
soup = BeautifulSoup(source,'html.parser')
ullist = soup.find('ul',class_='infolist list-unstyled')
months = ullist.get_text()
months = months.split()
last_month = months[0]

# MECANISMO PARA ACTUALIZAR
## GENERACIÓN DE UN CÓDIGO DE FECHA PARA COMPARACIÓN CON EL DE LA ÚLTIMA ACTUALIZACIÓN
generated_code_now = last_month+'_'+last_year 
###
f = open('LAST_DOWNLOADER_FILE.txt','r')
last_update_code = f.read()
f.close()
print(generated_code_now)
print(last_update_code)

had_update = generated_code_now != last_update_code

## IDENTIFICAMOS EL XPATH DEL BOTON CON EL MAYOR MES
if had_update:
    print("Se ha identificado una nueva actualización, recuperando el arhivo excel")
    xpath= (r'//a[@id='
                            r'"Mercado Mayorista/'
                            r'Liquidaciones del MME/'
                            r'01 Mercado de Corto Plazo/'
                            r'Potencias Contratadas/'
                            fr'{last_year}/'
                            fr'{last_month}/'
                            r'"]')
    ## INSTANCIAMOS EL BOTON
    button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((
                By.XPATH, xpath)))

    ## HACER CLICK AL BOTON
    button.click()
    sleep(5)

    ### IDENTIFICANDO LA ULTIMA VERSIÓN DEL ARCHIVO
    body = driver.execute_script("return document.body")
    source = body.get_attribute('innerHTML')
    soup = BeautifulSoup(source,'html.parser')
            
    ##Identificar la etiqueta que contiene los archivos a descargar
    main_table = soup.find('table',id='tbDocumentLibrary').find('tbody')
    trs = main_table.find_all('tr')
    names_files = []
    num_version = []

    for tr in trs:
        name_file = tr.find_all('td')[2].get_text()
        names_files.append(name_file)

    for name in names_files:
        li = re.findall('[0-9]+',name)
        try:
            num = li[1]
            num_version.append(int(num))
        except:
            num_version.append(0) 

    max_version = max(num_version)
    pos_max_version = num_version.index(max_version)
    last_file_version = names_files[pos_max_version]

    ## DESCARGAMOS EL ARCHIVO EN CUESTION
    ## IDENTIFICAMOS PATH DE LA SECCIÓN DE DESCARGA

    xpath= (r'//*[@id='
                            r'"Mercado Mayorista/'
                            r'Liquidaciones del MME/'
                            r'01 Mercado de Corto Plazo/'
                            r'Potencias Contratadas/'
                            fr'{last_year}/'
                            fr'{last_month}/'
                            fr'{last_file_version}'
                            r'"]')

    ## INSTANCIAMOS EL BOTON
    button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((
                By.XPATH, xpath)))

    ## HACER CLICK AL BOTON de DESCARGA
    button.click()
    sleep(15)

    ### IDENTIFICAR Y MOVER EL ARCHIVO DESCARGADO
    #--------------------------------------------------------
    #iDENTIFICANDO NOMBRE DE ARCHIVO
    folder_path = r'C:\Users\rchavez\Downloads'#r'C:\Users\Toshiba\Downloads'
    file_type = r'\*xlsx'
    files = glob.glob(folder_path + file_type)
    max_file = max(files, key=os.path.getctime)
    # Movemos el archivo descargado a una carpeta dentro del proyecto
    source = f'{max_file}'
    ## Nuevo nombre de archivo
    destination = f"EXCEL_FILES/{generated_code_now}.xlsx"
    shutil.move(source,destination)
    with open('LAST_DOWNLOADER_FILE.txt','w') as f:
        f.write(generated_code_now)


## NO SE HA DETECTADO UNA ACTUALIZACON        
else:
    print("No hubo actualización")


driver.close()


