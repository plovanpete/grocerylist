// Function to fetch and render all groceries in the table
async function getAllGroceries() {
    const response = await fetch('/allgroceries/');
    const groceries = await response.json();

    const tableBody = document.getElementById('groceryList');
    tableBody.innerHTML = ''; // Clear previous data

    groceries.forEach(grocery => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${grocery._id}</td>
            <td>${grocery.title}</td>
            <td>${grocery.quantity}</td>
            <td>
                <button type="button" class="btn btn-info update-btn" data-id="${grocery._id}" data-target="#updateGroceryModal">Update</button>
                <button type="button" class="btn btn-danger delete-btn" onclick="deleteGrocery('${grocery._id}')">Delete</button>
            </td>
        `;
        tableBody.appendChild(row);
    });
}


// Function to handle adding a new grocery item
async function addGrocery(formData) {
    const response = await fetch('/groceries/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    });
    if (!response.ok) {
        const errorMessage = await response.text();
        alert(`Failed to add grocery item: ${errorMessage}`);
    } else {
        await getAllGroceries();
        $('#addGroceryModal').modal('hide');
    }
}

// Event listener for adding grocery form submission
document.getElementById('addGroceryForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const formData = {
        title: document.getElementById('title').value,
        quantity: parseInt(document.getElementById('quantity').value)
    };
    await addGrocery(formData);
});

// Function to handle updating an existing grocery item
async function updateGrocery() {
    const id = document.getElementById('updateId').value;
    const newTitle = document.getElementById('updateNewTitle').value;
    const newQuantity = document.getElementById('updateNewQuantity').value;

    // Check if any of the required fields is empty
    if (!id || (!newTitle && !newQuantity)) {
        alert("Please fill in the required fields!");
        return;
    }

    const response = await fetch(`/groceries/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            title: newTitle,
            quantity: newQuantity,
        }),
    });

    const result = await response.json();

    // Check if grocery is not found
    if (response.status === 404) {
        alert(`Grocery with ID '${id}' not found!`);
        return;
    }

    // If the update was successful, hide the modal and refresh the grocery list
    $('#updateGroceryModal').modal('hide');
    await getAllGroceries(); // Refresh grocery list
}

// Event listener for updating grocery form submission
document.getElementById('updateGroceryForm').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent default form submission behavior
    await updateGrocery(); // Call updateGrocery function
});

document.getElementById('groceryList').addEventListener('click', async function(event) {
    if (event.target.classList.contains('update-btn')) {
        const groceryId = event.target.getAttribute('data-id');
        const response = await fetch(`/groceries/${groceryId}`);
        const grocery = await response.json();

        // Populate the modal fields with the current data
        document.getElementById('updateId').value = grocery._id;
        document.getElementById('updateCurrentTitle').value = grocery.title;
        document.getElementById('updateCurrentQuantity').value = grocery.quantity;

        // Clear the new title and quantity fields
        document.getElementById('updateNewTitle').value = '';
        document.getElementById('updateNewQuantity').value = '';

        $('#updateGroceryModal').modal('show');
    }
});


// Function to handle deleting a grocery item
async function deleteGrocery(groceryId) {
    const response = await fetch(`/groceries/${groceryId}`, {
        method: 'DELETE'
    });

    if (!response.ok) {
        const errorMessage = await response.text();
        alert(`Failed to delete grocery item: ${errorMessage}`);
    } else {
        await getAllGroceries();
    }
}


// Fetch and render all groceries on page load
window.addEventListener('load', async function() {
    await getAllGroceries();
});

