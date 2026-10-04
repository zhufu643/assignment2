# Global Earthquake Activity

![Global earthquake activity](out/plot.png)

## The phenomenon

This project looks at global earthquakes of magnitude 2.5 and above during one month. Earthquakes happen every day, but their number, magnitude, and depth change over time. Most people usually only notice strong earthquakes reported in the news, while many smaller earthquakes happen continuously. I wanted to look at this phenomenon because the data makes it possible to compare individual strong events with the overall pattern of earthquake activity. The visualization focuses on how earthquake magnitude and frequency change across different days.

## The source

The data comes from the USGS Earthquake Hazards Program:

https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php

The dataset contains about 2000 earthquake records. Each row represents one earthquake event and includes its time, magnitude, location, latitude, longitude, and depth. Depth is measured in kilometres.

## What the picture shows

The upper scatter plot shows individual earthquakes over time. The x-axis is date, the y-axis is magnitude, and point colour represents earthquake depth. The dashed line marks magnitude 5.0, while several stronger earthquakes are labelled.

The lower heatmap groups the same data by day and magnitude band. Each square shows how many earthquakes occurred in one magnitude range on one day, and darker colours mean more earthquakes. This makes daily patterns easier to see, but it also hides some detail. The heatmap combines many separate events, so the exact magnitude, depth, and location of each earthquake are no longer visible. The chart also does not show the geographic distribution of the earthquakes.

## Run it

```bash
uv run fetch.py
uv run plot.py