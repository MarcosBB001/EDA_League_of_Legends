import pandas as pd

def load_datasets():
    df_1 = 0
    return df_1


def parse_patches(lista_parches):
    """
    Convierte las strings de los parches 15.24.734.7485 en floats (15.24)
    Tiene en cuenta casos especiales como 16.1.737.4870 a 16.01 (en vez de 16.10)
    """
    parts = lista_parches.str.extract(r"^(\d+)\.(\d+)")
    return (parts[0] + "." + parts[1].str.zfill(2)).astype(float)

