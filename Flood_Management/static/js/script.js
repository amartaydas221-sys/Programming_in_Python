const app = document.getElementById("app");
let notice = "";

const escapeHtml = (value) => String(value ?? "").replace(/[&<>"']/g, (char) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
}[char]));

async function api(path, options = {}) {
    const response = await fetch(`/api/${path}`, {
        ...options,
        headers: {
            ...(options.body ? { "Content-Type": "application/json" } : {}),
            ...options.headers,
        },
    });
    const result = await response.json();
    if (!response.ok) {
        throw new Error(result.error || "The request failed.");
    }
    return result;
}

function message() {
    if (!notice) return "";
    const result = `<p class="message success" role="status">${escapeHtml(notice)}</p>`;
    notice = "";
    return result;
}

function table(headers, rows, emptyMessage) {
    return `<div class="table-container"><table><thead><tr>${headers
        .map((header) => `<th>${header}</th>`).join("")}</tr></thead><tbody>${
        rows || `<tr><td colspan="${headers.length}">${emptyMessage}</td></tr>`
    }</tbody></table></div>`;
}

function stat(title, value) {
    return `<div class="card"><h3>${escapeHtml(title)}</h3><p class="number">${escapeHtml(value)}</p></div>`;
}

async function dashboard() {
    const summary = await api("dashboard");
    app.innerHTML = `${message()}<h2>Dashboard</h2>
        <section class="stats">
            ${stat("Registered Families", summary.family_count)}
            ${stat("People Affected", summary.people_count)}
            ${stat("Families Served", summary.served_count)}
            ${stat("Shelters", summary.shelter_count)}
            ${stat("Inventory Items", summary.inventory_count)}
            ${stat("Distributions", summary.distribution_count)}
        </section>`;
}

async function families() {
    const search = new URLSearchParams(location.hash.split("?")[1] || "").get("q") || "";
    const records = await api(`families?q=${encodeURIComponent(search)}`);
    const rows = records.map((family) => `<tr>
        <td>${escapeHtml(family.familyId)}</td><td>${escapeHtml(family.headName)}</td>
        <td>${escapeHtml(family.phone)}</td><td>${escapeHtml(family.district)}</td>
        <td>${escapeHtml(family.members)}</td><td>${escapeHtml(family.damageLevel)}</td>
        <td>${family.receivedRelief ? "Received" : "Waiting"}</td>
        <td><button class="danger" data-delete-family="${escapeHtml(family.familyId)}">Delete</button></td>
    </tr>`).join("");
    app.innerHTML = `${message()}<h2>Family Management</h2>
        <section class="card"><h3>Register Affected Family</h3>
            <form id="family-form">
                <label>Family ID<input name="familyId" required></label>
                <label>Head of Family<input name="headName" required></label>
                <label>Phone Number (11 digits)<input name="phone" type="tel" pattern="[0-9]{11}" maxlength="11" required></label>
                <label>District<input name="district" required></label>
                <label>Upazila<input name="upazila" required></label>
                <label>Village<input name="village" required></label>
                <label>Total Family Members<input name="members" type="number" min="1" required></label>
                <label>Children<input name="children" type="number" min="0" value="0" required></label>
                <label>Elderly Members<input name="elderly" type="number" min="0" value="0" required></label>
                <label>Members with Disabilities<input name="disabledMembers" type="number" min="0" value="0" required></label>
                <label>Damage Level<select name="damageLevel" required>
                    <option>Low</option><option>Medium</option><option>High</option><option>Extreme</option>
                </select></label>
                <label>Shelter Needed<select name="shelterNeeded" required>
                    <option value="yes">Yes</option><option value="no">No</option>
                </select></label>
                <button type="submit">Register Family</button>
            </form>
        </section>
        <section class="card"><h3>Registered Families</h3>
            <form id="family-search"><label>Search by ID, name, phone, or district
                <input name="q" value="${escapeHtml(search)}"></label><button>Search</button>
                <a href="#families">Show All</a>
            </form>
            ${table(["Family ID", "Head of Family", "Phone", "District", "Members", "Damage", "Relief Status", "Action"], rows, "No family records found.")}
        </section>`;
}

async function inventory() {
    const records = await api("inventory");
    const rows = records.map((item) => `<tr>
        <td>${escapeHtml(item.itemId)}</td><td>${escapeHtml(item.itemName)}</td>
        <td>${escapeHtml(item.quantity)}</td><td>${escapeHtml(item.unit)}</td>
        <td>${escapeHtml(item.minimumStock)}</td>
        <td>${item.quantity <= item.minimumStock ? '<span class="low-stock">Low Stock</span>' : '<span class="available">Available</span>'}</td>
        <td><form data-update-inventory="${escapeHtml(item.itemId)}">
            <label>Quantity<input name="quantity" type="number" min="0" value="${escapeHtml(item.quantity)}" required></label>
            <label>Minimum stock<input name="minimumStock" type="number" min="0" value="${escapeHtml(item.minimumStock)}" required></label>
            <button>Update</button>
        </form></td>
        <td><button class="danger" data-delete-inventory="${escapeHtml(item.itemId)}">Delete</button></td>
    </tr>`).join("");
    app.innerHTML = `${message()}<h2>Relief Inventory Management</h2>
        <section class="card"><h3>Add New Item</h3>
            <form id="inventory-form">
                <label>Item ID<input name="itemId" required></label>
                <label>Item Name<input name="itemName" required></label>
                <label>Quantity<input name="quantity" type="number" min="0" required></label>
                <label>Unit<input name="unit" required></label>
                <label>Minimum Stock Level<input name="minimumStock" type="number" min="0" required></label>
                <button type="submit">Add Item</button>
            </form>
        </section>
        <section class="card"><h3>Available Inventory</h3>
            ${table(["Item ID", "Name", "Quantity", "Unit", "Minimum Stock", "Status", "Update Stock", "Action"], rows, "No inventory items found.")}
        </section>`;
}

async function shelters() {
    const [records, familyRecords] = await Promise.all([api("shelters"), api("families")]);
    const rows = records.map((shelter) => `<tr>
        <td>${escapeHtml(shelter.shelterId)}</td><td>${escapeHtml(shelter.shelterName)}</td>
        <td>${escapeHtml(shelter.district)}</td><td>${escapeHtml(shelter.capacity)}</td>
        <td>${escapeHtml(shelter.currentOccupancy)}</td>
        <td>${escapeHtml(shelter.capacity - shelter.currentOccupancy)}</td>
        <td><form data-update-shelter="${escapeHtml(shelter.shelterId)}">
            <label>Name<input name="shelterName" value="${escapeHtml(shelter.shelterName)}" required></label>
            <label>District<input name="district" value="${escapeHtml(shelter.district)}" required></label>
            <label>Capacity<input name="capacity" type="number" min="${escapeHtml(shelter.currentOccupancy)}" value="${escapeHtml(shelter.capacity)}" required></label>
            <button>Update</button>
        </form></td>
        <td><button class="danger" data-delete-shelter="${escapeHtml(shelter.shelterId)}">Delete</button></td>
    </tr>`).join("");
    const familyRows = familyRecords.map((family) => `<tr>
        <td>${escapeHtml(family.familyId)}</td><td>${escapeHtml(family.headName)}</td>
        <td>${escapeHtml(family.district)}</td><td>${family.shelterNeeded ? "Yes" : "No"}</td>
    </tr>`).join("");
    app.innerHTML = `${message()}<h2>Shelter Management</h2>
        <section class="card"><h3>Add Shelter</h3>
            <form id="shelter-form">
                <label>Shelter ID<input name="shelterId" type="number" min="1" required></label>
                <label>Shelter Name<input name="shelterName" required></label>
                <label>District<input name="district" required></label>
                <label>Total Capacity<input name="capacity" type="number" min="0" required></label>
                <button type="submit">Add Shelter</button>
            </form>
        </section>
        <section class="card"><h3>Registered Shelters</h3>
            ${table(["ID", "Shelter", "District", "Capacity", "Occupancy", "Available Places", "Update", "Delete"], rows, "No shelters registered yet.")}
        </section>
        <section class="card"><h3>Registered Families</h3>
            ${table(["Family ID", "Family Head", "District", "Shelter Needed"], familyRows, "No families registered.")}
        </section>`;
}

async function distribution() {
    const [familyRecords, records] = await Promise.all([
        api("families"),
        api("distributions"),
    ]);
    const eligible = familyRecords.filter((family) => !family.receivedRelief);
    const options = eligible.map((family) => `<option value="${escapeHtml(family.familyId)}">
        ${escapeHtml(family.familyId)} - ${escapeHtml(family.headName)} - ${escapeHtml(family.damageLevel)} Damage
    </option>`).join("");
    const rows = records.map((record) => `<tr>
        <td>${escapeHtml(record.distributionId)}</td><td>${escapeHtml(record.date)}</td>
        <td>${escapeHtml(record.familyId)}</td><td>${escapeHtml(record.headName)}</td>
        <td>${escapeHtml(record.package)}</td>
        <td>${record.items.map((item) => `${escapeHtml(item.itemName)}: ${escapeHtml(item.quantity)} ${escapeHtml(item.unit)}`).join("<br>")}</td>
    </tr>`).join("");
    app.innerHTML = `${message()}<h2>Relief Distribution</h2>
        <section class="card"><h3>Distribute Relief Package</h3>
            <p>The system selects the relief package according to the family's recorded damage level.</p>
            <form id="distribution-form"><label>Select Eligible Family
                <select name="familyId" required><option value="">-- Select Family --</option>${options}</select>
            </label><button ${eligible.length ? "" : "disabled"}>Distribute Relief</button></form>
        </section>
        <section class="card"><h3>Distribution History</h3>
            ${table(["Distribution ID", "Date", "Family ID", "Family Head", "Package", "Items Distributed"], rows, "No distributions recorded yet.")}
        </section>`;
}

async function reports() {
    const [summary, inventoryRecords, distributionRecords, groups] = await Promise.all([
        api("dashboard"), api("inventory"), api("distributions"), api("reports"),
    ]);
    const districtRows = groups.by_district.map((entry) =>
        `<tr><td>${escapeHtml(entry.district)}</td><td>${escapeHtml(entry.count)}</td></tr>`).join("");
    const damageRows = groups.by_damage.map((entry) =>
        `<tr><td>${escapeHtml(entry.damage)}</td><td>${escapeHtml(entry.count)}</td></tr>`).join("");
    const inventoryRows = inventoryRecords.map((item) => `<tr>
        <td>${escapeHtml(item.itemName)}</td><td>${escapeHtml(item.quantity)}</td>
        <td>${escapeHtml(item.unit)}</td>
        <td>${item.quantity <= item.minimumStock ? "Low Stock" : "Available"}</td>
    </tr>`).join("");
    const historyRows = distributionRecords.map((record) => `<tr>
        <td>${escapeHtml(record.distributionId)}</td><td>${escapeHtml(record.date)}</td>
        <td>${escapeHtml(record.familyId)} - ${escapeHtml(record.headName)}</td>
        <td>${escapeHtml(record.package)}</td>
    </tr>`).join("");
    app.innerHTML = `${message()}<h2>Management Reports</h2>
        <section class="stats">
            ${stat("Total Families", summary.family_count)}
            ${stat("Families Served", summary.served_count)}
            ${stat("Total People Affected", summary.people_count)}
            ${stat("Total Shelters", summary.shelter_count)}
            ${stat("Inventory Items", summary.inventory_count)}
            ${stat("Total Distributions", summary.distribution_count)}
        </section>
        <section class="card"><h3>Families by District</h3>${table(["District", "Number of Families"], districtRows, "No district data available.")}</section>
        <section class="card"><h3>Families by Damage Level</h3>${table(["Damage Level", "Number of Families"], damageRows, "No damage data available.")}</section>
        <section class="card"><h3>Inventory Summary</h3>${table(["Item", "Quantity", "Unit", "Status"], inventoryRows, "No inventory records available.")}</section>
        <section class="card"><h3>Relief Distribution History</h3>${table(["ID", "Date", "Family", "Package"], historyRows, "No distribution history available.")}</section>`;
}

const pages = { dashboard, families, inventory, shelters, distribution, reports };

function formObject(form) {
    const values = Object.fromEntries(new FormData(form).entries());
    for (const key of ["members", "children", "elderly", "disabledMembers",
        "quantity", "minimumStock", "capacity", "shelterId"]) {
        if (key in values) values[key] = Number(values[key]);
    }
    return values;
}

async function handleSubmit(event) {
    const form = event.target;
    if (!(form instanceof HTMLFormElement)) return;
    event.preventDefault();
    try {
        if (form.id === "family-search") {
            location.hash = `families?q=${encodeURIComponent(new FormData(form).get("q"))}`;
            return;
        }
        if (form.id === "family-form") {
            await api("families", { method: "POST", body: JSON.stringify(formObject(form)) });
            notice = "Family registered successfully.";
        } else if (form.id === "inventory-form") {
            await api("inventory", { method: "POST", body: JSON.stringify(formObject(form)) });
            notice = "Inventory item added successfully.";
        } else if (form.id === "shelter-form") {
            await api("shelters", { method: "POST", body: JSON.stringify(formObject(form)) });
            notice = "Shelter added successfully.";
        } else if (form.id === "distribution-form") {
            await api("distributions", { method: "POST", body: JSON.stringify(formObject(form)) });
            notice = "Relief package distributed successfully.";
        } else if (form.matches("[data-update-inventory]")) {
            await api(`inventory/${encodeURIComponent(form.dataset.updateInventory)}`, {
                method: "PUT", body: JSON.stringify(formObject(form)),
            });
            notice = "Inventory updated successfully.";
        } else if (form.matches("[data-update-shelter]")) {
            await api(`shelters/${encodeURIComponent(form.dataset.updateShelter)}`, {
                method: "PUT", body: JSON.stringify(formObject(form)),
            });
            notice = "Shelter updated successfully.";
        }
        await render();
    } catch (error) {
        alert(error.message);
    }
}

async function handleClick(event) {
    const button = event.target.closest("button[data-delete-family], button[data-delete-inventory], button[data-delete-shelter]");
    if (!button) return;
    if (!confirm("Are you sure you want to delete this record?")) return;
    try {
        if (button.dataset.deleteFamily) {
            await api(`families/${encodeURIComponent(button.dataset.deleteFamily)}`, { method: "DELETE" });
        } else if (button.dataset.deleteInventory) {
            await api(`inventory/${encodeURIComponent(button.dataset.deleteInventory)}`, { method: "DELETE" });
        } else {
            await api(`shelters/${encodeURIComponent(button.dataset.deleteShelter)}`, { method: "DELETE" });
        }
        notice = "Record deleted successfully.";
        await render();
    } catch (error) {
        alert(error.message);
    }
}

async function render() {
    const pageName = location.hash.slice(1).split("?")[0] || "dashboard";
    const page = pages[pageName] || dashboard;
    try {
        await page();
    } catch (error) {
        app.innerHTML = `<section class="card message error"><h2>Unable to load this page</h2><p>${escapeHtml(error.message)}</p><p>Make sure XAMPP MySQL is running and restart the Python server.</p></section>`;
    }
}

app.addEventListener("submit", handleSubmit);
app.addEventListener("click", handleClick);
window.addEventListener("hashchange", render);
render();
