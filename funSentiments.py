import pandas as pd

df = pd.read_csv('input/All-seasons.csv')


def episode(season, episode):
    """
    Get episode of a season

    """
    df_epi= df[(df.Season == f'{season}') & (df.Episode == f'{episode}')]
    return df_epi[["Character", "Line"]]

def get_character(data): 
    """
    Get all character of an episode

"""
    return list(dict.fromkeys(data['Character'].tolist()))