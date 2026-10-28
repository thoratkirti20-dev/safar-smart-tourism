(() => {
    "use strict";

    const byId = (id) => document.getElementById(id);
    const placeById = new Map(PLACES.map((place) => [place.id, place]));

    const searchInput = byId("searchInput");
    const clearSearch = byId("clearSearch");
    const regionFilter = byId("regionFilter");
    const categoryFilter = byId("categoryFilter");
    const placeCards = Array.from(document.querySelectorAll(".place-card"));
    const resultsCount = byId("resultsCount");
    const emptyState = byId("emptyState");
    const destinationSelect = byId("destinationSelect");
    const routeMessage = byId("routeMessage");
    const routeButton = byId("routeButton");
    const locateButton = byId("locateButton");
    const routeStats = byId("routeStats");
    const facilityDestination = byId("facilityDestination");
    const rapidoDestination = byId("rapidoDestination");

    // Search and filters for the full list of 50 places.
    function filterPlaces() {
        const query = searchInput.value.trim().toLowerCase();
        const region = regionFilter.value;
        const category = categoryFilter.value;
        let shown = 0;

        placeCards.forEach((card) => {
            const textMatches = !query || card.dataset.search.includes(query);
            const regionMatches = region === "all" || card.dataset.region === region;
            const categoryMatches = category === "all" || card.dataset.category === category;
            const visible = textMatches && regionMatches && categoryMatches;
            card.hidden = !visible;
            if (visible) shown += 1;
        });

        resultsCount.textContent = `Showing ${shown} of ${PLACES.length} destinations`;
        emptyState.hidden = shown !== 0;
    }

    // Load real place photographs and richer article summaries from Wikipedia.
    // Cards load as they approach the viewport, so 50 images are not requested at once.
    const wikiSummaryPromises = new Map();
    const photoObserver = ("IntersectionObserver" in window)
        ? new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) return;
                photoObserver.unobserve(entry.target);
                const place = placeById.get(entry.target.dataset.id);
                if (place) loadCardWikipediaContent(entry.target, place);
            });
        }, { rootMargin: "260px 0px" })
        : null;

    function wikipediaSummaryUrl(title) {
        const normalized = String(title || "").trim().replaceAll(" ", "_");
        return "https://en.wikipedia.org/api/rest_v1/page/summary/" + encodeURIComponent(normalized);
    }

    async function fetchSummaryForTitle(title) {
        if (!title) return null;
        try {
            const response = await fetch(wikipediaSummaryUrl(title));
            if (!response.ok) return null;
            const data = await response.json();
            if (data.type === "standard" && (data.extract || data.thumbnail || data.originalimage)) return data;
            return null;
        } catch (error) {
            return null;
        }
    }

    async function requestWikipediaSummary(place) {
        const direct = await fetchSummaryForTitle(place.wiki_title || place.name);
        if (direct) return direct;

        // If a page title differs from the common attraction name, discover the closest article.
        try {
            const query = encodeURIComponent(`${place.name} ${place.city} ${place.state}`);
            const response = await fetch(`https://en.wikipedia.org/w/rest.php/v1/search/page?q=${query}&limit=5`);
            if (!response.ok) return null;
            const data = await response.json();
            const pages = Array.isArray(data.pages) ? data.pages : [];
            const choice = pages.find((page) => page.thumbnail && page.key) || pages.find((page) => page.key);
            if (!choice) return null;
            return await fetchSummaryForTitle(choice.key);
        } catch (error) {
            return null;
        }
    }

    function getWikipediaSummary(place) {
        if (!wikiSummaryPromises.has(place.id)) {
            wikiSummaryPromises.set(place.id, requestWikipediaSummary(place));
        }
        return wikiSummaryPromises.get(place.id);
    }

    function getPhotoSource(summary) {
        const originalUrl = summary?.originalimage?.source || summary?.thumbnail?.source || "";
        const articleUrl = summary?.content_urls?.desktop?.page || `https://en.wikipedia.org/wiki/${encodeURIComponent((summary?.title || "").replaceAll(" ", "_"))}`;
        if (!originalUrl) return { url: articleUrl, label: "Wikipedia article and image source ↗" };
        try {
            const parsed = new URL(originalUrl);
            const isCommons = parsed.hostname.includes("wikimedia.org") && parsed.pathname.includes("/wikipedia/commons/");
            if (isCommons) {
                const fileName = decodeURIComponent(parsed.pathname.split("/").pop() || "");
                if (fileName) {
                    return {
                        url: `https://commons.wikimedia.org/wiki/File:${encodeURIComponent(fileName.replaceAll("_", " "))}`,
                        label: "Photo source & licence ↗"
                    };
                }
            }
        } catch (error) {
            // Fall back to the article page below.
        }
        return { url: articleUrl, label: "Photo source ↗" };
    }

    function applyCardWikipediaContent(card, place, summary) {
        if (!summary) {
            const placeholderText = card.querySelector(".photo-placeholder small");
            if (placeholderText) placeholderText.textContent = "Photo not available offline";
            return;
        }

        const description = card.querySelector(".place-summary");
        if (description && summary.extract) description.textContent = summary.extract;

        const image = card.querySelector(".place-photo");
        const frame = card.querySelector("[data-photo-frame]");
        const photoCredit = card.querySelector("[data-photo-credit]");
        const imageUrl = summary.thumbnail?.source || summary.originalimage?.source;

        if (photoCredit) {
            const source = getPhotoSource(summary);
            photoCredit.href = source.url;
            photoCredit.textContent = source.label;
            photoCredit.hidden = false;
        }

        if (image && imageUrl && !image.dataset.loaded) {
            image.addEventListener("load", () => {
                if (frame) frame.classList.add("has-photo");
                image.dataset.loaded = "true";
            }, { once: true });
            image.addEventListener("error", () => {
                const placeholderText = card.querySelector(".photo-placeholder small");
                if (placeholderText) placeholderText.textContent = "Photo unavailable";
            }, { once: true });
            image.src = imageUrl;
        }
    }

    async function loadCardWikipediaContent(card, place) {
        const summary = await getWikipediaSummary(place);
        applyCardWikipediaContent(card, place, summary);
    }

    if (photoObserver) {
        placeCards.forEach((card) => photoObserver.observe(card));
    } else {
        placeCards.forEach((card) => {
            const place = placeById.get(card.dataset.id);
            if (place) loadCardWikipediaContent(card, place);
        });
    }

    function setDetailImage(summary, place) {
        const image = byId("detailImage");
        const placeholder = byId("detailPhotoPlaceholder");
        const credit = byId("detailPhotoCredit");
        const imageUrl = summary?.originalimage?.source || summary?.thumbnail?.source;

        image.hidden = true;
        image.removeAttribute("src");
        placeholder.hidden = false;
        placeholder.querySelector("p").textContent = imageUrl ? "Loading photo…" : "No photo was supplied for this article.";
        credit.hidden = true;

        if (summary) {
            const source = getPhotoSource(summary);
            credit.href = source.url;
            credit.textContent = source.label;
            credit.hidden = false;
        }

        if (!imageUrl) return;
        image.alt = `Photograph of ${place.name}`;
        image.onload = () => {
            image.hidden = false;
            placeholder.hidden = true;
        };
        image.onerror = () => {
            placeholder.hidden = false;
            placeholder.querySelector("p").textContent = "The photo could not be loaded. Open the source article for available images.";
        };
        image.src = imageUrl;
    }

    function openPlaceDetails(placeId) {
        const place = placeById.get(placeId);
        if (!place) return;
        const dialog = byId("placeDialog");
        dialog.dataset.placeId = place.id;
        byId("detailCategory").textContent = `${place.category} · ${place.region}`;
        byId("detailTitle").textContent = place.name;
        byId("detailLocation").textContent = `${place.city}, ${place.state}, India`;
        byId("detailExtract").textContent = place.summary;
        byId("detailBestTime").textContent = place.best_time || "Check local weather and visitor notices.";
        byId("detailDuration").textContent = place.suggested_duration || "Allow time according to your plans.";
        byId("detailVisitorTip").textContent = place.visitor_tip || "Check current visitor guidance before travelling.";
        const highlights = byId("detailHighlights");
        highlights.replaceChildren();
        (place.highlights || []).forEach((highlight) => {
            const item = document.createElement("li");
            item.textContent = highlight;
            highlights.appendChild(item);
        });
        byId("detailWikiLink").href = `https://en.wikipedia.org/wiki/${encodeURIComponent((place.wiki_title || place.name).replaceAll(" ", "_"))}`;
        byId("detailMapLink").href = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(`${place.name}, ${place.city}, ${place.state}`)}`;
        setDetailImage(null, place);
        if (!dialog.open) dialog.showModal();

        getWikipediaSummary(place).then((summary) => {
            if (dialog.dataset.placeId !== place.id || !dialog.open) return;
            if (summary) {
                byId("detailExtract").textContent = summary.extract || place.summary;
                byId("detailWikiLink").href = summary.content_urls?.desktop?.page || byId("detailWikiLink").href;
                setDetailImage(summary, place);
            } else {
                byId("detailExtract").textContent = `${place.summary} More encyclopedic information and a photo may be unavailable while offline or if the source article has no suitable image.`;
            }
        });
    }

    document.querySelectorAll(".card-details").forEach((button) => {
        button.addEventListener("click", () => openPlaceDetails(button.dataset.placeId));
    });

    byId("closePlaceDialog").addEventListener("click", () => byId("placeDialog").close());
    byId("detailRouteButton").addEventListener("click", () => {
        const placeId = byId("placeDialog").dataset.placeId;
        byId("placeDialog").close();
        setDestination(placeId, true);
    });
    byId("placeDialog").addEventListener("click", (event) => {
        if (event.target === byId("placeDialog")) byId("placeDialog").close();
    });

    searchInput.addEventListener("input", filterPlaces);
    regionFilter.addEventListener("change", filterPlaces);
    categoryFilter.addEventListener("change", filterPlaces);
    clearSearch.addEventListener("click", () => {
        searchInput.value = "";
        filterPlaces();
        searchInput.focus();
    });

    // Map setup. The map requires the Leaflet CDN and internet access.
    const map = L.map("map", { scrollWheelZoom: false }).setView([22.8, 79.0], 4.5);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 19,
        attribution: "&copy; OpenStreetMap contributors"
    }).addTo(map);

    const markers = new Map();
    const markerGroup = L.featureGroup();

    PLACES.forEach((place) => {
        const marker = L.marker([place.lat, place.lng]);
        const popup = document.createElement("div");
        popup.innerHTML = `<div class="popup-title"></div><div class="popup-subtitle"></div><button class="popup-button" type="button">Plan a route</button>`;
        popup.querySelector(".popup-title").textContent = `${place.icon} ${place.name}`;
        popup.querySelector(".popup-subtitle").textContent = `${place.city}, ${place.state}`;
        popup.querySelector("button").addEventListener("click", () => setDestination(place.id, true));
        marker.bindPopup(popup);
        markers.set(place.id, marker);
        markerGroup.addLayer(marker);
    });
    markerGroup.addTo(map);

    // In cases where remote map tiles are slow, still show markers and controls.
    function updateSelectedDestination() {
        const place = placeById.get(destinationSelect.value);
        if (!place) return;

        facilityDestination.textContent = `${place.name}, ${place.city}, ${place.state}`;
        rapidoDestination.textContent = `${place.name}, ${place.city}, ${place.state}`;

        const queryLocation = `${place.name}, ${place.city}, ${place.state}`;
        const facilities = [
            { id: "hotelLink", type: "Hotels" },
            { id: "restaurantLink", type: "Restaurants" },
            { id: "hospitalLink", type: "Hospitals" },
            { id: "parkingLink", type: "Parking" }
        ];
        facilities.forEach((facility) => {
            const query = `${facility.type} near ${queryLocation}`;
            byId(facility.id).href = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(query)}`;
        });

        return place;
    }

    function setDestination(placeId, scrollToPlanner = false) {
        if (!placeById.has(placeId)) return;
        destinationSelect.value = placeId;
        const place = updateSelectedDestination();
        map.setView([place.lat, place.lng], 11);
        const marker = markers.get(place.id);
        if (marker) marker.openPopup();
        routeMessage.textContent = `Selected ${place.name}. Select “Show road route” to get directions from your current location.`;
        if (scrollToPlanner) byId("route-planner").scrollIntoView({ behavior: "smooth" });
    }
    window.setDestination = setDestination;

    destinationSelect.addEventListener("change", () => {
        setDestination(destinationSelect.value, false);
    });

    document.querySelectorAll(".card-route").forEach((button) => {
        button.addEventListener("click", () => setDestination(button.dataset.placeId, true));
    });

    // Current location and routing state.
    let userLocation = null;
    let userMarker = null;
    let routeLine = null;

    function getCurrentLocation() {
        return new Promise((resolve, reject) => {
            if (!navigator.geolocation) {
                reject(new Error("This browser does not support location services."));
                return;
            }
            navigator.geolocation.getCurrentPosition((position) => {
                userLocation = { lat: position.coords.latitude, lng: position.coords.longitude };
                if (userMarker) map.removeLayer(userMarker);
                userMarker = L.circleMarker([userLocation.lat, userLocation.lng], {
                    radius: 8, color: "#ffffff", weight: 3, fillColor: "#dd854b", fillOpacity: 1
                }).addTo(map).bindPopup("Your current location");
                userMarker.openPopup();
                map.setView([userLocation.lat, userLocation.lng], 11);
                resolve(userLocation);
            }, (error) => {
                if (error.code === 1) reject(new Error("Location access was denied. Allow location access in your browser and try again."));
                else if (error.code === 2) reject(new Error("Your location is unavailable. Check your device location settings."));
                else if (error.code === 3) reject(new Error("The location request timed out. Please try again."));
                else reject(new Error("Could not read your location. Please try again."));
            }, { enableHighAccuracy: true, timeout: 15000, maximumAge: 60000 });
        });
    }

    locateButton.addEventListener("click", async () => {
        locateButton.disabled = true;
        routeMessage.textContent = "Requesting your current location…";
        try {
            await getCurrentLocation();
            routeMessage.textContent = "Your location was found. Choose a destination and show the road route.";
        } catch (error) {
            routeMessage.textContent = error.message;
        } finally {
            locateButton.disabled = false;
        }
    });

    routeButton.addEventListener("click", async () => {
        const destination = updateSelectedDestination();
        if (!destination) return;
        routeButton.disabled = true;
        routeStats.hidden = true;
        routeMessage.textContent = "Finding a road route…";

        try {
            if (!userLocation) await getCurrentLocation();
            const coordinates = `${userLocation.lng},${userLocation.lat};${destination.lng},${destination.lat}`;
            const url = `https://router.project-osrm.org/route/v1/driving/${coordinates}?overview=full&geometries=geojson`;
            const response = await fetch(url);
            if (!response.ok) throw new Error("The road-routing service is temporarily unavailable. Please try again later.");
            const data = await response.json();
            if (data.code !== "Ok" || !data.routes || !data.routes.length) throw new Error("A driving route could not be found for this destination.");

            const route = data.routes[0];
            const points = route.geometry.coordinates.map(([lng, lat]) => [lat, lng]);
            if (routeLine) map.removeLayer(routeLine);
            routeLine = L.polyline(points, { color: "#176b52", weight: 5, opacity: 0.86 }).addTo(map);
            map.fitBounds(routeLine.getBounds(), { padding: [30, 30] });
            byId("routeDistance").textContent = `${(route.distance / 1000).toFixed(1)} km`;
            const totalMinutes = Math.round(route.duration / 60);
            const hours = Math.floor(totalMinutes / 60);
            const minutes = totalMinutes % 60;
            byId("routeDuration").textContent = hours ? `${hours} hr ${minutes} min` : `${minutes} min`;
            routeStats.hidden = false;
            routeMessage.textContent = `Route found to ${destination.name}. This is an estimate, not live traffic information.`;
        } catch (error) {
            routeMessage.textContent = error.message;
        } finally {
            routeButton.disabled = false;
        }
    });

    // Responsive navigation.
    const menuToggle = byId("menuToggle");
    const mainNav = byId("mainNav");
    menuToggle.addEventListener("click", () => {
        const isOpen = mainNav.classList.toggle("open");
        menuToggle.setAttribute("aria-expanded", String(isOpen));
    });
    mainNav.querySelectorAll("a").forEach((link) => link.addEventListener("click", () => {
        mainNav.classList.remove("open");
        menuToggle.setAttribute("aria-expanded", "false");
    }));

    // Start with all destination markers and the default selected place.
    byId("mapCount").textContent = `${PLACES.length} pins`;
    updateSelectedDestination();
    filterPlaces();
})();
