function completeHabit(checkbox) {
    const listItem = checkbox.closest(".habit-item");
    const name = listItem.querySelector(".habit-name");
    const habitId = listItem.dataset.habitId;
    const isChecked = checkbox.checked;

    // Toggle completion based on checkbox state
    if (isChecked) {
        // Add strikethrough and dim text
        name.classList.add("line-through", "text-gray-400");

        // Move the item to the bottom of the list
        const list = document.getElementById("habit-list");
        list.removeChild(listItem);
        list.appendChild(listItem);

        // Send the request to the backend to mark the habit as completed
        fetch(`/habit/complete-habit/${habitId}/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value, // CSRF token for security
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                "habit_id": habitId,
                "date": new Date().toISOString().split('T')[0] // Send today's date
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log("Habit marked as completed:", data);
        })
        .catch(error => {
            console.error("Error marking habit as completed:", error);
        });
    } else {
        // Remove strikethrough and restore text style
        name.classList.remove("line-through", "text-gray-400");

        // Move the item back to its original position
        const list = document.getElementById("habit-list");
        list.prepend(listItem);

        // Send the request to the backend to undo the habit completion
        fetch(`/habit/undo-complete-habit/${habitId}/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value, // CSRF token for security
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                "habit_id": habitId,
                "date": new Date().toISOString().split('T')[0] // Send today's date
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log("Habit completion undone:", data);
        })
        .catch(error => {
            console.error("Error undoing habit completion:", error);
        });
    }
}
