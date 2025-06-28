from skyfield.api import Star, Loader, load
from skyfield.data import hipparcos
load = Loader('nightsky/src')
def load_stars(max_magnitude=6):
    with load.open(hipparcos.URL) as f:
        df = hipparcos.load_dataframe(f)
    return df[df['magnitude'] <= max_magnitude]

def observe_stars():
    planets = load('de421.bsp')
    earth = planets['earth']
    ts = load.timescale()
    t = ts.now()
    











    

