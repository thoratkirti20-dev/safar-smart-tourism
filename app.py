from flask import Flask, render_template, jsonify

app = Flask(__name__)

# 50 curated tourism destinations across India: 15 in Maharashtra and 35 elsewhere.
PLACES = [
    # Maharashtra (15)
    {"id":"gateway-of-india","name":"Gateway of India","city":"Mumbai","state":"Maharashtra","region":"Maharashtra","category":"Heritage","icon":"🏛️","lat":18.9220,"lng":72.8347,"summary":"An iconic waterfront landmark overlooking the Arabian Sea."},
    {"id":"elephanta-caves","name":"Elephanta Caves","city":"Mumbai","state":"Maharashtra","region":"Maharashtra","category":"Heritage","icon":"🗿","lat":18.9633,"lng":72.9315,"summary":"Rock-cut cave temples reached by ferry from Mumbai."},
    {"id":"marine-drive","name":"Marine Drive","city":"Mumbai","state":"Maharashtra","region":"Maharashtra","category":"Nature","icon":"🌊","lat":18.9440,"lng":72.8238,"summary":"A celebrated seaside promenade known for its curved coastline."},
    {"id":"siddhivinayak-temple","name":"Siddhivinayak Temple","city":"Mumbai","state":"Maharashtra","region":"Maharashtra","category":"Spiritual","icon":"🛕","lat":19.0169,"lng":72.8305,"summary":"A well-known temple dedicated to Lord Ganesha."},
    {"id":"sanjay-gandhi-national-park","name":"Sanjay Gandhi National Park","city":"Mumbai","state":"Maharashtra","region":"Maharashtra","category":"Nature","icon":"🌳","lat":19.2147,"lng":72.9106,"summary":"A large green reserve with trails and the Kanheri Caves."},
    {"id":"shaniwar-wada","name":"Shaniwar Wada","city":"Pune","state":"Maharashtra","region":"Maharashtra","category":"Heritage","icon":"🏰","lat":18.5196,"lng":73.8553,"summary":"A historic fortification associated with the Maratha Empire."},
    {"id":"aga-khan-palace","name":"Aga Khan Palace","city":"Pune","state":"Maharashtra","region":"Maharashtra","category":"Heritage","icon":"🏛️","lat":18.5524,"lng":73.9015,"summary":"A landmark palace connected with India's freedom movement."},
    {"id":"sinhagad-fort","name":"Sinhagad Fort","city":"Pune","state":"Maharashtra","region":"Maharashtra","category":"Nature","icon":"⛰️","lat":18.3663,"lng":73.7559,"summary":"A hill fort with panoramic views and trekking routes."},
    {"id":"dagdusheth-temple","name":"Dagdusheth Halwai Ganpati Temple","city":"Pune","state":"Maharashtra","region":"Maharashtra","category":"Spiritual","icon":"🛕","lat":18.5164,"lng":73.8568,"summary":"A famous Ganesha temple in the heart of Pune."},
    {"id":"mahabaleshwar","name":"Mahabaleshwar","city":"Mahabaleshwar","state":"Maharashtra","region":"Maharashtra","category":"Nature","icon":"🌿","lat":17.9307,"lng":73.6477,"summary":"A hill station known for viewpoints, forests and cool weather."},
    {"id":"panchgani","name":"Panchgani","city":"Panchgani","state":"Maharashtra","region":"Maharashtra","category":"Nature","icon":"⛰️","lat":17.9237,"lng":73.8000,"summary":"A scenic hill town famous for Table Land and valley views."},
    {"id":"ajanta-caves","name":"Ajanta Caves","city":"Ajanta","state":"Maharashtra","region":"Maharashtra","category":"Heritage","icon":"🗿","lat":20.5519,"lng":75.7033,"summary":"Ancient Buddhist caves renowned for murals and rock-cut art."},
    {"id":"ellora-caves","name":"Ellora Caves","city":"Ellora","state":"Maharashtra","region":"Maharashtra","category":"Heritage","icon":"🗿","lat":20.0268,"lng":75.1795,"summary":"A remarkable complex of Buddhist, Hindu and Jain monuments."},
    {"id":"grishneshwar-temple","name":"Grishneshwar Temple","city":"Verul","state":"Maharashtra","region":"Maharashtra","category":"Spiritual","icon":"🛕","lat":20.0240,"lng":75.1665,"summary":"A revered Shiva temple near the Ellora Caves."},
    {"id":"lonar-crater-lake","name":"Lonar Crater Lake","city":"Lonar","state":"Maharashtra","region":"Maharashtra","category":"Nature","icon":"🌋","lat":19.9757,"lng":76.5096,"summary":"A meteor-impact crater lake with unusual geology and ecology."},

    # Other Indian destinations (35)
    {"id":"taj-mahal","name":"Taj Mahal","city":"Agra","state":"Uttar Pradesh","region":"Other India","category":"Heritage","icon":"🏛️","lat":27.1751,"lng":78.0421,"summary":"A world-famous marble mausoleum and UNESCO World Heritage Site."},
    {"id":"red-fort","name":"Red Fort","city":"Delhi","state":"Delhi","region":"Other India","category":"Heritage","icon":"🏰","lat":28.6562,"lng":77.2410,"summary":"A historic Mughal fort in Old Delhi."},
    {"id":"qutub-minar","name":"Qutub Minar","city":"Delhi","state":"Delhi","region":"Other India","category":"Heritage","icon":"🗼","lat":28.5245,"lng":77.1855,"summary":"A towering medieval minaret in the Qutb complex."},
    {"id":"india-gate","name":"India Gate","city":"Delhi","state":"Delhi","region":"Other India","category":"Heritage","icon":"🏛️","lat":28.6129,"lng":77.2295,"summary":"A prominent war memorial and landmark in New Delhi."},
    {"id":"amber-fort","name":"Amber Fort","city":"Jaipur","state":"Rajasthan","region":"Other India","category":"Heritage","icon":"🏰","lat":26.9855,"lng":75.8513,"summary":"A hilltop fort with ornate courtyards and palace architecture."},
    {"id":"hawa-mahal","name":"Hawa Mahal","city":"Jaipur","state":"Rajasthan","region":"Other India","category":"Heritage","icon":"🏛️","lat":26.9239,"lng":75.8267,"summary":"Jaipur's iconic Palace of Winds with its detailed facade."},
    {"id":"city-palace-udaipur","name":"City Palace","city":"Udaipur","state":"Rajasthan","region":"Other India","category":"Heritage","icon":"🏰","lat":24.5764,"lng":73.6835,"summary":"A grand palace complex overlooking Lake Pichola."},
    {"id":"jaisalmer-fort","name":"Jaisalmer Fort","city":"Jaisalmer","state":"Rajasthan","region":"Other India","category":"Heritage","icon":"🏰","lat":26.9124,"lng":70.9126,"summary":"A living sandstone fort rising above the Thar Desert city."},
    {"id":"golden-temple","name":"Golden Temple","city":"Amritsar","state":"Punjab","region":"Other India","category":"Spiritual","icon":"🛕","lat":31.6200,"lng":74.8765,"summary":"The revered Sikh shrine also known as Harmandir Sahib."},
    {"id":"dashashwamedh-ghat","name":"Dashashwamedh Ghat","city":"Varanasi","state":"Uttar Pradesh","region":"Other India","category":"Spiritual","icon":"🪔","lat":25.3065,"lng":83.0104,"summary":"A well-known Ganges riverfront ghat in Varanasi."},
    {"id":"fatehpur-sikri","name":"Fatehpur Sikri","city":"Fatehpur Sikri","state":"Uttar Pradesh","region":"Other India","category":"Heritage","icon":"🏛️","lat":27.0945,"lng":77.6679,"summary":"A historic Mughal city with monumental sandstone buildings."},
    {"id":"khajuraho-temples","name":"Khajuraho Temples","city":"Khajuraho","state":"Madhya Pradesh","region":"Other India","category":"Heritage","icon":"🛕","lat":24.8318,"lng":79.9199,"summary":"Temples celebrated for their detailed stone sculptures."},
    {"id":"sanchi-stupa","name":"Sanchi Stupa","city":"Sanchi","state":"Madhya Pradesh","region":"Other India","category":"Heritage","icon":"☸️","lat":23.4793,"lng":77.7397,"summary":"An ancient Buddhist monument and important pilgrimage site."},
    {"id":"konark-sun-temple","name":"Konark Sun Temple","city":"Konark","state":"Odisha","region":"Other India","category":"Heritage","icon":"🛕","lat":19.8876,"lng":86.0945,"summary":"A stone temple designed in the form of the Sun God's chariot."},
    {"id":"jagannath-temple","name":"Jagannath Temple","city":"Puri","state":"Odisha","region":"Other India","category":"Spiritual","icon":"🛕","lat":19.8048,"lng":85.8180,"summary":"A major Hindu pilgrimage temple in Puri."},
    {"id":"tiger-hill","name":"Tiger Hill","city":"Darjeeling","state":"West Bengal","region":"Other India","category":"Nature","icon":"🌄","lat":27.0120,"lng":88.2534,"summary":"A famous sunrise viewpoint with Himalayan panoramas on clear days."},
    {"id":"mg-marg-gangtok","name":"MG Marg","city":"Gangtok","state":"Sikkim","region":"Other India","category":"City & Culture","icon":"🚶","lat":27.3314,"lng":88.6138,"summary":"A pedestrian-friendly central promenade in Gangtok."},
    {"id":"kaziranga-national-park","name":"Kaziranga National Park","city":"Kohora","state":"Assam","region":"Other India","category":"Nature","icon":"🦏","lat":26.5775,"lng":93.1711,"summary":"A protected landscape known for its greater one-horned rhinoceroses."},
    {"id":"elephant-falls","name":"Elephant Falls","city":"Shillong","state":"Meghalaya","region":"Other India","category":"Nature","icon":"💧","lat":25.5374,"lng":91.8427,"summary":"A multi-tier waterfall surrounded by lush greenery."},
    {"id":"charminar","name":"Charminar","city":"Hyderabad","state":"Telangana","region":"Other India","category":"Heritage","icon":"🏛️","lat":17.3616,"lng":78.4747,"summary":"A landmark monument and symbol of Hyderabad's old city."},
    {"id":"golconda-fort","name":"Golconda Fort","city":"Hyderabad","state":"Telangana","region":"Other India","category":"Heritage","icon":"🏰","lat":17.3833,"lng":78.4011,"summary":"A historic fort known for its architecture and acoustic design."},
    {"id":"hampi-virupaksha","name":"Virupaksha Temple, Hampi","city":"Hampi","state":"Karnataka","region":"Other India","category":"Heritage","icon":"🛕","lat":15.3350,"lng":76.4600,"summary":"A temple in the historic ruins of the Vijayanagara Empire."},
    {"id":"mysore-palace","name":"Mysore Palace","city":"Mysuru","state":"Karnataka","region":"Other India","category":"Heritage","icon":"🏰","lat":12.3052,"lng":76.6552,"summary":"An ornate royal palace and one of Mysuru's best-known landmarks."},
    {"id":"lalbagh","name":"Lalbagh Botanical Garden","city":"Bengaluru","state":"Karnataka","region":"Other India","category":"Nature","icon":"🌳","lat":12.9507,"lng":77.5848,"summary":"A historic botanical garden with a glasshouse and diverse plant life."},
    {"id":"fort-kochi","name":"Fort Kochi","city":"Kochi","state":"Kerala","region":"Other India","category":"Beach & Coast","icon":"⛵","lat":9.9658,"lng":76.2421,"summary":"A coastal neighbourhood with colonial-era streets and Chinese fishing nets."},
    {"id":"munnar-tea-gardens","name":"Munnar Tea Gardens","city":"Munnar","state":"Kerala","region":"Other India","category":"Nature","icon":"🍃","lat":10.0889,"lng":77.0595,"summary":"Rolling tea plantations and misty hills in the Western Ghats."},
    {"id":"alleppey-backwaters","name":"Alleppey Backwaters","city":"Alappuzha","state":"Kerala","region":"Other India","category":"Nature","icon":"🛶","lat":9.4981,"lng":76.3388,"summary":"A network of lagoons and canals known for houseboat journeys."},
    {"id":"kanyakumari","name":"Kanyakumari","city":"Kanyakumari","state":"Tamil Nadu","region":"Other India","category":"Beach & Coast","icon":"🌅","lat":8.0883,"lng":77.5385,"summary":"A coastal destination at India's southern tip, known for sea views."},
    {"id":"rameswaram-temple","name":"Ramanathaswamy Temple","city":"Rameswaram","state":"Tamil Nadu","region":"Other India","category":"Spiritual","icon":"🛕","lat":9.2881,"lng":79.3174,"summary":"A major pilgrimage temple known for its long corridors."},
    {"id":"meenakshi-temple","name":"Meenakshi Amman Temple","city":"Madurai","state":"Tamil Nadu","region":"Other India","category":"Spiritual","icon":"🛕","lat":9.9195,"lng":78.1193,"summary":"A historic temple complex known for its colourful gopurams."},
    {"id":"ooty-botanical-garden","name":"Government Botanical Garden","city":"Ooty","state":"Tamil Nadu","region":"Other India","category":"Nature","icon":"🌷","lat":11.4120,"lng":76.7067,"summary":"A landscaped garden in the Nilgiri hill station of Ooty."},
    {"id":"radhanagar-beach","name":"Radhanagar Beach","city":"Swaraj Dweep","state":"Andaman and Nicobar Islands","region":"Other India","category":"Beach & Coast","icon":"🏝️","lat":11.9830,"lng":92.9597,"summary":"A celebrated Andaman beach with pale sand and clear coastal water."},
    {"id":"pangong-tso","name":"Pangong Tso","city":"Leh district","state":"Ladakh","region":"Other India","category":"Nature","icon":"🏔️","lat":33.7595,"lng":78.6670,"summary":"A high-altitude Himalayan lake known for its changing blue tones."},
    {"id":"laxman-jhula","name":"Laxman Jhula Area","city":"Rishikesh","state":"Uttarakhand","region":"Other India","category":"Spiritual","icon":"🌉","lat":30.1239,"lng":78.3218,"summary":"A popular Ganges-side area surrounded by temples and ashrams."},
    {"id":"hidimba-devi-temple","name":"Hidimba Devi Temple","city":"Manali","state":"Himachal Pradesh","region":"Other India","category":"Spiritual","icon":"🛕","lat":32.2396,"lng":77.1887,"summary":"A distinctive wooden temple set among cedar forests in Manali."},
]


# Article titles are used to retrieve real photographs and additional reading from Wikipedia.
# The image/article source is linked on each card; image availability varies by article.
WIKI_TITLES = {
    "gateway-of-india": "Gateway of India",
    "elephanta-caves": "Elephanta Caves",
    "marine-drive": "Marine Drive, Mumbai",
    "siddhivinayak-temple": "Shree Siddhivinayak Ganapati Temple",
    "sanjay-gandhi-national-park": "Sanjay Gandhi National Park",
    "shaniwar-wada": "Shaniwar Wada",
    "aga-khan-palace": "Aga Khan Palace",
    "sinhagad-fort": "Sinhagad",
    "dagdusheth-temple": "Dagadusheth Halwai Ganapati Temple",
    "mahabaleshwar": "Mahabaleshwar",
    "panchgani": "Panchgani",
    "ajanta-caves": "Ajanta Caves",
    "ellora-caves": "Ellora Caves",
    "grishneshwar-temple": "Grishneshwar Temple",
    "lonar-crater-lake": "Lonar Lake",
    "taj-mahal": "Taj Mahal",
    "red-fort": "Red Fort",
    "qutub-minar": "Qutb Minar",
    "india-gate": "India Gate",
    "amber-fort": "Amber Fort",
    "hawa-mahal": "Hawa Mahal",
    "city-palace-udaipur": "City Palace, Udaipur",
    "jaisalmer-fort": "Jaisalmer Fort",
    "golden-temple": "Golden Temple, Amritsar",
    "dashashwamedh-ghat": "Dashashwamedh Ghat",
    "fatehpur-sikri": "Fatehpur Sikri",
    "khajuraho-temples": "Khajuraho Group of Monuments",
    "sanchi-stupa": "Sanchi Stupa",
    "konark-sun-temple": "Konark Sun Temple",
    "jagannath-temple": "Jagannath Temple, Puri",
    "tiger-hill": "Tiger Hill, Darjeeling",
    "mg-marg-gangtok": "MG Marg, Gangtok",
    "kaziranga-national-park": "Kaziranga National Park",
    "elephant-falls": "Elephant Falls",
    "charminar": "Charminar",
    "golconda-fort": "Golconda Fort",
    "hampi-virupaksha": "Virupaksha Temple, Hampi",
    "mysore-palace": "Mysore Palace",
    "lalbagh": "Lalbagh Botanical Garden",
    "fort-kochi": "Fort Kochi",
    "munnar-tea-gardens": "Munnar",
    "alleppey-backwaters": "Kerala backwaters",
    "kanyakumari": "Kanyakumari",
    "rameswaram-temple": "Ramanathaswamy Temple",
    "meenakshi-temple": "Meenakshi Amman Temple",
    "ooty-botanical-garden": "Government Botanical Garden, Ooty",
    "radhanagar-beach": "Radhanagar Beach",
    "pangong-tso": "Pangong Tso",
    "laxman-jhula": "Lakshman Jhula",
    "hidimba-devi-temple": "Hidimba Devi Temple",
}

PLACE_HIGHLIGHTS = {
    "gateway-of-india": ["Waterfront arch", "Arabian Sea views", "Colaba neighbourhood"],
    "elephanta-caves": ["Rock-cut cave temples", "Stone sculptures", "Ferry journey from Mumbai"],
    "marine-drive": ["Seafront promenade", "Coastal skyline", "Evening views"],
    "siddhivinayak-temple": ["Ganesha shrine", "Temple architecture", "Prabhadevi area"],
    "sanjay-gandhi-national-park": ["Kanheri Caves", "Forest trails", "Urban biodiversity"],
    "shaniwar-wada": ["Peshwa-era history", "Fortified gateway", "Historic courtyards"],
    "aga-khan-palace": ["Freedom movement history", "Palace architecture", "Memorial grounds"],
    "sinhagad-fort": ["Hilltop fort remains", "Sahyadri views", "Trekking routes"],
    "dagdusheth-temple": ["Ganesha shrine", "Festival decorations", "Pune old city"],
    "mahabaleshwar": ["Arthur's Seat area", "Venna Lake", "Strawberry farms in season"],
    "panchgani": ["Table Land plateau", "Sydney Point", "Valley scenery"],
    "ajanta-caves": ["Buddhist cave art", "Ancient murals", "Rock-cut architecture"],
    "ellora-caves": ["Kailasa Temple", "Buddhist caves", "Jain monuments"],
    "grishneshwar-temple": ["Shiva shrine", "Temple carvings", "Near Ellora Caves"],
    "lonar-crater-lake": ["Meteor-impact crater", "Distinctive lake ecosystem", "Geology and birdlife"],
    "taj-mahal": ["White marble mausoleum", "Charbagh gardens", "Yamuna-side setting"],
    "red-fort": ["Lahori Gate", "Mughal architecture", "Museum areas"],
    "qutub-minar": ["Minar tower", "Qutb complex", "Historic stone inscriptions"],
    "india-gate": ["War memorial", "Kartavya Path area", "Central Delhi landmarks"],
    "amber-fort": ["Hilltop palace", "Sheesh Mahal", "Courtyards and gateways"],
    "hawa-mahal": ["Honeycomb facade", "Jharokha windows", "Pink City setting"],
    "city-palace-udaipur": ["Lake Pichola views", "Royal courtyards", "Museum collections"],
    "jaisalmer-fort": ["Golden sandstone walls", "Historic lanes", "Jain temples"],
    "golden-temple": ["Harmandir Sahib", "Amrit Sarovar", "Community langar"],
    "dashashwamedh-ghat": ["Ganga riverfront", "Evening Ganga Aarti", "Boat views"],
    "fatehpur-sikri": ["Buland Darwaza", "Palace complex", "Mughal-era architecture"],
    "khajuraho-temples": ["Temple sculptures", "Western Group", "Historic Nagara architecture"],
    "sanchi-stupa": ["Great Stupa", "Carved stone gateways", "Buddhist heritage"],
    "konark-sun-temple": ["Chariot-shaped temple", "Stone wheels", "Sculptural panels"],
    "jagannath-temple": ["Temple traditions", "Grand Road area", "Rath Yatra heritage"],
    "tiger-hill": ["Sunrise viewpoint", "Kanchenjunga views", "Himalayan panorama"],
    "mg-marg-gangtok": ["Pedestrian promenade", "Local cafes", "Town-centre shops"],
    "kaziranga-national-park": ["Wildlife safaris", "Grassland ecosystem", "One-horned rhinoceros habitat"],
    "elephant-falls": ["Tiered waterfall", "Forest setting", "Footpath viewpoints"],
    "charminar": ["Four minarets", "Old-city bazaars", "Laad Bazaar nearby"],
    "golconda-fort": ["Fort ramparts", "Acoustic design features", "Panoramic city views"],
    "hampi-virupaksha": ["Virupaksha Temple", "Hampi Bazaar area", "Vijayanagara ruins"],
    "mysore-palace": ["Royal interiors", "Palace architecture", "Palace grounds"],
    "lalbagh": ["Glass House", "Botanical collections", "Garden paths"],
    "fort-kochi": ["Chinese fishing nets", "Colonial-era streets", "Waterfront walks"],
    "munnar-tea-gardens": ["Tea estates", "Hill viewpoints", "Tea heritage"],
    "alleppey-backwaters": ["Backwater canals", "Houseboat journeys", "Paddy-field scenery"],
    "kanyakumari": ["Sea confluence views", "Vivekananda Rock area", "Sunrise and sunset viewpoints"],
    "rameswaram-temple": ["Long pillared corridors", "Temple tanks", "Pilgrimage architecture"],
    "meenakshi-temple": ["Colourful gopurams", "Temple halls", "Historic temple complex"],
    "ooty-botanical-garden": ["Botanical collections", "Landscaped gardens", "Nilgiri hill setting"],
    "radhanagar-beach": ["Sandy beach", "Coastal forest", "Sunset shoreline"],
    "pangong-tso": ["High-altitude lake", "Changing blue tones", "Himalayan scenery"],
    "laxman-jhula": ["Ganga riverside", "Temples and ashrams", "River-valley views"],
    "hidimba-devi-temple": ["Wooden pagoda-style temple", "Cedar forest", "Manali hill setting"],
}

PLACE_TIPS = {
    "gateway-of-india": "The waterfront can be busy. Combine this stop with Colaba and check ferry details separately if visiting Elephanta Caves.",
    "elephanta-caves": "The island is reached by ferry. Check the latest ferry schedule and cave access arrangements before travelling.",
    "marine-drive": "Visit around sunset for changing coastal light; weekends and evenings are often busy.",
    "siddhivinayak-temple": "Check current darshan timings and rules on the temple's official channels before travelling.",
    "sanjay-gandhi-national-park": "Check park entry, cave access and activity timings before you go; wear walking shoes.",
    "shaniwar-wada": "Allow time for the fort grounds and nearby old-Pune attractions; check current entry and event details.",
    "aga-khan-palace": "Allow time to read the historical exhibits and memorial information, not just view the building.",
    "sinhagad-fort": "Carry water and suitable footwear. Weather, road access and trail conditions can change quickly.",
    "dagdusheth-temple": "Expect crowds during festivals; confirm current temple guidelines and timings.",
    "mahabaleshwar": "Viewpoints may be misty during monsoon. Check local road and weather conditions before setting out.",
    "panchgani": "Viewpoints are weather-dependent; allow extra time for traffic during weekends and holiday seasons.",
    "ajanta-caves": "Plan several hours for the cave complex and check the latest weekly closure and ticket details before departure.",
    "ellora-caves": "The complex is spread across multiple caves; comfortable shoes and several hours help you explore it.",
    "grishneshwar-temple": "Dress respectfully and check current darshan rules; combine the visit with nearby Ellora if practical.",
    "lonar-crater-lake": "The crater landscape can involve walking on uneven ground; use marked access and avoid disturbing wildlife.",
    "taj-mahal": "Check the official ticketing page and weekly closure details. Entry rules may differ for the main mausoleum.",
    "red-fort": "Security checks can take time; check the current museum/entry arrangements and leave restricted items behind.",
    "qutub-minar": "Allow time for the wider archaeological complex rather than only the main tower.",
    "india-gate": "This is an outdoor public area; combine it with nearby central-Delhi sights and check traffic restrictions.",
    "amber-fort": "There are slopes and stairs around the complex; wear comfortable shoes and plan for warm weather.",
    "hawa-mahal": "The facade is especially photogenic from the street; nearby old-city markets can be crowded.",
    "city-palace-udaipur": "Allow extra time for the palace museums and lakefront surroundings; check ticket options in advance.",
    "jaisalmer-fort": "The fort is a living neighbourhood. Respect residents, keep noise down and avoid blocking narrow lanes.",
    "golden-temple": "Cover your head, remove footwear where required and follow the site's visitor guidance; the langar is community-run.",
    "dashashwamedh-ghat": "River steps can be slippery. Check local arrangements and safety guidance for boats and evening ceremonies.",
    "fatehpur-sikri": "The site is extensive and exposed to sun; carry water and check local transport and entry details.",
    "khajuraho-temples": "Give yourself time to explore more than one temple group; consider a licensed guide for architectural context.",
    "sanchi-stupa": "The monuments are outdoors on a historic site; comfortable shoes and sun protection are useful.",
    "konark-sun-temple": "Explore the carved stone details carefully and check current site access or conservation restrictions.",
    "jagannath-temple": "Access rules may vary for visitors. Confirm current entry guidance and festival crowd arrangements before going.",
    "tiger-hill": "Sunrise views depend on weather and visibility; leave early and bring warm layers.",
    "mg-marg-gangtok": "It is a pedestrian area. Check local weather and try nearby local food shops and cafes.",
    "kaziranga-national-park": "Safari zones and seasons vary. Book through authorised channels and follow wildlife-distance rules.",
    "elephant-falls": "Paths and steps can be slippery after rain; follow posted safety instructions around the waterfall.",
    "charminar": "The surrounding market streets can be congested; allow extra time and keep valuables secure in crowds.",
    "golconda-fort": "The complex has many steps and uneven surfaces; carry water and avoid the hottest part of the day.",
    "hampi-virupaksha": "Respect worship areas and local customs; many historic ruins in the wider Hampi area require additional travel time.",
    "mysore-palace": "Check current visitor hours and photography rules, which may vary between indoor and outdoor areas.",
    "lalbagh": "The garden is large; check entry gates, opening conditions and any special flower-show dates before visiting.",
    "fort-kochi": "The area is best explored on foot; carry sun protection and allow time for traffic around popular waterfront stops.",
    "munnar-tea-gardens": "Tea-estate access varies. Use authorised visitor sites and check local rain, fog and road conditions.",
    "alleppey-backwaters": "Confirm houseboat operator credentials, inclusions and boarding times before paying for a cruise.",
    "kanyakumari": "Sunrise and sunset views depend on cloud and sea conditions; check ferry operations if visiting offshore memorials.",
    "rameswaram-temple": "Follow the temple's current dress and ritual guidance; check bathing/entry arrangements before arrival.",
    "meenakshi-temple": "Confirm current darshan timings and photography restrictions; dress respectfully and plan for crowded periods.",
    "ooty-botanical-garden": "Hill weather can change quickly; bring a light layer and check garden entry conditions.",
    "radhanagar-beach": "Check sea conditions and lifeguard guidance; do not enter the water when warnings are displayed.",
    "pangong-tso": "This is a high-altitude destination. Allow time to acclimatise and confirm permits, road access and weather before travel.",
    "laxman-jhula": "Check the current status of bridge access and local crossing arrangements before planning a route around the river.",
    "hidimba-devi-temple": "The forest setting can be cool and damp; wear shoes suitable for uneven paths and respect temple customs.",
}


def recommended_season(place):
    pid, state, category = place["id"], place["state"], place["category"]
    if pid == "pangong-tso":
        return "Usually late May–September, depending on road access, permits and weather."
    if pid == "kaziranga-national-park":
        return "Often November–April; verify the current park and safari operating season."
    if pid == "radhanagar-beach":
        return "Often November–April; check ferry operations and sea conditions."
    if state in ("Rajasthan", "Delhi", "Uttar Pradesh", "Madhya Pradesh", "Odisha", "Punjab"):
        return "October–March is generally more comfortable for outdoor sightseeing."
    if state in ("Himachal Pradesh", "Uttarakhand", "Ladakh", "Sikkim", "West Bengal") and category == "Nature":
        return "Spring to autumn can work, but check local weather and road conditions before travel."
    if state in ("Kerala", "Tamil Nadu", "Karnataka", "Telangana", "Andaman and Nicobar Islands"):
        return "November–February is often comfortable; consider local rain, heat and sea conditions."
    if state in ("Assam", "Meghalaya"):
        return "October–April is often convenient; waterfall conditions and rain vary by season."
    if category == "Nature" and state == "Maharashtra":
        return "October–February is often comfortable; monsoon scenery can be lush but paths may be slippery."
    if state == "Maharashtra":
        return "October–February is often comfortable for sightseeing; check local event and weather updates."
    return "Seasonal conditions vary; check local weather, access and any official visitor notices before travelling."


def suggested_duration(place):
    pid, category = place["id"], place["category"]
    overrides = {
        "elephanta-caves": "Half day, including ferry travel",
        "sanjay-gandhi-national-park": "Half day or longer",
        "sinhagad-fort": "Half day",
        "ajanta-caves": "3–5 hours",
        "ellora-caves": "3–5 hours",
        "lonar-crater-lake": "Half day",
        "taj-mahal": "2–3 hours",
        "amber-fort": "2–4 hours",
        "city-palace-udaipur": "2–4 hours",
        "kaziranga-national-park": "Half day to a full day",
        "pangong-tso": "Full day or overnight trip from the region",
        "alleppey-backwaters": "Half day or overnight cruise",
        "hampi-virupaksha": "2–3 hours for the temple; longer for Hampi",
    }
    if pid in overrides:
        return overrides[pid]
    return {
        "Heritage": "About 2–3 hours",
        "Nature": "Half day, depending on activities",
        "Spiritual": "About 1–2 hours; longer on festival days",
        "Beach & Coast": "About 2–4 hours",
        "City & Culture": "About 2–3 hours",
    }.get(category, "Allow 2–3 hours, depending on your plans")


for place in PLACES:
    place["wiki_title"] = WIKI_TITLES.get(place["id"], place["name"])
    place["highlights"] = PLACE_HIGHLIGHTS.get(place["id"], [place["category"], place["city"], "Local sightseeing"])
    place["visitor_tip"] = PLACE_TIPS.get(place["id"], "Check local visitor guidance, access, weather and transport options before departure.")
    place["best_time"] = recommended_season(place)
    place["suggested_duration"] = suggested_duration(place)

@app.route("/")
def home():
    return render_template("index.html", places=PLACES, place_count=len(PLACES), maharashtra_count=sum(1 for place in PLACES if place["region"] == "Maharashtra"))

@app.route("/api/places")
def api_places():
    return jsonify(PLACES)

@app.route("/api/health")
def health():
    return jsonify({"status": "OK", "message": "Safar Smart Tourism is running", "places": len(PLACES)})

if __name__ == "__main__":
    app.run(debug=True)
