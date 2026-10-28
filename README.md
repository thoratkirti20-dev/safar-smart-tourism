# Safar — Smart Tourism India

A Flask tourism website featuring 50 destinations (15 in Maharashtra and 35 elsewhere in India), real destination photographs loaded from Wikipedia/Wikimedia when available, expanded place summaries and a details dialog with highlights, suggested visit seasons, duration guidance and travel tips. It also includes destination search and filters, an interactive Leaflet/OpenStreetMap map, current-location support, OSRM road-route estimates, nearby facility searches through Google Maps, and an external Rapido link.

## Project files

```text
safar_smart_tourism/
├── app.py
├── requirements.txt
├── templates/
│   └── index.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── map.js
```

## Run on Windows / VS Code

1. Extract the ZIP file to a folder, for example `C:\Users\YOUR_USERNAME\Downloads\safar_smart_tourism`.
2. Open that folder in VS Code (`File → Open Folder`).
3. Open `Terminal → New Terminal`.
4. Create a virtual environment if you do not already have one:

   ```powershell
   python -m venv venv
   ```

5. Activate it:

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

6. Install Flask:

   ```powershell
   python -m pip install -r requirements.txt
   ```

7. Start the website:

   ```powershell
   python app.py
   ```

8. Open `http://127.0.0.1:5000` in your browser.

If you already have an activated `venv`, skip steps 4 and 5. Keep the terminal running while using the website. Press `Ctrl+C` in the terminal to stop Flask.

## Features and notes

- Search by destination, city, state, category, or description.
- Filter Maharashtra destinations separately from other Indian destinations.
- Browse all 50 destination cards and select any destination for the map.
- Card photographs and article extracts are loaded from the Wikipedia REST summary API as cards approach the screen. If a page has no usable thumbnail or the connection fails, the card displays a fallback illustration instead.
- Use “About place” to open a detail panel with an encyclopedia extract, key highlights, suggested visit timing, approximate time to allow, practical visitor tips, and links to the article and image source.
- Photo-source links open the relevant Wikimedia Commons file page when the image is hosted there, so users can review the file author and licence details. If the image is not from Commons, the link opens the Wikipedia article.
- Map tiles are served by OpenStreetMap and rendered with Leaflet.
- Browser geolocation generally works on `localhost` / `127.0.0.1`, subject to browser permission and device settings.
- Road routes and drive-time estimates use the public OSRM demo endpoint. It is a demo service, may be rate-limited or unavailable, and does not provide live traffic predictions.
- Hotels, restaurants, hospitals, and parking use Google Maps search links; they are not a live in-page directory.
- Rapido opens its website in a new tab. This demo does not integrate a booking API, automatically share the destination, or book rides.
- The page loads Wikipedia/Wikimedia photos and summaries, Leaflet, OpenStreetMap tiles, OSRM routes, and Google Maps searches from online services, so internet access is needed for the complete presentation.
