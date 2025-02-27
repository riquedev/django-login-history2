import typing
from unittest.mock import MagicMock

IPApiResponse = typing.Tuple[typing.Dict, int
]
SUCCESS_RESPONSE: IPApiResponse = ({
                                       "ip": "8.8.8.8",
                                       "network": "8.8.8.0/24",
                                       "version": "IPv4",
                                       "city": "Mountain View",
                                       "region": "California",
                                       "region_code": "CA",
                                       "country": "US",
                                       "country_name": "United States",
                                       "country_code": "US",
                                       "country_code_iso3": "USA",
                                       "country_capital": "Washington",
                                       "country_tld": ".us",
                                       "continent_code": "NA",
                                       "in_eu": False,
                                       "postal": "94043",
                                       "latitude": 37.42301,
                                       "longitude": -122.083352,
                                       "timezone": "America/Los_Angeles",
                                       "utc_offset": "-0800",
                                       "country_calling_code": "+1",
                                       "currency": "USD",
                                       "currency_name": "Dollar",
                                       "languages": "en-US,es-US,haw,fr",
                                       "country_area": 9629091.0,
                                       "country_population": 327167434,
                                       "asn": "AS15169",
                                       "org": "GOOGLE"
                                   }, 200)

QUOTA_EXCEEDED_RESPONSE: IPApiResponse = ({"error": True, "reason": "RateLimited", "message": "127.0.0.1"}, 429)
INVALID_IP_ADDRESS_RESPONSE: IPApiResponse = ({"error": True, "reason": "Invalid IP Address", "ip": "127.0.0.1"}, 200)
RESERVED_IP_ADDRESS_RESPONSE: IPApiResponse = ({"error": True, "reason": "Reserved IP Address", "ip": "127.0.0.1"}, 200)
INVALID_KEY_RESPONSE: IPApiResponse = ({
                                           "error": True,
                                           "reason": "Invalid Key",
                                           "message": "Invalid key. SignUp @ https://ipapi.co/pricing/ "
                                       }, 403)


def get_mock(response: IPApiResponse) -> MagicMock:
    magic = MagicMock()
    magic.json.return_value = response[0]
    magic.status_code = response[1]
    return magic
