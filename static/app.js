// Minimalist Digital Ema frontend JS

document.addEventListener('DOMContentLoaded', () => {
  const emaWall = document.getElementById('ema-wall');
  const emaForm = document.getElementById('ema-form');

  // Placeholder data
  const placeholderEmas = [
    {
      id: 1,
      name: 'gurt',
      message: 'sybau',
      type: 'wish',
      created_at: '2024-06-01T10:00:00Z',
    },
    {
      id: 2,
      name: 'yo',
      message: 'presh',
      type: 'thanks',
      created_at: '2024-06-02T14:30:00Z',
    },
    {
      id: 3,
      name: 'gurt',
      message: 'yo',
      type: 'prayer',
      created_at: '2024-06-03T08:15:00Z',
    },
  ];

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
  emaForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const formData = new FormData(emaForm);
    const newEma = {
      id: Date.now(),
      name: formData.get('name').trim(),
      message: formData.get('message').trim(),
      type: formData.get('type'),
      created_at: new Date().toISOString(),
    };
    placeholderEmas.unshift(newEma);
    renderEmas(placeholderEmas);
    emaForm.reset();
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

  // Initial render
  renderEmas(placeholderEmas);
});
