import csv
import random


def add_random_offset(latitude, longitude, offset=2):
    lat_offset = latitude + random.uniform(-offset, offset)
    lon_offset = longitude + random.uniform(-offset, offset)
    return lat_offset, lon_offset


input_file = "top_tracks_by_country_geo_offset.csv"
output_file = "tracks_with_offset.csv"

with open(input_file, mode="r", newline="", encoding="utf-8") as infile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames + ["longitude_offset", "latitude_offset"]

    with open(output_file, mode="w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            latitude = float(row["Latitude"])
            longitude = float(row["Longitude"])
            lat_offset, lon_offset = add_random_offset(latitude, longitude)

            row["latitude_offset"] = lat_offset
            row["longitude_offset"] = lon_offset
            writer.writerow(row)

print(f"Data with offsets saved to {output_file}")
