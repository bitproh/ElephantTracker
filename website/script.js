// Simple page navigation
const pages = document.querySelectorAll('.page');
const initialPage = 'home';

function showPage(pageId) {
  pages.forEach(page => {
    if (page.id === pageId) {
      page.classList.add('active');
    } else {
      page.classList.remove('active');
    }
  });
  window.scrollTo(0, 0); // Scroll to top on page change
  if (pageId === 'tracking') {
    setTimeout(() => {
      map.invalidateSize();  // forces Leaflet to recalc and render
    }, 200);
  }
}

// Show initial page on load
document.addEventListener('DOMContentLoaded', () => {
  showPage(initialPage);
});

// ----------------------
// Google Maps Integration
// ----------------------

// Initialize map (centered on Kerala)
const map = L.map('map').setView([9.9312, 76.2673], 8);

// Add OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
}).addTo(map);

// Function to fetch detections from backend
async function loadEvents() {
  try {
    const res = await fetch('/api/events'); // Flask API endpoint
    const events = await res.json();

    // Clear old markers
    if (window.markers) {
      window.markers.forEach(m => map.removeLayer(m));
    }
    window.markers = [];

    // Add markers for each event
    events.forEach(ev => {
      const marker = L.marker([ev.lat, ev.lon]).addTo(map);
      marker.bindPopup(`
        <b>${ev.elephant_id}</b><br>
        Device: ${ev.device_id}<br>
        Time: ${ev.timestamp}
      `);
      window.markers.push(marker);
    });
  } catch (err) {
    console.error("Error loading events:", err);
  }
}

// Load initially and refresh every 5 sec
loadEvents();
setInterval(loadEvents, 5000);
