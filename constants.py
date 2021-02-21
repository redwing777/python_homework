from dataclasses import dataclass


@dataclass()
class TestProfile:
    url: str = "https://booking.com"
    ext_file: str = "./extension/djennkbadhfcmhlbejdidgmdgnacbcmi.crx"
    timeout: float = 0.5
    prefered_city: str = "Budapest"


desired_caps = {
    "chrome": {
        "browserName": "chrome",
        "screenResolution": "1920x1080x24",
        "browserVersion": "78.0",
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True
        }
    }
}