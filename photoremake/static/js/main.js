const alertBox = document.getElementById("alert-box");
const imageBox = document.getElementById("image-box");
const imageForm = document.getElementById("image-form");

const confirmBtn = document.getElementById("confirm-btn");
const input = document.getElementById("id_file");

const csrf = document.getElementsByClassName("csrfmiddlewaretoken");

let image;

console.log($("#title"));

// ver $image = $('#image');

input.addEventListener("change", () => {
  console.log("changed");
  const img_data = input.files[0];
  const url = URL.createObjectURL(img_data);
  imageBox.innerHTML = `<img src="${url}" id="image" width="500px" />`;
  //   image = document.getElementById("image");
});

confirmBtn.addEventListener("click", () => {
  const fd = new FormData();
  $.ajax({
    type: "POST",
    url: imageForm.action,
    enctype: "multipart/form-data",
    // data: fd,
    data: { csrfmiddlewaretoken: "{{ csrf_token }}" },
    success: function (response) {
      console.log(response);
    },
    error: function (error) {
      console.log(error);
    },
    cache: false,
    contentType: false,
    processData: false,
  });
});
