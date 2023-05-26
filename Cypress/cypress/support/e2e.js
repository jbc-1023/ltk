import './commands'
require('cypress-xpath')

Cypress.on('uncaught:exception', (err) => {
    if (err.message.includes('ResizeObserver')) {
      // returning false here prevents Cypress from
      // failing the test
      return false;
    }
    return true;
  });

  // Hide fetch/XHR requests
const app = window.top;
if (!app.document.head.querySelector('[data-hide-command-log-request]')) {
  const style = app.document.createElement('style');
  style.innerHTML =
    '.command-name-request, .command-name-xhr { display: none }';
  style.setAttribute('data-hide-command-log-request', '');

  app.document.head.appendChild(style);
}