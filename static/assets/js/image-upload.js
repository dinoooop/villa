 $(document).ready(function () {
        let cropper;
        let modal = new bootstrap.Modal(document.getElementById("cropModal"));

        $(".img-upload-trigger").on("click", function (e) {
            e.preventDefault();
            $("#uploadImage").trigger("click");
        });

        // Open modal with selected image
        $("#uploadImage").on("change", function (e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (event) {
                    $("#imagePreview").attr("src", event.target.result);

                    modal.show();

                    $("#cropModal").on("shown.bs.modal", function () {
                        if (cropper) cropper.destroy();
                        cropper = new Cropper(document.getElementById("imagePreview"), {
                            aspectRatio: 1,
                            viewMode: 1,
                        });
                    }).on("hidden.bs.modal", function () {
                        if (cropper) {
                            cropper.destroy();
                            cropper = null;
                        }
                    });
                };
                reader.readAsDataURL(file);
            }
        });

        // Just crop and preview (don’t upload yet)
        $("#cropAndUpload").on("click", function () {
            if (!cropper) return;

            const canvas = cropper.getCroppedCanvas({
                width: 300,
                height: 300
            });

            // Preview cropped image
            $("#fileTopImagePreview").attr("src", canvas.toDataURL());

            // Store cropped image (base64) in hidden input
            $("#croppedImageInput").val(canvas.toDataURL("image/png"));

            modal.hide();
        });
    });
