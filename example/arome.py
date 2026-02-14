from astronacht_meteo.geosphere_api.arome import AROME

if __name__ == "__main__":
    ar = AROME()
    m = ar.metadata
    print(m.keys())
