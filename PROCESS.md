# Process

<!-- The first step was to fetch and save the data. I used `fetch.py` to download earthquake records from the USGS GeoJSON source and store them locally. After that, `plot.py` could read the cached file directly instead of downloading the data every time. This also made it possible to regenerate the visualization offline.

My first version was a simple scatter plot. The x-axis represented time, the y-axis represented earthquake magnitude, and each point represented one earthquake event. This version worked, but it looked too simple and did not show enough information about the overall pattern. I then added more layers of information. I used point colour to represent earthquake depth, so each point could show time, magnitude, and depth at the same time. I also added an M5.0 reference line and labels for several of the strongest earthquakes so that larger events were easier to identify. Later, I noticed that the scatter plot was useful for individual earthquakes, but it was difficult to see how earthquake frequency changed from day to day. Because of this, I added a heatmap below the scatter plot. The heatmap groups earthquakes by date and magnitude band, including 2.5–3.0, 3.0–4.0, 4.0–5.0, and 5.0+. Each cell represents the number of earthquakes in one magnitude range on one day, and darker colours mean more earthquakes. This creates a clear contrast between individual events in the scatter plot and overall patterns in the heatmap.
During the design process, I also adjusted the font sizes, label positions, legends, spacing, and overall layout to reduce overlap and improve readability.

I used AI tools as support during this project. AI helped me understand Python code, explain error messages, and suggest possible improvements to the visualization. It also helped me explore ideas such as adding earthquake depth, the M5.0 reference line, labels for stronger earthquakes, and the magnitude-band heatmap. AI also gave suggestions for data grouping, layout adjustments, and wording in the README and PROCESS file.

 -->

## Tools
Microsoft
Visual Studio Code
ChatGPT

## Kept

## Rejected
