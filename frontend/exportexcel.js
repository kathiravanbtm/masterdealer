function exportByGstin() {
  const gstin = document.getElementById("gstinInput").value.trim();
  if (!gstin) {
    alert("Enter GSTIN");
    return;
  }
  exportFilteredDealers({ gstin: gstin });
}

function exportByFilters() {
  const filters = {};
  const district = document.getElementById("filterDistrictInput").value.trim();
  const street = document.getElementById("filterStreetInput").value.trim();
  const pincode = document.getElementById("filterPincode").value.trim();
  const nagar = document.getElementById("filterNagarInput").value.trim();

  if (district) filters.district = district;
  if (street) filters.street = street;
  if (pincode) filters.pincode = pincode;
  if (nagar) filters.nagar = nagar;

  if (Object.keys(filters).length === 0) {
    alert("Please enter at least one filter.");
    return;
  }

  exportFilteredDealers(filters);
}

function exportOtherDistricts() {
  exportFilteredDealers({ exclude_district: "thiruvannamalai" });
}



async function exportFilteredDealers(filters) {
  try {
    const res = await fetch(`${API_BASE}/export/dealers`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(filters),
    });

    if (!res.ok) throw new Error("Export failed");

    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "filtered_dealers.xlsx";
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
  } catch (err) {
    console.error("Export error:", err);
    alert("Failed to export dealers");
  }
}
