// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Event delegation for habit checkboxes
    document.body.addEventListener('change', function(event) {
        if (event.target.classList.contains('habit-checkbox')) {
            handleHabitCompletion(event.target);
        }
    });

    async function handleHabitCompletion(checkbox) {
        const listItem = checkbox.closest('.habit-item');
        const habitId = listItem.dataset.habitId;
        const isChecked = checkbox.checked;
        
        try {
            const response = await fetch(
                isChecked ? `/habit/complete-habit/${habitId}/` : `/habit/undo-complete-habit/${habitId}/`, 
                {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCSRFToken(),
                        'Content-Type': 'application/json',
                    },
                }
            );
            
            const data = await response.json();
            
            if (!data.success) {
                throw new Error(data.error || 'Failed to update habit');
            }
            
            updateUI(listItem, isChecked);
            
        } catch (error) {
            console.error('Error:', error);
            checkbox.checked = !isChecked; // Revert UI on failure
            showError('Failed to update habit. Please try again.');
        }
    }

    function getCSRFToken() {
        // Try to get CSRF token from cookie as fallback
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
            
        return cookieValue || document.querySelector('[name=csrfmiddlewaretoken]')?.value;
    }

    function updateUI(listItem, isChecked) {
        const incompleteList = document.getElementById('incomplete-habits');
        const completedList = document.getElementById('completed-habits');
        
        if (isChecked) {
            completedList.appendChild(listItem);
        } else {
            incompleteList.prepend(listItem);
        }
    }

    function showError(message) {
        // You can replace this with a proper notification system
        alert(message);
    }
});