from skyfield.api import Star, load
from skyfield.data import hipparcos

def load_stars(max_magnitude=6):
    with load.open(hipparcos.URL) as f:
        df = hipparcos.load_dataframe(f)
    return df[df['magnitude'] <= max_magnitude]
    



