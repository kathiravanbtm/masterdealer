function filterDealers() {
  // Collect filter inputs
  const district = document.getElementById("filterDistrictInput").value.trim();
  const nagar = document.getElementById("filterNagarInput").value.trim();
  const street = document.getElementById("filterStreetInput").value.trim();
  const pincode = document.getElementById("filterPincode").value.trim();

  // Prepare query parameters for non-empty filters
  const params = new URLSearchParams();
  if (district) params.append('district', district);
  if (nagar) params.append('nagar', nagar);
  if (street) params.append('street', street);
  if (pincode) params.append('pincode', pincode);

  if ([district, nagar, street, pincode].every(v => v === '')) {
    alert("Please enter at least one filter value.");
    return;
  }

  fetch(`${API_BASE}/dealers/filter?${params.toString()}`)
    .then(response => {
      if (!response.ok) {
        return response.text().then(text => {
          throw new Error(`Filter request failed: ${response.status} ${response.statusText} - ${text}`);
        });
      }
      return response.json();
    })
    .then(data => {
      populateDealerTable(data);
    })
    .catch(error => {
      console.error(error);
      alert("Error filtering dealers: " + error.message);
    });
}

function populateDealerTable(dealers) {
  const table = document.getElementById("dealer-tables");
  table.innerHTML = "";

  if (!dealers || dealers.length === 0) {
    table.innerHTML = "<tr><td>No dealers found.</td></tr>";
    return;
  }

  // Define custom order of fields
  const orderedFields = [
    "gstin",
    "trade_name",
    "mobile",
    "survey_no",
    "booth_no",
    "door_no",
    "floor",
    "street",
    "road",
    "nagar",
    "village",
    "taluk",
    "district",
    "pincode",
    "landmark",
    "jurisdiction"  // Make sure this field exists in your API response
  ];

  // Create table header row
  const headerRow = document.createElement("tr");
  orderedFields.forEach(field => {
    const th = document.createElement("th");
    th.textContent = field.replace(/_/g, ' ').toUpperCase(); // optional: format names
    headerRow.appendChild(th);
  });
  table.appendChild(headerRow);

  // Create data rows
  dealers.forEach(dealer => {
    const row = document.createElement("tr");
    orderedFields.forEach(field => {
      const td = document.createElement("td");
      td.textContent = dealer[field] !== undefined ? dealer[field] : "-";
      row.appendChild(td);
    });
    table.appendChild(row);
  });
}


async function otherdistricts() {
  try {
    const res = await fetch(`http://127.0.0.1:5000/api/districts/other`);
    if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
    const data = await res.json();
    const table = document.getElementById("other-districts-table");

    // Build table header
    table.innerHTML = `<tr>
      <th>GSTIN</th>
      <th>Trade Name</th>
      <th>District</th>
    </tr>`;

    // Populate table rows
    data.forEach(row => {
      table.innerHTML += `<tr>
        <td>${row.gstin || '-'}</td>
        <td>${row.trade_name || '-'}</td>
        <td>${row.district || '-'}</td>

      </tr>`;
    });

    if(data.length === 0) {
      table.innerHTML += `<tr><td colspan="3">No dealers found.</td></tr>`;
    }
  } catch (error) {
    console.error("Error loading dealers:", error);
    alert("Failed to load dealers. Check console for details.");
  }
}
