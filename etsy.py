from urllib import urlopen, urlencode
try:
        import simplejson as json
except ImportError:
        import json


class Etsy(object):
    base_url = "http://beta-api.etsy.com/v1/"

    def __init__(self, api_key):
        self.__api_key = api_key
    
    def _make_call(self, path, params):
        basedict = {"api_key":self.__api_key}
        basedict.update(params)
        fullurl = self.base_url + path + '?' + urlencode(basedict)
        f = urlopen(fullurl)

        ret = json.load(f)
        f.close()
        return ret

    def getUserDetails(self, user_id, **params):
        path = '/users/'
        a = {'user_id':user_id}

        a.update(params)

        r = self._make_call(path, a)

        u = EtsyUser(self, r['results'][0])
        return u

    def getUsersByName(self, search_name, **params):
        path = '/users/keywords/'
        a = {'search_name':search_name}

        a.update(params)

        r = self._make_call(path, a)

        return [EtsyUser(self, u) for u in r['results']]

    def getFavoriteListingsOfUser(self, user_id, **params):
        path = '/users/%s/favorites/listings' % user_id

        r = self._make_call(path, params)

        return [EtsyResource(self, u) for u in r['results']]

    def getFavorersOfUser(self, user_id, **params):
        path = '/users/%s/favorers' % user_id

        r = self._make_call(path, params)

        return [EtsyUser(self, u) for u in r['results']]






class EtsyUser(EtsyResource):
    def getFavorers(self, **params):
        return self.etsy.getFavorersOfUser(self.user_name, **params)

    def getFavoriteListings(self, **params):
        return self.etsy.getFavoriteListingsOfUser(self.user_name, **params)

    #def getFavoriteShops(self, **params):
    #    return self.etsy.getFavoriteShopsOfUser(self.user_name, **params)



class EtsyResource (object):
    def __init__(self, etsy, d):
        self.__dict__ = d
        self.etsy = etsy

    def __repr__(self):
        return '<' + ', '.join(['%s=%s' % (key, value.__repr__())
                                for key, value
                                in self.__dict__.iteritems()]) + '>'

