const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const photoInput = document.getElementById('photo');
const captureButton = document.getElementById('captureButton');
const checkButton = document.getElementById('checkSkinType');
const resultsPopup = document.getElementById('resultsPopup');
const inlineLoader = document.getElementById('inlineLoader');  // This is the loader that will be displayed below the button

// Open camera and show the video stream
function openCamera() {
  if (navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true })
      .then(function (stream) {
        video.style.display = "block";
        video.srcObject = stream;
        captureButton.style.display = "block";
      })
      .catch(function (error) {
        alert("Camera access denied or unavailable.");
      });
  } else {
    alert("Your browser does not support camera access.");
  }
}

// Capture the image from the video stream
function captureImage() {
  const context = canvas.getContext('2d');
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  context.drawImage(video, 0, 0, canvas.width, canvas.height);

  canvas.toBlob(function(blob) {
    const file = new File([blob], "captured_image.jpg", { type: "image/jpeg" });
    const dataTransfer = new DataTransfer();
    dataTransfer.items.add(file);
    photoInput.files = dataTransfer.files;

    const stream = video.srcObject;
    const tracks = stream.getTracks();
    tracks.forEach(track => track.stop());

    video.style.display = "none";
    captureButton.style.display = "none";
  }, "image/jpeg", 1.0);
}

// Show popup results
function showResults(skinType, confidence, recommendations) {
  document.getElementById('skinType').innerText = skinType;
  document.getElementById('confidence').innerText = confidence.toFixed(2);
  const productList = document.getElementById('productList');
  productList.innerHTML = "";
  recommendations.forEach(item => {
    const li = document.createElement("li");
    li.textContent = item;
    productList.appendChild(li);
  });
  resultsPopup.style.display = "block";
}

// Close the results popup
function closePopup() {
  resultsPopup.style.display = "none";
}

// Function to upload image and get skin type
checkButton.onclick = async function() {
  const photo = photoInput.files[0];
  if (!photo) {
    alert("Please select or capture an image first.");
    return;
  }

  // Show the loader during analysis
  inlineLoader.style.display = "block"; // Show loader below the button

  const formData = new FormData();
  formData.append('file', photo);

  try {
    const response = await fetch('/check_skin_type', {
      method: 'POST',
      body: formData
    });

    if (response.ok) {
      const result = await response.json();
      showResults(result.skin_type, result.confidence, result.recommendations);
    } else {
      alert("Failed to analyze skin type. Please try again.");
    }
  } catch (error) {
    alert("Error analyzing skin type. Please try again.");
  } finally {
    inlineLoader.style.display = "none"; // Hide the loader after the process
  }
};

document.getElementById("checkSkinBtn").addEventListener("click", function () {
  // Show the loader
  inlineLoader.style.display = "block";

  // Simulate a process with a timeout
  setTimeout(() => {
    inlineLoader.style.display = "none"; // Hide the loader after the process
    alert("Skin check completed!"); // Replace this with your functionality
  }, 3000); // Adjust the time as needed
});

// Select the circle
const circle = document.querySelector('.circle');

// Function to handle mouse movement
function handleMouseMove(event) {
  const { clientX, clientY } = event;

  // Show the circle
  circle.style.display = 'block';

  // Position the circle at the cursor location
  circle.style.left = `${clientX}px`;
  circle.style.top = `${clientY}px`;
}

// Event listeners to handle mouse movements and visibility
document.addEventListener('mousemove', handleMouseMove);

document.addEventListener('mouseleave', () => {
  circle.style.display = 'none'; // Hide circle when cursor leaves the page
});

document.addEventListener('mouseenter', () => {
  circle.style.display = 'block'; // Show circle when cursor enters the page
});

//video hover play for wellness tips section 
function playVideo(element) {
  const video = element.querySelector('video');
  video.play();
}

function pauseVideo(element) {
  const video = element.querySelector('video');
  video.pause();
}
