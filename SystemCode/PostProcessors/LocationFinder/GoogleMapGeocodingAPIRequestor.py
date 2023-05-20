import requests

class GMGeocodingAPI():
    """
    A class to interact with the Google Maps Geocoding API.

    Attributes
    ----------
    api_key : str
        The API key to use for authentication with the Google Maps Geocoding API. https://developers.google.com/maps/documentation/embed/get-api-key 

    Methods
    -------
    queryCountry(address)
        Returns the country of the given address.
    """
    def __init__(self, api_key: str) -> None:
        """
        Initializes a new instance of the GMGeocodingAPI class.

        Parameters
        ----------
        api_key : str
            The API key to use for authentication with the Google Maps Geocoding API.
        """
        self.api_key = api_key

    def queryCountry(self, address: str) -> str:
        """
        Returns the country of the given address.

        Parameters
        ----------
        address : str
            The address to query.

        Returns
        -------
        dict
            The country, country_code, lat, long of the given address.
        """
        url = self._get_query_statement(address)
        response = requests.get(url)
        data = response.json()
        country = 'unknown'
        country_code = 'unknown'
        lat = 0 # 0 by default
        lng = 0 # 0 by default
        if data["status"] == "OK":
            # Get the country from the first result
            result = data["results"][0]
            
            for component in result["address_components"]:
                if "country" in component["types"]:
                    country = component["long_name"]
                    country_code = component["short_name"]
            try:
                geometry = result["geometry"]
                lat = geometry['location']['lat']
                lng = geometry['location']['lng']
            except Exception as error:
                print(r'Something wrong when getting lat, lng of location: {error}')          
        else:
            print(f"No results found for {address}")

        return {'country': country, 
                'country_code': country_code, 
                'lat': lat, 
                'lng': lng}

    def _get_query_statement(self, address: str) -> str:
        """
        Returns the query statement for the given address.

        Parameters
        ----------
        address : str
            The address to query.

        Returns
        -------
        str
            The query statement for the given address.
        """
        return f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={self.api_key}'
    
    
if __name__=='__main__':

    geoCodingApi = GMGeocodingAPI('AIzaSyAxAQEpYlOt8BFXe9q2JBXne-yhokmFevs')
    print(geoCodingApi.queryCountry('Stockholm'))