#%%
from ESTRACTER import Estracter_data
estracter = Estracter_data()
#%%
FINAL_DF = estracter.EXTRACT_ALL_DATA_FROM_EXCEL()

FINAL_DF.to_excel('DATOS_EXTRAIDOS_COES.xlsx',sheet_name= 'POTENCIAS_CONTRATADAS',index = False)























# %%
