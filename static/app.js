// Minimalist Digital Ema frontend JS

document.addEventListener('DOMContentLoaded', () => {
  const emaWall = document.getElementById('ema-wall');
  const emaForm = document.getElementById('ema-form');

  // API base URL
  const API_BASE = '/api/emas/';

  // Fetch emas from backend
  async function fetchEmas() {
    try {
      const response = await fetch(`${API_BASE}?skip=0&limit=50`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const emas = await response.json();
      return emas;
    } catch (error) {
      console.error('Error fetching emas:', error);
      return [];
    }
  }

  // Submit new ema to backend
  async function submitEma(emaData) {
    try {
      const response = await fetch(API_BASE, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(emaData),
      });
      if (!response.ok) {
        const errorText = await response.text();
        console.error('Submission failed:', {
          status: response.status,
          statusText: response.statusText,
          errorText,
          sentData: emaData
        });
        
        // Handle content filtering errors
        if (response.status === 400) {
          try {
            const errorData = JSON.parse(errorText);
            throw new Error(errorData.detail || 'Message contains inappropriate content');
          } catch (e) {
            throw new Error('Message contains inappropriate content');
          }
        }
        
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const newEma = await response.json();
      return newEma;
    } catch (error) {
      console.error('Error submitting ema:', error);
      throw error;
    }
  }

  // Render ema cards
  function renderEmas(emas) {
    emaWall.innerHTML = '';
    if (!emas.length) {
      emaWall.innerHTML = '<p style="text-align:center;color:#aaa;">No wishes yet. Be the first!</p>';
      return;
    }
    emas.forEach(ema => {
      const card = document.createElement('div');
      card.className = 'ema-card';
      card.innerHTML = `
        <div class="ema-message">${escapeHTML(ema.message)}</div>
        <div class="ema-meta">
          <span>${ema.name ? escapeHTML(ema.name) : 'Anonymous'}</span>
          <span>${ema.type ? capitalize(ema.type) : ''}</span>
          <span>${formatDate(ema.created_at)}</span>
        </div>
      `;
      emaWall.appendChild(card);
    });
  }

  // Form submission (sidebar)
  emaForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(emaForm);
    const emaData = {
      name: formData.get('name').trim() || null,
      message: formData.get('message').trim(),
      type: formData.get('type') || null,
    };

    try {
      // Submit to backend
      await submitEma(emaData);
      
      // Refresh the ema wall
      const emas = await fetchEmas();
      renderEmas(emas);
      
      // Reset form
      emaForm.reset();
    } catch (error) {
      console.error('Failed to submit ema:', error);
      alert('Failed to submit your wish. Please try again.');
    }
  });

  // Helpers
  function escapeHTML(str) {
    return str.replace(/[&<>'"]/g, tag => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;'
    })[tag]);
  }
  function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
  }
  function formatDate(iso) {
    const d = new Date(iso);
    return d.toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
  }

  // Initial load
  async function initializeApp() {
    const emas = await fetchEmas();
    renderEmas(emas);
  }

  initializeApp();
});
