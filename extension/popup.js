// popup.js - Chrome extension popup logic for screenshot capture and analysis

// Helper: convert dataURL to Blob
function dataURLtoBlob(dataUrl) {
  const arr = dataUrl.split(',');
  const mime = arr[0].match(/:(.*?);/)[1];
  const bstr = atob(arr[1]);
  let n = bstr.length;
  const u8arr = new Uint8Array(n);
  while (n--) {
    u8arr[n] = bstr.charCodeAt(n);
  }
  return new Blob([u8arr], { type: mime });
}

async function captureAndAnalyze() {
  const resultDiv = document.getElementById('result');
  resultDiv.textContent = 'Capturing screen…';

  // Capture visible tab
  chrome.tabs.captureVisibleTab(null, { format: 'png' }, async (dataUrl) => {
    if (chrome.runtime.lastError) {
      resultDiv.textContent = 'Capture error: ' + chrome.runtime.lastError.message;
      return;
    }

    try {
      const blob = dataURLtoBlob(dataUrl);
      const formData = new FormData();
      formData.append('file', blob, 'screenshot.png');

      resultDiv.textContent = 'Analyzing…';
      const res = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        body: formData
      });
      if (!res.ok) {
        throw new Error('Backend error: ' + res.statusText);
      }
      const data = await res.json();
      resultDiv.textContent = data.result || 'No result';
    } catch (err) {
      resultDiv.textContent = 'Error: ' + err.message;
    }
  });
}

document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('startBtn');
  btn.addEventListener('click', captureAndAnalyze);
});
