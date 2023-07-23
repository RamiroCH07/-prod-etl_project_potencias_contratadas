#%%
from DOWNLOADER import Downloader_files

#%%
obj_downloader = Downloader_files()
had_update = obj_downloader.DOWNLOADING_LAST_FILE()
print(had_update)