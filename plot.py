# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///

"""
Read the earthquake GeoJSON file in data/,
make one picture with two panels, and save it to out/.

Top panel:
    scatter plot of individual earthquakes over time

Bottom panel:
    heatmap of daily earthquake counts by magnitude band

Run:

    uv run plot.py
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt


FILE = "earthquakes-2.5-month.geojson"
PICTURE = "earthquakes-scatter-heatmap.png"

HERE = Path(__file__).parent
DATA = HERE / "data" / FILE
OUT = HERE / "out"


def load_earthquakes(path):
    """Return the earthquake features from the GeoJSON file."""
    with path.open(encoding="utf-8") as handle:
        raw = json.load(handle)

    return raw["features"]


def magnitude_band_index(mag):
    """Return the row index for the magnitude-band heatmap."""
    if 2.5 <= mag < 3.0:
        return 0
    if 3.0 <= mag < 4.0:
        return 1
    if 4.0 <= mag < 5.0:
        return 2
    return 3   # 5.0+


def all_days_between(start_date, end_date):
    """Return every date from start_date to end_date inclusive."""
    days = []
    current = start_date
    while current <= end_date:
        days.append(current)
        current += timedelta(days=1)
    return days


def main():
    table = load_earthquakes(DATA)

    print(f"{DATA.name}: {len(table)} earthquake records")
    print("The first earthquake record:")
    print(table[0])

    times = []
    mags = []
    depths = []
    places = []
    dates = []

    # loop over the earthquake records
    for feature in table:
        props = feature["properties"]

        mag = props["mag"]
        when = props["time"]
        place = props["place"]

        coordinates = feature["geometry"]["coordinates"]
        depth = coordinates[2]

        if mag is None or when is None or depth is None:
            continue

        event_time = datetime.fromtimestamp(when / 1000)

        times.append(event_time)
        mags.append(float(mag))
        depths.append(float(depth))
        places.append(place if place else "Unknown location")
        dates.append(event_time.date())

    print(f"{len(mags)} earthquakes kept")
    print(f"Magnitude range: {min(mags)} to {max(mags)}")
    print(f"Depth range: {min(depths)} to {max(depths)} km")

    # ----- build the heatmap table -----

    start_date = min(dates)
    end_date = max(dates)
    day_list = all_days_between(start_date, end_date)
    day_to_col = {day: i for i, day in enumerate(day_list)}

    band_labels = [
        "2.5–3.0",
        "3.0–4.0",
        "4.0–5.0",
        "5.0+",
    ]

    heatmap = [
        [0 for _ in day_list]
        for _ in band_labels
    ]

    for event_date, mag in zip(dates, mags):
        row = magnitude_band_index(mag)
        col = day_to_col[event_date]
        heatmap[row][col] += 1

    max_daily_count = max(max(row) for row in heatmap)
    print(f"Highest daily count in one band: {max_daily_count}")

    # ----- figure layout -----

    fig, (ax1, ax2) = plt.subplots(
        2,
        1,
        figsize=(12, 8),
        height_ratios=[3, 1.6],
        sharex=True
    )

    first_time = min(times)
    last_time = max(times)

    # ----- top panel: scatter -----

    scatter = ax1.scatter(
        times,
        mags,
        c=depths,
        s=22,
        alpha=0.6,
        cmap="magma_r"
    )

    ax1.axhline(
        5.0,
        linestyle="--",
        linewidth=1,
        alpha=0.5
    )

    ax1.text(
        first_time,
        5.05,
        "M5.0",
        fontsize=9,
        ha="left"
    )

    ax1.set_ylabel("Magnitude")
    ax1.set_ylim(2.3, max(mags) + 0.8)
    ax1.grid(alpha=0.15)

    # label the three strongest earthquakes
    top3 = sorted(
        range(len(mags)),
        key=lambda i: mags[i],
        reverse=True
    )[:3]

    offsets = [
        (10, 34),
        (36, -12),
        (-140, 18)
    ]

    for index, offset in zip(top3, offsets):
        place_text = places[index]
        if len(place_text) > 34:
            place_text = place_text[:34] + "..."

        ax1.annotate(
            f"M{mags[index]:.1f}\n{place_text}",
            (times[index], mags[index]),
            xytext=offset,
            textcoords="offset points",
            fontsize=8,
            linespacing=1.5,
            arrowprops={
                "arrowstyle": "->",
                "linewidth": 0.8
            }
        )

    ax1.set_title(
        "Individual earthquakes: time, magnitude and depth",
        pad=12
    )

    depth_bar = fig.colorbar(
        scatter,
        ax=ax1,
        pad=0.02
    )
    depth_bar.set_label("Depth below surface (km)")

    # ----- bottom panel: heatmap -----

    # imshow needs numeric x positions, so use matplotlib date numbers
    x0 = mdates.date2num(day_list[0])
    x1 = mdates.date2num(day_list[-1] + timedelta(days=1))

    image = ax2.imshow(
        heatmap,
        aspect="auto",
        origin="lower",
        interpolation="nearest",
        cmap="Blues",
        extent=[x0, x1, -0.5, len(band_labels) - 0.5]
    )

    ax2.set_yticks(range(len(band_labels)))
    ax2.set_yticklabels(band_labels)
    ax2.set_ylabel("Magnitude band")
    ax2.set_xlabel("Date")
    ax2.set_title(
        "Daily earthquake counts by magnitude band",
        pad=10
    )

    count_bar = fig.colorbar(
        image,
        ax=ax2,
        pad=0.02
    )
    count_bar.set_label("Earthquakes per day")

    # ----- shared x-axis formatting -----

    locator = mdates.DayLocator(interval=4)
    formatter = mdates.DateFormatter("%Y-%m-%d")

    ax2.xaxis.set_major_locator(locator)
    ax2.xaxis.set_major_formatter(formatter)

    ax1.tick_params(axis="x", labelbottom=False)
    fig.autofmt_xdate(rotation=30)

    # ----- overall title -----

    fig.suptitle(
        f"{len(mags)} Global Earthquakes of Magnitude 2.5+ — "
        f"{first_time:%d %b} to {last_time:%d %b %Y}",
        fontsize=16,
        y=0.98
    )

    fig.tight_layout(rect=[0, 0, 1, 0.96])

    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / PICTURE, dpi=150)

    print(f"saved out/{PICTURE}")

    plt.show()


if __name__ == "__main__":
    main()