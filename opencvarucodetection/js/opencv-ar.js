let cvReady = false;
cv['onRuntimeInitialized'] = () => {
  console.log('OpenCV.js is ready!');
  cvReady = true;
};

const requiredMarkers = [0, 1, 2, 3]; 
const video = document.querySelector('video');
const trackEntity = document.getElementById('track');
const dPad = document.getElementById('dPad');
const stopButton = document.getElementById('stopButton');

let dictionary, parameters;

function initAruco() {
  dictionary = new cv.aruco.getPredefinedDictionary(cv.aruco.DICT_4X4_50);
  parameters = new cv.aruco.DetectorParameters();
}

function detectMarkers() {
  if (!cvReady || !video.readyState === 4) return null;

  const src = new cv.Mat(video.videoHeight, video.videoWidth, cv.CV_8UC4);
  const cap = new cv.VideoCapture(video);
  cap.read(src);

  let corners = new cv.MatVector();
  let ids = new cv.Mat();
  cv.aruco.detectMarkers(src, dictionary, corners, ids, parameters);

  let detectedIDs = [];
  if (!ids.empty()) {
    for (let i = 0; i < ids.rows; i++) {
      detectedIDs.push(ids.intAt(i, 0));
    }
  }

  src.delete();
  corners.delete();
  ids.delete();

  return detectedIDs;
}

function allMarkersDetected(detectedIDs) {
  return requiredMarkers.every(id => detectedIDs.includes(id));
}

function updateScene() {
  if (!cvReady) return;

  const detectedIDs = detectMarkers();
  if (!detectedIDs) return;

  if (allMarkersDetected(detectedIDs)) {
    trackEntity.setAttribute('visible', true);
    dPad.style.display = 'flex';
    stopButton.style.display = 'block';

    trackEntity.setAttribute('position', '0 0 -5');
    trackEntity.setAttribute('scale', '2 2 2');
  } else {
    trackEntity.setAttribute('visible', false);
    dPad.style.display = 'none';
    stopButton.style.display = 'none';
  }
}

function startDetectionLoop() {
  setInterval(updateScene, 150); 
}

window.addEventListener('load', () => {
  console.log('Window Loaded');
  initAruco();
  startDetectionLoop();
});
