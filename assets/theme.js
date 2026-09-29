// Start the new visual direction in dark mode; retain subsequent user choices.
document.documentElement.dataset.theme = 'dark';
try {
  const theme = localStorage.getItem('portfolio-theme');
  if (theme === 'light' || theme === 'dark') document.documentElement.dataset.theme = theme;
} catch {}
