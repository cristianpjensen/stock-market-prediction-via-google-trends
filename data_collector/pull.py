import json
import requests


def main():
    token = get_token("debt", "2004-01-01 2020-06-01")

    print(token)


def get_token(keyword, timespan):
    """
    Retrieves a token from Google Trends, based on the keyword and timespan.

    This function is a deritative of the Pytrends module, by github.com/GeneralMills.
    Licensed under the Apache license, version 2.0.
    Changes made by github.com/cristianpjensen to fit Njord's use case.
    """
    session = requests.session()

    response = session.get(
        url="https://trends.google.com/trends/api/explore",
        timeout=(2, 5),
        cookies=dict(filter(lambda i: i[0] == "NID", requests.get(
            "https://trends.google.com/?geo=US",
            timeout=(2, 5)
        ).cookies.items())),
        params={"hl": "en-US", "tz": -120,
                "req": '{"comparisonItem": [{"keyword": ' + f'"{keyword}"' + ', "time": ' + f'"{timespan}"' + ', "geo": "US"}], "category": 0, "property": ""}'}
    )

    content = response.text[4:]
    return json.loads(content)["widgets"][0]["token"]


if __name__ == "__main__":
    main()
