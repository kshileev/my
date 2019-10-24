from html.parser import HTMLParser

def download_skyvector():
    import requests
    a = []

    class SkyvectorHTMLParser(HTMLParser):
        def __init__(self):
            super.init()
            self.comms

        def handle_starttag(self, tag, attrs):
            if tag == 'table' and len(attrs) == 1 and attrs[0] == ('id', 'aptcomms'):
                tx = self.get_starttag_text()
                a.append(tag)

        def handle_endtag(self, tag):
            pass
        def handle_data(self, data):
            pass

    #r = requests.get('https://skyvector.com/airport/URSS/Sochi-Airport')

    p = SkyvectorHTMLParser()
    p.feed(txt)
    pass


class AviaDistance:
    def __init__(self, meters):
        self.meters = meters

    @property
    def feets(self):
        return self.meters * 30.42



class AviaLocation:
    def __init__(self, lat, lon, type_of_location, code, src, elevation=None):
        self.lat = lat
        self.lon = lon
        self.elevation = elevation
        self.type_of_point = type_of_location
        self.code = code
        self.src = src

    @staticmethod
    def encode(coll):
        import json

        if type(coll) is list:
            for_json = [x.__dict__ for x in coll]
        elif type(coll) is dict:
            for_json = {k: v.__dict__ for k,v in coll.items()}
        else:
            raise RuntimeError('provided argument is neither list nor dict')
        with open('AviaNavPoint.json', 'w') as f:
            json.dump(for_json, f)


class AviaRadioNav:
    NDB = 'NDB'
    VOR = 'VOR'
    VOR_DME = 'VOR_DME'
    def __init__(self, loc, freq, aeroport_code):
        self.loc = loc
        self.freq = freq
        self.aeroport_code = aeroport_code

    @property
    def icao_code(self):
        return self.loc.code


class AviaRunway:
    def __init__(self, loc, code, dist, surface, src):
        self.edge = AviaLocation(lat=loc[0], lon=[1], type_of_location='RUNWAY', code=code, src=src)
        self.dist = dist
        self.surface = surface


class AviaAeroport:
    KTA = 'KTA'
    def __init__(self, kta):
        self.kta = kta
        self.freq_ATIS = 0
        self.freq_START = 0
        self.freq_TWR = 0
        self.freq_TAXI = 0
        self.freq_APP = 0
        self.runways = []

    @property
    def icao_code(self):
        return self.kta.code

    @property
    def elevation(self):
        return self.kta.elevation


def request_get_url(url):
    import requests

    r = requests.get(url=url)
    if r.ok:
        return r.text
    else:
        return r.reason

def download_world_aero_data():
    import multiprocessing

    urls = []
    for country in ['Russia', 'Ukraine', 'Belarus']:
        urls.append(f'http://worldaerodata.com/nav/{country}.php')
        urls.append(f'http://worldaerodata.com/countries/{country}.php')

    pool = multiprocessing.Pool(processes=20)
    htmls = pool.map(request_get_url, urls)

    urls = []
    for html in htmls:
        if '?nav=' in html:
            for link in html.split('?nav=')[1:]:
                urls.append('http://worldaerodata.com/wad.cgi?nav=' + link.split('"')[0])
        else:
            for link in html.split('?id=')[1:]:
                urls.append('http://worldaerodata.com/wad.cgi?id=' + link.split('"')[0])
    htmls = pool.map(request_get_url, urls)
    nav_points = {}
    for html in htmls:
        fields = html.split('F0F0F0')
        if len(fields) > 25:
            kta = AviaLocation(lat=float(fields[4].split('<br>')[0].split('<BR>')[0].strip('">')),
                               lon=float(fields[5].split('<br>')[0].split('<BR>')[0].strip('">')),
                               elevation=AviaDistance(meters=float(fields[6].split('<br>')[0].split('<BR>')[1].split()[0])),
                               code=fields[2].split('\n')[0].strip('">'),
                               type_of_location=AviaAeroport.KTA,
                               src='http://worldaerodata.com')
            nav_point = AviaAeroport(kta=kta)
            nav_points[nav_point.icao_code] = nav_point
        else:
            loc = AviaLocation(lat=float(fields[7].split('<br>')[0].strip('">')),
                               lon=float(fields[8].split('<br>')[0].strip('">')),
                               type_of_location=fields[1].split('</td')[0].strip('">'),
                               code=fields[2].split('</td')[0].strip('">'),
                               src='http://worldaerodata.com')
            nav_point = AviaRadioNav(loc=loc,
                                     freq=float(fields[4].split('</td')[0].strip('">')),
                                     aeroport_code=fields[9].split('airport=')[1].split('">')[0])
            nav_points[nav_point.icao_code + '_close_to_' + nav_point.aeroport_code] = nav_point
    AviaLocation.encode(coll=nav_points)

def download_route(origin, destination):
    import requests
    import json

    url = f'https://infogate.matfmc.ru/htme/routes.htme?form-submit=FIRSForm.FIRSHtmlForm&fPntIn={origin}&fPntOut={destination}&SearchBtn=%CF%EE%E8%F1%EA'

    r = requests.get(url, verify=False)
    routes = []
    for route in r.text.split(origin)[2:]:
        params = route.split('<td align=center>')
        d = {'ort_dist': params[2].split('</td')[0],
             'route_dist': params[3].split('</td')[0],
             'route': params[4].split('</td')[0].split()
             }
        routes.append(d)
    with open(f'avia_routes_{origin}_{destination}.json', 'w') as f:
        json.dump(routes, f)


if __name__ == '__main__':
    # download_route(origin='URSS', destination='UUWW')
    download_world_aero_data()
#    download_skyvector()