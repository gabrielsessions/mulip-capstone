document.getElementById("generateQRButton").onclick = async function() {
  const userId = "user123";  // Example user ID
  const response = await fetch("/generate_qr", {
      method: "POST",
      headers: {
          "Content-Type": "application/json"
      },
      body: JSON.stringify({ user_id: userId })
  });
  const blob = await response.blob();
  const qrContainer = document.getElementById("qrContainer");
  qrContainer.innerHTML = "";
  const img = document.createElement("img");
  img.src = URL.createObjectURL(blob);
  qrContainer.appendChild(img);
};

document.getElementById("verifyQRButton").onclick = async function() {
  const qrData = document.getElementById("qrInput").value;
  const userAgent = navigator.userAgent;
  const response = await fetch("/verify_qr", {
      method: "POST",
      headers: {
          "Content-Type": "application/json"
      },
      body: JSON.stringify({ token: qrData, user_agent: userAgent })
  });
  const result = await response.json();
  document.getElementById("result").textContent = JSON.stringify(result);
};
