document.addEventListener("DOMContentLoaded", function () {
    // Initialize Sortable for task cards
    const taskColumns = document.querySelectorAll(".status-column");
    taskColumns.forEach((column) => {
        new Sortable(column, {
            group: "tasks",
            animation: 150,
            ghostClass: "task-card dragging",
            onEnd: function (evt) {
                const taskId = evt.item.dataset.taskId;
                const newStatus = evt.to.dataset.status;
                
                $.ajax({
                    url: `/tasks/${taskId}/update_status/`,
                    method: "POST",
                    data: {
                        status: newStatus,
                    },
                    success: function (response) {
                        if (response.status === "success") {
                            showToast("Task status updated successfully", "success");
                        } else {
                            showToast("Error updating task status", "error");
                            // Revert the drag
                            evt.from.appendChild(evt.item);
                        }
                    },
                    error: function() {
                        showToast("Error updating task status", "error");
                        // Revert the drag
                        evt.from.appendChild(evt.item);
                    }
                });
            }
        });
    });

    // Handle task completion
    const completeButtons = document.querySelectorAll(".complete-task-btn");
    completeButtons.forEach((button) => {
        button.addEventListener("click", function (e) {
            e.preventDefault();
            const taskId = this.dataset.taskId;
            
            $.ajax({
                url: `/tasks/${taskId}/complete/`,
                method: "POST",
                success: function (response) {
                    if (response.status === "success") {
                        showToast("Task marked as completed", "success");
                        // Reload the task list
                        loadTasks();
                    } else {
                        showToast("Error completing task", "error");
                    }
                },
                error: function () {
                    showToast("Error completing task", "error");
                },
            });
        });
    });

    // Handle filter form submission
    const filterForm = document.querySelector(".filter-form");
    if (filterForm) {
        filterForm.addEventListener("submit", function (e) {
            e.preventDefault();
            loadTasks();
        });
    }

    // Function to load tasks via AJAX
    function loadTasks() {
        const formData = new FormData(filterForm);
        const params = new URLSearchParams(formData);
        
        $.ajax({
            url: window.location.pathname + "?" + params.toString(),
            method: "GET",
            success: function (response) {
                $("#taskList").html(response);
                initializeTaskCards();
            },
            error: function () {
                showToast("Error loading tasks", "error");
            },
        });
    }

    // Initialize task cards after loading
    function initializeTaskCards() {
        // Re-initialize Sortable
        const taskColumns = document.querySelectorAll(".status-column");
        taskColumns.forEach((column) => {
            new Sortable(column, {
                group: "tasks",
                animation: 150,
                ghostClass: "task-card dragging",
            });
        });

        // Re-initialize complete buttons
        const completeButtons = document.querySelectorAll(".complete-task-btn");
        completeButtons.forEach((button) => {
            button.addEventListener("click", function (e) {
                e.preventDefault();
                const taskId = this.dataset.taskId;
                completeTask(taskId);
            });
        });
    }

    // Show toast notification
    function showToast(message, type = "info") {
        const toastContainer = document.querySelector(".toast-container");
        if (!toastContainer) return;

        const toast = document.createElement("div");
        toast.className = `toast align-items-center text-white bg-${type} border-0`;
        toast.setAttribute("role", "alert");
        toast.setAttribute("aria-live", "assertive");
        toast.setAttribute("aria-atomic", "true");

        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        `;

        toastContainer.appendChild(toast);
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();

        toast.addEventListener("hidden.bs.toast", function () {
            toast.remove();
        });
    }
}); 