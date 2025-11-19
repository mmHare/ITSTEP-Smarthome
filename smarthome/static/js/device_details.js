document.addEventListener('DOMContentLoaded', function () {
    const selector = document.getElementById('logic_option');
    if (!selector) return; // safety check
    const formFields = document.getElementById('logic-form-fields');
    // 
    function updateFields() {
        const selected = selector.value;

        formFields.querySelectorAll('p').forEach(p => p.style.display = 'none'); // Hide everything first

        // Always show "active" if it exists
        // const activeField = formFields.querySelector('[name="active"]');
        // if (activeField) activeField.closest('p').style.display = 'block';
        const nameField = formFields.querySelector('[name="name"]');
        if (nameField) nameField.closest('p').style.display = 'block';

        if (selected === 'thermal') {
            ['numeric_min', 'numeric_max'].forEach(name => {
                const el = formFields.querySelector(`[name="${name}"]`);
                if (el) el.closest('p').style.display = 'block';
            });
        } else if (selected === 'time') {
            ['time_min', 'time_max'].forEach(name => {
                const el = formFields.querySelector(`[name="${name}"]`);
                if (el) el.closest('p').style.display = 'block';
            });
        }
    }

    // Run once on page load
    updateFields();
    // Run every time selection changes
    selector.addEventListener('change', updateFields);
});

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function toggleRuleActive(ruleId, isActive) {
    fetch(`/devices/logic/${ruleId}/toggle-active/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: JSON.stringify({ active: !!isActive })
    })
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                alert("Failed to update rule state: " + (data.error || 'unknown error'));
            }
        })
        .catch(error => {
            console.error('Error updating rule:', error);
            alert("Network error while updating rule state");
        });
}

function sendRuleAction(ruleId, pAction, pDict) {
    fetch(`/devices/logic/${ruleId}/rule-action/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ action: pAction, param_dict: pDict })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                if (data.action === 'delete') {
                    document.getElementById(`rule_${ruleId}`).closest('tr').remove();
                }
                else if (data.action === 'set_value') {
                    window.location.href = data.details_url;
                }
            } else {
                alert("Failed to act on rule: " + (data.error || 'unknown error'));
            }
        })
        .catch(error => {
            console.error('Error sending rule action:', error);
            alert("Network error while sending rule action");
        });
}

setInterval(() => {
    fetch("/devices/check_status/")
        .then(r => r.json())
        .then(data => {
            if (data.refresh_required) {
                window.location.reload();   // refresh page
            }
        });
}, 5000); // every 5 seconds