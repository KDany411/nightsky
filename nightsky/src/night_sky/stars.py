from skyfield.api import Star, Loader, load, wgs84
from skyfield.data import hipparcos
import skyfield.units
load = Loader('nightsky/src')
def load_stars(max_magnitude=6):
    with load.open(hipparcos.URL) as f:
        df = hipparcos.load_dataframe(f)
    return df[df['magnitude'] <= max_magnitude]

def observe_stars(position=wgs84.latlon(50.093977480399595, 14.450417726625702)):
    planets = load('de421.bsp')
    earth = planets['earth']
    ts = load.timescale()
    t = ts.now()
    for index, row in load_stars().iterrows():
        star = Star.from_dataframe(row)
        astro = position.at(t)
        thing = astro 
        alt, az, distance = thing.altaz()

    


observe_stars()








    

