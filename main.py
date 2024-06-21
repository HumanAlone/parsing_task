import csv
import os

import requests
from dotenv import load_dotenv

from settings import countries

load_dotenv()


class LastfmParser:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://ws.audioscrobbler.com/2.0/"

    def _get_response(self, params):
        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            return response.json()
        return

    def get_top_artists_by_country(self, countries, limit=10):
        params = {
            "method": "geo.getTopArtists",
            "api_key": self.api_key,
            "format": "json",
            "limit": limit,
        }
        topartists = []
        for country in countries:
            params["country"] = country[0]
            data = self._get_response(params)
            if data and data.get("topartists") and data.get("topartists").get("artist"):
                for artist in data["topartists"]["artist"]:
                    topartists.append(
                        (
                            country[0],
                            artist["name"],
                            artist["listeners"],
                            country[1],
                            country[2],
                        )
                    )
        return topartists

    def get_top_tracks_by_country(self, countries, limit=10):
        params = {
            "method": "geo.getTopTracks",
            "api_key": self.api_key,
            "format": "json",
            "limit": limit,
        }
        toptracks = []
        for country in countries:
            params["country"] = country[0]
            data = self._get_response(params)
            if data and data.get("tracks") and data.get("tracks").get("track"):
                for track in data["tracks"]["track"]:
                    toptracks.append(
                        (
                            country[0],
                            track["name"],
                            track["artist"]["name"],
                            track["listeners"],
                            country[1],
                            country[2],
                        )
                    )
        return toptracks

    def get_top_tags(self, limit=1000):
        params = {
            "method": "chart.getTopTags",
            "api_key": self.api_key,
            "format": "json",
            "limit": limit,
        }
        data = self._get_response(params)
        return data.get("tags").get("tag")

    def get_top_artists(self):
        params = {
            "method": "chart.getTopArtists",
            "api_key": self.api_key,
            "format": "json",
        }
        data = self._get_response(params)
        return data.get("artists").get("artist")

    def get_top_tracks(self):
        params = {
            "method": "chart.getTopTracks",
            "api_key": self.api_key,
            "format": "json",
        }
        data = self._get_response(params)
        return data.get("tracks").get("track")

    def get_top_albums(self, mbid):
        params = {
            "method": "artist.getTopAlbums",
            "api_key": self.api_key,
            "format": "json",
            "mbid": mbid,
        }
        data = self._get_response(params)
        return data

    def get_album_info(self, mbid):
        params = {
            "method": "album.getInfo",
            "api_key": self.api_key,
            "format": "json",
            "mbid": mbid,
        }
        data = self._get_response(params)
        return data

    def save_artists_to_csv(self, data, filename):
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Country", "Artist", "Listeners", "Longitude", "Latitude"])
            for entry in data:
                writer.writerow(entry)

    def save_tracks_to_csv(self, data, filename):
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                ["Country", "Name", "Artist", "Listeners", "Longitude", "Latitude"]
            )
            for entry in data:
                writer.writerow(entry)

    def save_tags_to_csv(self, data, filename):
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Reach", "Taggings"])
            for entry in data:
                writer.writerow((entry["name"], entry["reach"], entry["taggings"]))

    def save_top_artists_to_csv(self, data, filename):
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Playcount", "Listeners"])
            for top_artist in data:
                writer.writerow(
                    (
                        top_artist["name"],
                        top_artist["playcount"],
                        top_artist["listeners"],
                    )
                )

    def save_top_tracks_to_csv(self, data, filename):
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Artist", "Playcount", "Listeners"])
            for top_track in data:
                writer.writerow(
                    (
                        top_track["name"],
                        top_track["artist"]["name"],
                        top_track["playcount"],
                        top_track["listeners"],
                    )
                )


if __name__ == "__main__":
    api_key = os.getenv("LASTFM_API_KEY")
    parser = LastfmParser(api_key)

    top_artists_by_country = parser.get_top_artists_by_country(countries)
    parser.save_artists_to_csv(
        top_artists_by_country, "docs/top_artists_by_country.csv"
    )

    top_tracks_by_country = parser.get_top_tracks_by_country(countries)
    parser.save_tracks_to_csv(top_tracks_by_country, "docs/top_tracks_by_country.csv")

    top_tags = parser.get_top_tags(limit=15)
    parser.save_tags_to_csv(top_tags, "docs/top_tags.csv")

    top_artists = parser.get_top_artists()
    parser.save_top_artists_to_csv(top_artists, "docs/top_artists.csv")

    top_tracks = parser.get_top_tracks()
    parser.save_top_tracks_to_csv(top_tracks, "docs/top_tracks.csv")
