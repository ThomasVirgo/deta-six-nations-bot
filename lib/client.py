import requests


class SixNationsClient:
    def __init__(self) -> None:
        self.player_url = (
            "https://fantasy.sixnationsrugby.com/v1/private/searchjoueurs?lg=en"
        )

    def get_headers(self):
        return {
            "accept": "application/json",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "authorization": "Token eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NzU1MTU2NTMsImV4cCI6MTY3NzkzNDg1MywianRpIjoiSGRXS0JkV09vOG8rZVpIVVwvbEFPVVE9PSIsImlzcyI6Imh0dHBzOlwvXC9mYW50YXN5LnNpeG5hdGlvbnNydWdieS5jb20iLCJzdWIiOnsiaWQiOiIzMTQ4NzQiLCJtYWlsIjoidG9tY3ZpcmdvQGdtYWlsLmNvbSIsIm1hbmFnZXIiOiJUdXJkbyIsImlkbCI6IjEiLCJpZGciOiI3OTcxNCIsImZ1c2VhdSI6IkV1cm9wZVwvTG9uZG9uIiwibWVyY2F0byI6MCwiaWRqZyI6IjMzNjI0OSIsImlzYWRtaW5jbGllbnQiOmZhbHNlLCJpc2FkbWluIjpmYWxzZSwiaXNzdXBlcmFkbWluIjpmYWxzZSwidmlwIjpmYWxzZSwiaWRlbnRpdHkiOiI2MDAiLCJpZ25vcmVjb2RlIjpmYWxzZSwiY29kZSI6IjYwMC4yIiwiY29kZUY1IjoiNjAwLjQiLCJkZWNvIjowfX0.85EC8OvRGUpic_czjQtXNCGhSuB5h5EY5d7LVTFDN9Y",
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

    def get_body(self, page_size: int):
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
                "idj": "1",
                "pageIndex": 0,
                "pageSize": page_size,
                "loadSelect": 0,
                "searchonly": 1,
            }
        }

    def get_players(self, page_size: int):
        response = requests.post(
            self.player_url, json=self.get_body(page_size), headers=self.get_headers()
        )
        return response.json()


if __name__ == "__main__":
    client = SixNationsClient()
    print(client.get_players(500))
