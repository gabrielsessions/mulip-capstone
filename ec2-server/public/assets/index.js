const socket = io('https://cozmokart.site', {
  transports: ['websocket'],
});

function sendAction(msg) {
  console.log(msg);
  socket.send(msg);
}


const joystick = document.getElementById('joystick');
const container = document.getElementById('joystick-container');
const output = document.getElementById('output');

const containerRect = container.getBoundingClientRect();
const radius = containerRect.width / 2;
const centerX = radius;
const centerY = radius;

let dragging = false;

let lastX = 0, lastY = 0;
let debounceTimer = null;
let lastLoggedX = null;
let lastLoggedY = null;

function scheduleJoystickLog(x, y) {
  if (debounceTimer) clearTimeout(debounceTimer);

  debounceTimer = setTimeout(() => {
    // Round to nearest 0.1 step
    const step = 0.1;
    const roundedX = Math.round(x / step) * step;
    const roundedY = Math.round(y / step) * step;

    const cleanX = +roundedX.toFixed(1);
    const cleanY = +roundedY.toFixed(1);

    // Only log if changed from last logged value
    if (cleanX !== lastLoggedX || cleanY !== lastLoggedY) {
      sendAction(`X: ${cleanX}, Y: ${cleanY}`)
      console.log(`Joystick HOLD -> X: ${cleanX}, Y: ${cleanY}`);
      lastLoggedX = cleanX;
      lastLoggedY = cleanY;
    }
  }, 1); // time (in ms) after motion stops before logging
}

function updateJoystickPosition(clientX, clientY) {
  const dx = clientX - containerRect.left - centerX;
  const dy = clientY - containerRect.top - centerY;

  const distance = Math.sqrt(dx * dx + dy * dy);
  const angle = Math.atan2(dy, dx);
  const maxDistance = radius - joystick.offsetWidth / 2;

  const limitedDistance = Math.min(distance, maxDistance);

  const x = limitedDistance * Math.cos(angle);
  const y = limitedDistance * Math.sin(angle);

  joystick.style.transform = `translate(calc(-50% + ${x}px), calc(-50% + ${y}px))`;

  const normX = +(x / maxDistance).toFixed(2);
  const normY = +(-y / maxDistance).toFixed(2);

  output.textContent = `X: ${normX}, Y: ${normY}`;

  // Update line position
  const line = document.getElementById('center-line');
  line.setAttribute('x2', centerX + x);
  line.setAttribute('y2', centerY + y);

  scheduleJoystickLog(normX, normY);
}

function resetJoystick() {
  joystick.style.transform = `translate(-50%, -50%)`;
  output.textContent = `X: 0, Y: 0`;

  const line = document.getElementById('center-line');
  line.setAttribute('x2', centerX);
  line.setAttribute('y2', centerY);

  // Immediately log reset to center
  sendAction(`X: 0.0, Y: 0.0`);
  console.log(`Joystick RESET -> X: 0.0, Y: 0.0`);
  lastLoggedX = 0;
  lastLoggedY = 0;

}

joystick.addEventListener('pointerdown', (e) => {
  dragging = true;
  joystick.setPointerCapture(e.pointerId);
});

joystick.addEventListener('pointermove', (e) => {
  if (!dragging) return;
  updateJoystickPosition(e.clientX, e.clientY);
});

joystick.addEventListener('pointerup', (e) => {
  dragging = false;
  resetJoystick();
});


