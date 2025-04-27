$(document).ready(function() {

    $("#comment-form").on("submit", function (e) {
        e.preventDefault();
        const text = $("#comment-text").val();
        const taskId = $("#task-id").val();

        $.ajax({
            url: `/tasks/${taskId}/comment/create/`,
            method: "POST",
            data: {
                text: text,
                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
            },
            success: function(response) {
                if (response.success) {
                    const commentHtml = `
                        <div class="card mb-3" id="comment-${response.comment.id}">
                            <div class="card-body">
                                <div class="d-flex justify-content-between align-items-start">
                                    <div>
                                        <h6 class="card-subtitle mb-2 text-muted">
                                            ${response.comment.author}
                                            <small class="text-muted">${response.comment.created_at}</small>
                                        </h6>
                                        <p class="card-text comment-text">${response.comment.text}</p>
                                        <div class="comment-edit-form d-none">
                                            <textarea class="form-control mb-2" rows="3">${response.comment.text}</textarea>
                                            <button class="btn btn-sm btn-primary save-edit" data-comment-id="${response.comment.id}">Save</button>
                                            <button class="btn btn-sm btn-secondary cancel-edit" data-comment-id="${response.comment.id}">Cancel</button>
                                        </div>
                                    </div>
                                    <div class="btn-group">
                                        <button class="btn btn-sm btn-outline-primary edit-comment" data-comment-id="${response.comment.id}">
                                            <i class="fas fa-edit"></i>
                                        </button>
                                        <button class="btn btn-sm btn-outline-danger delete-comment" data-comment-id="${response.comment.id}">
                                            <i class="fas fa-trash"></i>
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;
                    $("#comments-list").prepend(commentHtml);
                    $("#comment-text").val("");
                }
            }
        });
    });


    $(document).on("click", ".edit-comment", function () {
        const commentId = $(this).data("comment-id");
        const $comment = $(`#comment-${commentId}`);
        $comment.find(".comment-text").addClass("d-none");
        $comment.find(".comment-edit-form").removeClass("d-none");
        $comment.find(".edit-comment").addClass("d-none");
    });

    $(document).on("click", ".cancel-edit", function () {
        const commentId = $(this).data("comment-id");
        const $comment = $(`#comment-${commentId}`);
        $comment.find(".comment-text").removeClass("d-none");
        $comment.find(".comment-edit-form").addClass("d-none");
        $comment.find(".edit-comment").removeClass("d-none");
    });

    $(document).on("click", ".save-edit", function () {
        const commentId = $(this).data("comment-id");
        const $comment = $(`#comment-${commentId}`);
        const newText = $comment.find(".comment-edit-form textarea").val();

        $.ajax({
            url: `/comment/${commentId}/update/`,
            method: 'POST',
            data: {
                text: newText,
                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
            },
            success: function(response) {
                if (response.success) {
                    $comment.find(".comment-text").text(response.comment.text).removeClass("d-none");
                    $comment.find(".comment-edit-form").addClass("d-none");
                    $comment.find(".edit-comment").removeClass("d-none");
                    

                    if (response.comment.updated_at) {
                        const $subtitle = $comment.find(".card-subtitle");
                        if (!$subtitle.find(".updated-at").length) {
                            $subtitle.append(` <small class="text-muted">(ред. ${response.comment.updated_at})</small>`);
                        }
                    }
                }
            }
        });
    });


    $(document).on("click", ".delete-comment", function () {
        const commentId = $(this).data("comment-id");
        if (confirm("Are you sure you want to delete this comment?")) {
            $.ajax({
                url: `/comment/${commentId}/delete/`,
                method: "POST",
                data: {
                    csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                },
                success: function(response) {
                    if (response.success) {
                        $(`#comment-${commentId}`).remove();
                    }
                }
            });
        }
    });
}); 