// ==========================================
// MOODSENSE CAMERA + EMOTION DETECTION
// ==========================================

document.addEventListener("DOMContentLoaded", function () {

    const video = document.getElementById("camera-video");
    const canvas = document.getElementById("camera-canvas");
    const captureButton = document.getElementById("capture-btn");
    const status = document.getElementById("camera-status");

    // Check required elements
    if (!video) {
        console.error("camera-video not found");
        return;
    }

    if (!canvas) {
        console.error("camera-canvas not found");
        return;
    }

    if (!captureButton) {
        console.error("capture-btn not found");
        return;
    }


    // ==========================================
    // START CAMERA
    // ==========================================

    navigator.mediaDevices.getUserMedia({
        video: true,
        audio: false
    })
    .then(function (stream) {

        video.srcObject = stream;

        video.play();

        if (status) {
            status.innerText = "Camera ready. Position your face clearly.";
        }

        captureButton.disabled = false;

        console.log("Camera started successfully");

    })
    .catch(function (error) {

        console.error("Camera Error:", error);

        if (status) {
            status.innerText =
                "Camera access denied. Please allow camera permission.";
        }

        captureButton.disabled = true;

    });


    // ==========================================
    // DETECT EMOTION BUTTON
    // ==========================================

    captureButton.addEventListener("click", async function () {

        console.log("Detect My Emotion button clicked");

        if (!video.srcObject) {

            alert("Camera is not started.");

            return;
        }


        // Disable button while detecting

        captureButton.disabled = true;

        captureButton.innerText =
            "Detecting Emotion...";


        if (status) {
            status.innerText =
                "Analyzing your facial expression...";
        }


        // ==========================================
        // CAPTURE CAMERA FRAME
        // ==========================================

        const context =
            canvas.getContext("2d");


        canvas.width =
            video.videoWidth;

        canvas.height =
            video.videoHeight;


        context.drawImage(
            video,
            0,
            0,
            canvas.width,
            canvas.height
        );


        // Convert image to Base64

        const imageData =
            canvas.toDataURL("image/jpeg", 0.85);


        // ==========================================
        // SEND IMAGE TO FLASK
        // ==========================================

        try {

            const response =
                await fetch("/detect", {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        image: imageData
                    })

                });


            const data =
                await response.json();


            console.log(
                "Detection Response:",
                data
            );


            // ==========================================
            // SUCCESS
            // ==========================================

            if (data.success) {

                if (status) {

                    status.innerText =
                        "Emotion detected: " +
                        data.emotion +
                        " (" +
                        Math.round(data.confidence) +
                        "%)";
                }


                // Redirect to result page

                window.location.href =
                    "/result?emotion=" +
                    encodeURIComponent(data.emotion) +
                    "&confidence=" +
                    encodeURIComponent(data.confidence);

            }


            // ==========================================
            // ERROR FROM BACKEND
            // ==========================================

            else {

                if (status) {
                    status.innerText =
                        data.message ||
                        "Unable to detect emotion.";
                }


                alert(
                    data.message ||
                    "Unable to detect emotion."
                );


                captureButton.disabled = false;

                captureButton.innerText =
                    "Detect My Emotion";

            }

        }

        catch (error) {

            console.error(
                "Detection Error:",
                error
            );


            if (status) {
                status.innerText =
                    "Connection error. Please try again.";
            }


            alert(
                "Cannot connect to the emotion detection server."
            );


            captureButton.disabled = false;

            captureButton.innerText =
                "Detect My Emotion";

        }

    });

});