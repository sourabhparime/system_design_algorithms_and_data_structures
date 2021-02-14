"""
Reviewed when doing location based system design question for example yelp:
https://docs.google.com/drawings/d/1vfGhV1YR1C2S3Dfh4TrrcWz5MWBLrEksSEcdjqNyOsc/edit

Geohash library code: https://github.com/vinsci/geohash/blob/master/Geohash/geohash.py

Review this when doing Leetcode and under leetcode hard questions.
"""


class GeoHash(object):
    """
    Geohash class to encode and deocode the lat long into boxes
    """
    __base32 = '0123456789bcdefghjkmnpqrstuvwxyz'
    __decodemap = {}

    for i in range(len(__base32)):
        __decodemap[__base32[i]] = i

    @classmethod
    def encode(self, latitude, longitude, precision=12, __base32=__base32):
        """
        Encode a position given in float arguments latitude, longitude to
        a geohash which will have the character count precision.
        """
        lat_interval, lon_interval = (-90.0, 90.0), (-180.0, 180.0)
        geohash = []
        bits = [16, 8, 4, 2, 1]
        bit = 0
        ch = 0
        even = True
        # Binary search on tolerance style
        while len(geohash) < precision:
            if even:
                mid = (lon_interval[0] + lon_interval[1]) / 2
                if longitude > mid:
                    ch |= bits[bit]
                    lon_interval = (mid, lon_interval[1])
                else:
                    lon_interval = (lon_interval[0], mid)
            else:
                mid = (lat_interval[0] + lat_interval[1]) / 2
                if latitude > mid:
                    ch |= bits[bit]
                    lat_interval = (mid, lat_interval[1])
                else:
                    lat_interval = (lat_interval[0], mid)
            even = not even
            if bit < 4:
                bit += 1
            else:
                geohash += __base32[ch]
                bit = 0
                ch = 0
        return ''.join(geohash)

    @classmethod
    def decode_exactly(self, geohash, __decodemap=__decodemap):
        """
        Decode the geohash to its exact values, including the error
        margins of the result.  Returns four float values: latitude,
        longitude, the plus/minus error for latitude (as a positive
        number) and the plus/minus error for longitude (as a positive
        number).
        """
        lat_interval, lon_interval = (-90.0, 90.0), (-180.0, 180.0)
        lat_err, lon_err = 90.0, 180.0
        is_even = True
        for c in geohash:
            cd = __decodemap[c]
            for mask in [16, 8, 4, 2, 1]:
                if is_even:  # adds longitude info
                    lon_err /= 2
                    if cd & mask:
                        lon_interval = ((lon_interval[0] + lon_interval[1]) / 2, lon_interval[1])
                    else:
                        lon_interval = (lon_interval[0], (lon_interval[0] + lon_interval[1]) / 2)
                else:  # adds latitude info
                    lat_err /= 2
                    if cd & mask:
                        lat_interval = ((lat_interval[0] + lat_interval[1]) / 2, lat_interval[1])
                    else:
                        lat_interval = (lat_interval[0], (lat_interval[0] + lat_interval[1]) / 2)
                is_even = not is_even
        lat = (lat_interval[0] + lat_interval[1]) / 2
        lon = (lon_interval[0] + lon_interval[1]) / 2
        return lat, lon, lat_err, lon_err


print("Testing geo hashing with encoding current location co ordinates ", GeoHash.encode(41.878113, -87.629799))
print("Testing geo hashing with decoding current location geohash ", GeoHash.decode_exactly(geohash="dp3wjztvtwjf"))
