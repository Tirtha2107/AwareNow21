import os
import requests

files = {
  "theft_pickpocket.jpg":"https://upload.wikimedia.org/wikipedia/commons/4/4e/Police_lights.jpg",
  "robbery_armed.jpg":"https://upload.wikimedia.org/wikipedia/commons/0/0d/Police_car_with_lights_on.jpg",
  "assault_first_aid.jpg":"https://upload.wikimedia.org/wikipedia/commons/6/69/First_aid_kit.jpg",
  "domestic_violence_ribbon.png":"https://upload.wikimedia.org/wikipedia/commons/4/4b/Domestic_violence_awareness_ribbon.png",
  "sexual_assault_help_sign.jpg":"https://upload.wikimedia.org/wikipedia/commons/5/59/Help-sign.jpg",
  "burglary_locked_door.jpg":"https://upload.wikimedia.org/wikipedia/commons/7/7d/Locked_door.jpg",
  "fraud_scams_email_spam.jpg":"https://upload.wikimedia.org/wikipedia/commons/8/89/Email_spam.jpg",
  "cybercrime_computer.jpg":"https://upload.wikimedia.org/wikipedia/commons/6/6a/Cybercrime_Computer.jpg",
  "kidnapping_police_officer.jpg":"https://upload.wikimedia.org/wikipedia/commons/1/1a/Police_officer.jpg",
  "arson_fire_station.jpg":"https://upload.wikimedia.org/wikipedia/commons/3/3f/Fire_station.jpg",
  "earthquake_damage.jpg":"https://upload.wikimedia.org/wikipedia/commons/4/4f/Earthquake_damage.jpg",
  "flood_flooded_street.jpg":"https://upload.wikimedia.org/wikipedia/commons/5/5c/Flooded_street.jpg",
  "tsunami_evac_route_japan.jpg":"https://upload.wikimedia.org/wikipedia/commons/5/55/Tsunami_Evacuation_Route_Japan.jpg",
  "hurricane_katrina.jpg":"https://upload.wikimedia.org/wikipedia/commons/7/7a/Hurricane_Katrina_from_GOES-12_2005-08-28.jpg",
  "tornado_cooper.jpg":"https://upload.wikimedia.org/wikipedia/commons/0/09/Tornado_at_Cooper.jpg",
  "wildfire_smoke.jpg":"https://upload.wikimedia.org/wikipedia/commons/1/15/Wildfire_smoke.jpg",
  "landslide_nepal.jpg":"https://upload.wikimedia.org/wikipedia/commons/9/92/Landslide_Nepal.jpg",
  "volcanic_eruption.jpg":"https://upload.wikimedia.org/wikipedia/commons/2/28/Volcano_Eruption.jpg",
  "heatwave_hot_sun.jpg":"https://upload.wikimedia.org/wikipedia/commons/2/2f/Hot_sun.jpg",
  "severe_storm_thunderstorm.jpg":"https://upload.wikimedia.org/wikipedia/commons/3/3d/Thunderstorm.jpg",
  "blizzard.jpg":"https://upload.wikimedia.org/wikipedia/commons/6/6b/Blizzard.jpg",
  "foggy_road.jpg":"https://upload.wikimedia.org/wikipedia/commons/7/77/Foggy_Road.jpg"
}

os.makedirs("images", exist_ok=True)

for fname, url in files.items():
    path = os.path.join("images", fname)
    print(f"Downloading {fname} ...")
    resp = requests.get(url, stream=True)
    if resp.status_code == 200:
        with open(path, "wb") as f:
            for chunk in resp.iter_content(1024):
                f.write(chunk)
    else:
        print(f"Failed to download {url} (status {resp.status_code})")

print("Done — images saved in ./images")
