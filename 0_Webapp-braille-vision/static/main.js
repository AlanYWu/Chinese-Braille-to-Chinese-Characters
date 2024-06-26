//========================================================================
// Drag and drop image handling
//========================================================================

var fileDrag = document.getElementById("file-drag");
var fileSelect = document.getElementById("file-upload");

// Add event listeners
fileDrag.addEventListener("dragover", fileDragHover, false);
fileDrag.addEventListener("dragleave", fileDragHover, false);
fileDrag.addEventListener("drop", fileSelectHandler, false);
fileSelect.addEventListener("change", fileSelectHandler, false);

function fileDragHover(e) {
  // prevent default behaviour
  e.preventDefault();
  e.stopPropagation();

  fileDrag.className = e.type === "dragover" ? "upload-box dragover" : "upload-box";
}

function fileSelectHandler(e) {
  // handle file selecting
  var files = e.target.files || e.dataTransfer.files;
  fileDragHover(e);
  for (var i = 0, f; (f = files[i]); i++) {
    previewFile(f);
  }
}

//========================================================================
// Web page elements for functions to use
//========================================================================

var imagePreview = document.getElementById("image-preview");
var imageDisplay = document.getElementById("image-display");
var uploadCaption = document.getElementById("upload-caption");
var predResult = document.getElementById("pred-result");
var predResultCNP = document.getElementById("pred-result-cnp");
var predResultENG = document.getElementById("pred-result-eng");
var loader = document.getElementById("loader");

//========================================================================
// Main button events
//========================================================================

function submitImage() {
  // action for the submit button
  console.log("submit");

  if (!imageDisplay.src || !imageDisplay.src.startsWith("data")) {
    window.alert("Please select an image before submit.");
    return;
  }
  
  loader.classList.remove("hidden");
  imageDisplay.classList.add("loading");

  // call the predict function of the backend
  predictImage(imageDisplay.src);
}

function clearImage() {
  // reset selected files
  fileSelect.value = "";

  // remove image sources and hide them
  imagePreview.src = "";
  imageDisplay.src = "";
  predResult.innerHTML = "";
  predResultCNP.innerHTML = "";
  predResultENG.innerHTML = "";

  hide(imagePreview);
  hide(imageDisplay);
  hide(loader);
  hide(predResult);
  hide(predResultCNP);
  hide(predResultENG);
  show(uploadCaption);

  imageDisplay.classList.remove("loading");
}
function previewFile_example() {
  var preview = document.querySelector('#preview');
  var file    = document.querySelector('#example-data-file').files[0];
  var reader  = new FileReader();

  reader.onloadend = function () {
    preview.src = reader.result;
  }

  if (file) {
    reader.readAsDataURL(file);
  } else {
    preview.src = "";
  }
}

document.getElementById('example-data-form').addEventListener('submit', function(e) {
  e.preventDefault();

  var formData = new FormData();
  formData.append('file', document.getElementById('example-data-file').files[0]);

  fetch('/submit_example', {
    method: 'POST',
    body: formData
  }).then(response => response.json()).then(data => {
    console.log(data);
  }).catch(error => {
    console.error(error);
  });
});

function previewFile(file) {
  // show the preview of the image
  console.log(file.name);
  var fileName = encodeURI(file.name);

  var reader = new FileReader();
  reader.readAsDataURL(file);
  reader.onloadend = () => {
    imagePreview.src = URL.createObjectURL(file);

    show(imagePreview);
    hide(uploadCaption);

    // reset
    predResult.innerHTML = "";
    predResultCNP.innerHTML = "";
    predResultENG.innerHTML = "";
    imageDisplay.classList.remove("loading");

    displayImage(reader.result, "image-display");
  };
}

//========================================================================
// Helper functions
//========================================================================

function predictImage(image, retries = 3, timeout = 500000) { //我刚才还是肤浅了
  const controller = new AbortController();
  const signal = controller.signal;

  const fetchData = () => {
    fetch("/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(image),
      signal
    })
      .then(resp => {
        if (resp.ok) {
          return resp.json().then(data => {
            displayResult(data);
          });
        } else {
          return resp.json().then(errData => {
            throw new Error(`Server error: ${resp.status} - ${errData.message}`);
          });
        }
      })
      .catch(err => {
        if (retries > 0) {
          console.log(`Retrying... attempts left: ${retries - 1}`);
          setTimeout(() => fetchData(), 1000); // Retry after 1 second
        } else {
          console.log("An error occurred", err.message);
          window.alert("Oops! Something went wrong. Please try again later.");
        }
      });
  };
  const fetchTimeout = setTimeout(() => {
    controller.abort();
    window.alert("Request timed out. Please refresh this page or try again later.");
  }, timeout);

  fetchData();
}


// Henry 240321
function py_translate(text) {
  fetch("/py_translate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ "input": text }) // 将输入包装在对象中，以便与Flask后端对接
  })
    .then(resp => {
      if (resp.ok) {
        return resp.json(); // 解析JSON响应
      } else {
        throw new Error('Server response was not OK.');
      }
    })
    .then(data => {
      // 将返回的结果放在id为"result"的div中
      document.getElementById("result").textContent = data.result;
    })
    .catch(err => {
      console.log("An error occurred:", err.message);
      window.alert("Oops! Something went wrong.");
    });
}


function displayImage(image, id) {
  // display image on given id <img> element
  let display = document.getElementById(id);
  display.src = image;
  show(display);
}

function displayResult(data) {
  // display the result
  hide(imagePreview);
  hide(imageDisplay);

  hide(loader);
  predResult.innerHTML = data.result;
  show(predResult);
  //predResultCNP.innerHTML = data.CNP_Result;
  //show(predResultCNP);
  //predResultENG.innerHTML = data.ENG_Result;
  //show(predResultENG);

}
 
function hide(el) {
  // hide an element
  el.classList.add("hidden");
}

function show(el) {
  // show an element
  el.classList.remove("hidden");
}

function selectImage(imageSrc) {
  // Update the value of the hidden input field with the clicked image's source
  document.getElementById('selected-image').value = imageSrc;
}

