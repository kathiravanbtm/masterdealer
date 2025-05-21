const filterDistrictInput = document.getElementById("filterDistrictInput");
const districtSuggestions = document.getElementById("districtSuggestions");

filterDistrictInput.addEventListener("input", function () {
  const query = this.value.trim();
  if (query.length < 2) {
    districtSuggestions.innerHTML = "";
    return;
  }

  fetch(`${API_BASE}/suggestions/districts?q=${encodeURIComponent(query)}`)
    .then(response => response.json())
    .then(data => {
      districtSuggestions.innerHTML = "";
      data.forEach(district => {
        const suggestionItem = document.createElement("div");
        suggestionItem.textContent = district;
        suggestionItem.classList.add("autocomplete-item");
        suggestionItem.addEventListener("click", function () {
          filterDistrictInput.value = district;
          districtSuggestions.innerHTML = "";
        });
        districtSuggestions.appendChild(suggestionItem);
      });
    })
    .catch(error => {
      console.error("Error fetching suggestions:", error);
    });
});


const filterNagarInput = document.getElementById("filterNagarInput");
const nagarSuggestions = document.getElementById("nagarSuggestions");

filterNagarInput.addEventListener("input", function() {
  const query = this.value.trim();
  if (query.length < 2) {
    nagarSuggestions.innerHTML = "";
    return;
  }

  fetch(`${API_BASE}/suggestions/nagar?q=${encodeURIComponent(query)}`)
    .then(response => response.json())
    .then(data => {
      nagarSuggestions.innerHTML = "";
      data.forEach(nagar => {
        const item = document.createElement("div");
        item.textContent = nagar;
        item.classList.add("autocomplete-item");
        item.addEventListener("click", () => {
          filterNagarInput.value = nagar;
          nagarSuggestions.innerHTML = "";
        });
        nagarSuggestions.appendChild(item);
      });
    })
    .catch(console.error);
});


const filterStreetInput = document.getElementById("filterStreetInput");
const streetSuggestions = document.getElementById("streetSuggestions");

filterStreetInput.addEventListener("input", function() {
  const query = this.value.trim();
  if (query.length < 2) {
    streetSuggestions.innerHTML = "";
    return;
  }

  fetch(`${API_BASE}/suggestions/street?q=${encodeURIComponent(query)}`)
    .then(response => response.json())
    .then(data => {
      streetSuggestions.innerHTML = "";
      data.forEach(street => {
        const item = document.createElement("div");
        item.textContent = street;
        item.classList.add("autocomplete-item");
        item.addEventListener("click", () => {
          filterStreetInput.value = street;
          streetSuggestions.innerHTML = "";
        });
        streetSuggestions.appendChild(item);
      });
    })
    .catch(console.error);
});
