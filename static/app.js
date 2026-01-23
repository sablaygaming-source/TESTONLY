// Grab references to HTML elements we need to interact with
const form = document.getElementById('studentForm');
const tableBody = document.getElementById('tableBody');

const refreshButton1 = document.getElementById('refreshForm')


// =================================================
// FUNCTION 1: Load data from the backend and display it
// =================================================
//parameter bInit = True for initial load, Otherwise False not initial
async function loadTableData(bInit) {
    console.log("Attempting to load data from /api/BankTransaction...");
    try {
        let response
        if (bInit) {
            // Ask the backend for the data (GET request)
            response = await fetch('/api/BankTransaction');
            // Convert the response JSON ainto a JavaScript Array

            console.log("debug response " + response.ok)
            console.log("debug response.status" + response.status)
            console.log("debug response " + response)
            console.dir(response)
        } else {
            response = await fetch('/kabisoteako/me')

        }
        const vData = await response.json()

        // Clear existing table rows
        tableBody.innerHTML = '';

        // Loop through each student in the database array
        if (!vData.user || vData.user.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="6">No records loaded. Please click REFRESH.</td></tr>';
        }

        vData.user.forEach(Transaction => {
            // Create a new table row HTML string
            const row = `
                <tr>
                    <td>${Transaction.BankTransaction}</td >
                    <td>${Transaction.AccountId}</td >
                    <td>${Transaction.Code}</td >
                    <td>${Transaction.BankName}</td >                    
                    <td>${Transaction.Type}</td >
                    <td>${Transaction.Date}</td >
                    <td>${Transaction.ContactName}</td >
                    <td>${Transaction.ContactNo}</td >
                    <td>${Transaction.Currency}</td >
                    <td>${Transaction.Status}</td >
                </tr >
            `;

            // Add the new row to the table body
            tableBody.innerHTML += row;
        });
    } catch (error) {
        console.error("Error loading data:", error);
    }
}

// =================================================
// FUNCTION 2: Handle Form Submission (Add Student)
// =================================================
form.addEventListener('submit', async function (event) {

    console.log("\nDebug: Submitting new student data.");
    // Prevent the default browser behavior of reloading the page
    event.preventDefault();

    // 1. Get data from the HTML input boxes
    const formData = {
        "BankTransaction": document.getElementById("BankTransaction").value,
        "AccountId": '',
        "Code": document.getElementById("Code").value,
        "BankName": document.getElementById("BankName").value,
        "Type": document.getElementById("Type").value,
        "Date": '',
        "ContactName": document.getElementById("ContactName").value,
        "ContactNo": document.getElementById("ContactNo").value,
        "Currency": document.getElementById("Currency").value,
        "Status": document.getElementById("Status").value,
    };

    try {
        // 2. Send data to the backend (POST request)
        const response = await fetch("/api/BankTransaction", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            // Convert JS object to JSON string to send over the network
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            throw new Error(`Server returned status: ${response.status}`);
        }


        // 3. Clear the form inputs
        form.reset();

        // 4. Reload the table to show the new data
        loadTableData();

    } catch (error) {
        console.error("Error saving data:", error);
    }
});


refreshButton1.addEventListener('click', async function (event) {
    console.log("debug freshButton1.addEvernListerner")
    loadTableData(bInit = false);

})

//timer to show on screen
async function pollTimer() {
    setInterval(async () => {
        const response = await fetch('/api/timer123', { 'method': 'GET' });
        const data = await response.json();
        console.dir(data)
        console.dir(response)
        document.getElementById("display2").textContent = data.user.time;
    }, 1000);
}

//load the timer from server.py
fetch('/api/timer123/start', {
    'method': 'POST',
    'headers': { 'Content-Type': 'application/json' },
    'body': ''
})

pollTimer();

// Load the table data as soon as the page opens (will likely show "No records loaded" 
// until the user clicks the REFRESH button to load server memory).
//loadTableData(bInit = true);

console.log("\nbefore io in app.js ");
