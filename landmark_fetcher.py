import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# 每個城市對應的地標圖片（加上 User-Agent header）
LANDMARK_URLS = {
    "New York City":   "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Southwest_corner_of_Central_Park%2C_looking_east%2C_NYC.jpg/960px-Southwest_corner_of_Central_Park%2C_looking_east%2C_NYC.jpg",
    "Los Angeles":     "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/LA_Skyline_Mountains2.jpg/960px-LA_Skyline_Mountains2.jpg",
    "Dallas":          "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Dallas_skyline_and_suburbs.jpg/960px-Dallas_skyline_and_suburbs.jpg",
    "San Francisco":   "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/GoldenGateBridge-001.jpg/960px-GoldenGateBridge-001.jpg",
    "Seattle":         "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Space_Needle002.jpg/480px-Space_Needle002.jpg",
    "Atlanta":         "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Atlanta_from_Buckhead.jpg/960px-Atlanta_from_Buckhead.jpg",
    "Miami":           "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Miami_collage_20110330.jpg/480px-Miami_collage_20110330.jpg",
    "Houston":         "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Houston_skyline_during_twilight.jpg/960px-Houston_skyline_during_twilight.jpg",
    "Kansas City":     "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/KansasCityMOSkyline.jpg/960px-KansasCityMOSkyline.jpg",
    "Philadelphia":    "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/Philadelphia_skyline_from_south_street_bridge_january_2020.jpg/960px-Philadelphia_skyline_from_south_street_bridge_january_2020.jpg",
    "Boston":          "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Boston_-_panoramio_%2823%29.jpg/960px-Boston_-_panoramio_%2823%29.jpg",
    "Mexico City":     "https://upload.wikimedia.org/wikipedia/commons/thumb/8/81/Mexico_City_Reforma.jpg/960px-Mexico_City_Reforma.jpg",
    "Guadalajara":     "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ce/GuadalajaraCathedral.jpg/480px-GuadalajaraCathedral.jpg",
    "Monterrey":       "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Monterrey_nuevo_leon_mexico_macroplaza.jpg/960px-Monterrey_nuevo_leon_mexico_macroplaza.jpg",
    "Toronto":         "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Toronto_-_ON_-_Toronto_Harbourfront3.jpg/960px-Toronto_-_ON_-_Toronto_Harbourfront3.jpg",
    "Vancouver":       "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/Above_Gotham.jpg/960px-Above_Gotham.jpg",
}

HEADERS = {
    "User-Agent": "WorldCupTravelAgent/1.0 (educational project)"
}


def make_placeholder(city: str) -> Image.Image:
    """
    網路完全不通時，用 PIL 畫一張帶城市名稱的純色佔位圖。
    ControlNet 仍可處理，只是邊緣資訊較少。
    """
    img = Image.new("RGB", (512, 512), color=(30, 80, 50))
    draw = ImageDraw.Draw(img)

    # 畫足球紋路
    draw.ellipse([156, 156, 356, 356], outline=(255, 255, 255), width=4)
    draw.ellipse([206, 206, 306, 306], outline=(255, 255, 255), width=2)

    # 城市名稱
    draw.text((256, 420), city, fill=(255, 255, 255), anchor="mm")
    draw.text((256, 60), "FIFA World Cup 2026", fill=(255, 215, 0), anchor="mm")

    print(f"Generated placeholder image for {city}")
    return img


def fetch_landmark(city: str) -> Image.Image:
    """
    根據城市名稱從網路抓地標圖片。
    失敗時直接產生本地佔位圖，不再嘗試第二次網路請求。
    """
    url = LANDMARK_URLS.get(city)

    if url:
        try:
            print(f"Fetching landmark for {city}...")
            resp = requests.get(url, headers=HEADERS, timeout=8)
            resp.raise_for_status()
            image = Image.open(BytesIO(resp.content)).convert("RGB")
            image = image.resize((512, 512))
            print(f"Landmark fetched successfully: {image.size}")
            return image

        except Exception as e:
            print(f"Network fetch failed: {e}")
            print("Falling back to local placeholder image...")

    return make_placeholder(city)