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


def construct_valid_teams(individual_stats):
    """
    Extrae los SummonerMatchID que pertenecen a partidas (MatchId) con 10 SummonerMatchId asociados.
    Comprueba que esas partidas sean válidas (tengan asociados 5 winners y 5 losers).
    """
    # Get the MatchID that have 10 SummonerMatchId associated
    players_per_match = individual_stats.groupby("MatchId").size()
    n_minimum_summoners_mask = individual_stats["MatchId"].map(players_per_match) == 10 
    individual_stats_10 = individual_stats[n_minimum_summoners_mask] 

    # Make sure each MatchID has 5 winners ("Win"==1) and 5 losers ("Win"==0). 
    # Since each MatchID has 10 SummonerIDMatch associated, the sum should equal to 5
    winners_per_match = individual_stats_10.groupby("MatchId")["Win"].sum()
    valid_match_ids = winners_per_match[winners_per_match == 5].index
    individual_stats_10 = individual_stats_10[individual_stats_10["MatchId"].isin(valid_match_ids)]

    return individual_stats_10

    
    