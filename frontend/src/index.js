import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App.jsx';
import reportWebVitals from './reportWebVitals';

// Create the root React DOM node from the #root element in public/index.html
const root = ReactDOM.createRoot(document.getElementById('root'));

// Render the App component inside React's StrictMode (dev-only warnings and checks)
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// Performance measurement hook (optional)
// To log metrics, pass a logging function to reportWebVitals (e.g., console.log)
// Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
