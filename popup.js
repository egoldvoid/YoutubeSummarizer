document.getElementById('summarizeBtn').addEventListener('click', async () => {
    const videoUrl = await getCurrentTabUrl();
    const summary = await getSummary(videoUrl);
    document.getElementById('summary').innerText = summary;
  });
  
  async function getCurrentTabUrl() {
    let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    return tab.url;
  }
  
  async function getSummary(videoUrl) {
    const response = await fetch('http://127.0.0.1:5000/summarize', {  // Flask is running locally
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url: videoUrl }),
    });
  
    const data = await response.json();
    return data.summary || 'Error fetching summary';
  }
  