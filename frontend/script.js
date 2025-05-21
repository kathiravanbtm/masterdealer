const API_BASE = "http://localhost:5000/api";

async function checkHealth() {
  try {
    const res = await fetch(`${API_BASE}/health`);
    const data = await res.json();
    document.getElementById("status").innerText = `API Status: ${data.status}`;
  } catch {
    document.getElementById("status").innerText = "API is not reachable.";
  }
}

async function loadDealers() {
  const res = await fetch(`${API_BASE}/dealers`);
  const data = await res.json();
  const table = document.getElementById("dealer-table");
  table.innerHTML = "<tr><th>GSTIN</th><th>Trade Name</th><th>Mobile</th><th>Email</th><th>Taxpayer Type</th><th>Visited</th><th>Jurisdiction</th></tr>";
  data.forEach(row => {
    table.innerHTML += `<tr>
      <td>${row.gstin}</td>
      <td>${row.trade_name || '-'}</td>
      <td>${row.mobile || '-'}</td>
      <td>${row.email || '-'}</td>
      <td>${row.taxpayer_type || '-'}</td>
      <td>${row.visited ? 'Yes' : 'No'}</td>
      <td>${row.jurisdiction || '-'}</td>
    </tr>`;
  });
}

async function uploadCSV() {
  const fileInput = document.getElementById("csvFile");
  const file = fileInput.files[0];

  if (!file) {
    alert("Please select a CSV file first.");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch(`${API_BASE}/dealers/upload_csv`, {
      method: "POST",
      body: formData,
    });

    const result = await res.json();

    if (res.ok) {
      alert(result.message || "CSV uploaded successfully.");
    } else {
      alert(`Upload failed: ${result.error || "Unknown error"}`);
    }
  } catch (err) {
    console.error("Upload error:", err);
    alert("An error occurred while uploading the CSV.");
  }
}

function createInfoSection(title, data) {
  let html = `<h3>${title}</h3><table border="1">`;

  displayOrder.forEach(key => {
    if (key in data) {
      const label = key.replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase());
      html += `<tr><th>${label}</th><td>${data[key]}</td></tr>`;
    }
  });

  html += "</table><br>";
  return html;
}

const displayOrder = [
  "gstin",
  "status",
  "type_of_payee",
  "allocation",
  "jurisdiction",
  "commodity",
  "pincode",
  "bank_name",
  "bank_branch",
  "bank_email",
  "bank_address",
  "account_number",
  "account_name",
  "accountant_phone",
  "accountant_email",
  "raw_address"
];

  async function findDealer() {
    const gstin = document.getElementById("gstinInput").value.trim();
    const infoDiv = document.getElementById("dealer-info");
    infoDiv.innerHTML = ''; // clear previous

    if (!gstin) {
      alert("Please enter a GSTIN");
      return;
    }

    try {
      const res = await fetch(`${API_BASE}/dealers/${gstin}`);
      if (!res.ok) {
        infoDiv.innerHTML = `Error: ${res.status} ${res.statusText}`;
        return;
      }

      const dealer = await res.json();
      if (dealer.error) {
        infoDiv.innerHTML = dealer.error;
        return;
      }

      // Extract bank details and dealer info separately
      const { bank_details, ...dealerInfo } = dealer;

      let html = '';
      html += createInfoSection("Dealer Information", dealerInfo);
      if (bank_details && Object.keys(bank_details).length > 0) {
        html += createInfoSection("Bank Details", bank_details);
      } else {
        html += '<p>No bank details found.</p>';
      }

      infoDiv.innerHTML = html;

    } catch (err) {
      infoDiv.innerHTML = `Fetch error: ${err.message}`;
    }
  }
checkHealth();