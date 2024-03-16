initialize();

async function initialize() {
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);
  const sessionId = urlParams.get('session_id');

  const response = await fetch(`https://8000-petergarvan-horizonmark-ofungvqkje6.ws-eu110.gitpod.io/session-status/?session_id=${sessionId}`);
  const session = await response.json();

  if (session.status == 'open') {
    window.replace('https://8000-petergarvan-horizonmark-ofungvqkje6.ws-eu110.gitpod.io')
  } else if (session.status == 'complete') {
    setTimeout(function() {
      window.location.href = 'https://8000-petergarvan-horizonmark-ofungvqkje6.ws-eu110.gitpod.io/';
    }, 5000);
  }
}