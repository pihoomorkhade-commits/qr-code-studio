const cameraStartButton = document.getElementById("start-camera");
const cameraStopButton = document.getElementById("stop-camera");
const cameraStatus = document.getElementById("camera-status");
const cameraResult = document.getElementById("camera-result");
const cameraText = document.getElementById("camera-text");

let qrScanner = null;
let cameraRunning = false;

cameraStartButton.addEventListener("click", async () => {
    if (cameraRunning) return;

    cameraStartButton.disabled = true;
    cameraStatus.textContent = "Starting camera...";

    try {
        if (typeof Html5Qrcode === "undefined") {
            throw new Error("Scanner library did not load. Check your internet connection.");
        }

        if (!qrScanner) {
            qrScanner = new Html5Qrcode("camera-view");
        }

        await qrScanner.start(
            { facingMode: "environment" },
            { fps: 10, qrbox: { width: 220, height: 220 } },
            (decodedText) => {
                cameraText.textContent = decodedText;
                cameraResult.hidden = false;
                cameraStatus.textContent = "QR code scanned successfully!";
                stopCamera();
            },
            () => {}
        );

        cameraRunning = true;
        cameraStopButton.disabled = false;
        cameraStatus.textContent = "Point your camera at a QR code.";

    } catch (error) {
        cameraStartButton.disabled = false;
        cameraStatus.textContent =
            "Could not start camera. Allow camera access and check your connection.";
        console.error(error);
    }
});

async function stopCamera() {
    if (qrScanner && cameraRunning) {
        try {
            await qrScanner.stop();
            qrScanner.clear();
        } catch (error) {
            console.error("Camera stop error:", error);
        }
    }

    cameraRunning = false;
    cameraStartButton.disabled = false;
    cameraStopButton.disabled = true;
}

cameraStopButton.addEventListener("click", stopCamera);