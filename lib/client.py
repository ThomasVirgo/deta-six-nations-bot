from typing import Optional
import requests


class SixNationsClient:
    def __init__(self, token: Optional[str] = None) -> None:
        self.token = token
        self.player_url = (
            "https://fantasy.sixnationsrugby.com/v1/private/searchjoueurs?lg=en"
        )
        self.login_url = "https://fantasy.sixnationsrugby.com/v1/public/login?lg=en"

    def get_headers(self, add_auth: bool = False):
        headers = {
            "accept": "application/json",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "content-type": "application/json",
            "sec-ch-ua": '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-access-key": "600@14.04@",
            "cookie": "_gid=GA1.2.982290925.1675421657; __gads=ID=d78c75aa92a9b1a1:T=1675421657:S=ALNI_MZXED3KybBhN-57ZHiQILXtmor6jg; __gpi=UID=00000bd1b52320a8:T=1675421657:RT=1675421657:S=ALNI_MZfbHrarhLg633py-MxtpUh8ledxw; _ga=GA1.3.994192290.1675421657; _gid=GA1.3.982290925.1675421657; _fbp=fb.1.1675431537584.1984078954; _ga_4K568SMX64=GS1.1.1675514713.3.1.1675514722.0.0.0; _gat_tracker1=1; _gat_tracker2=1; _ga=GA1.2.994192290.1675421657; _gat_gtag_UA_28936500_4=1; _ga_Z8CQEC7B8T=GS1.1.1675514674.2.1.1675515653.0.0.0",
            "Referer": "https://fantasy.sixnationsrugby.com/",
            "Referrer-Policy": "strict-origin-when-cross-origin",
        }
        if add_auth:
            headers["authorization"] = f"Token {self.token}"

        return headers

    def get_players_body(self, page_size: int):
        return {
            "filters": {
                "nom": "",
                "club": "",
                "position": "",
                "budget_ok": False,
                "engage": False,
                "partant": False,
                "dreamteam": False,
                "quota": "",
                "idj": "2",
                "pageIndex": 0,
                "pageSize": page_size,
                "loadSelect": 0,
                "searchonly": 1,
            }
        }

    def get_players(self, page_size: int):
        response = requests.post(
            self.player_url,
            json=self.get_players_body(page_size),
            headers=self.get_headers(add_auth=True),
        )
        return response.json()

    def login(self, email: str, password: str) -> str:
        body = {
            "user": {
                "mail": email,
                "password": password,
                "fcmtoken": "",
            }
        }
        response = requests.post(self.login_url, headers=self.get_headers(), json=body)
        data = response.json()
        return data.get("user", {}).get("token", "")


if __name__ == "__main__":
    pass
