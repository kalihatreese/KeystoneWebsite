import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';

const industries = [
  {name: "Healthcare & Life Sciences", msg: "Automate compliance & predictive patient analytics."},
  {name: "Finance & Banking", msg: "Institutional-grade analytics with AI oversight."},
  {name: "Information Technology / Software", msg: "Full-stack AI orchestration for teams."},
  {name: "Retail & E-Commerce", msg: "Boost sales and optimize inventory."},
  {name: "Manufacturing / Industrial", msg: "Automate operations and predictive maintenance."},
  {name: "Energy / Utilities", msg: "Monitor grids and optimize energy usage."},
  {name: "Professional Services", msg: "Streamline operations and workflow automation."}
];

const handleCheckout = async () => {
  const res = await fetch('/api/create-checkout-session', { method: 'POST' });
  const data = await res.json();
  if(data.url) window.location.href = data.url;
};

const App = () => (
  <div className="p-8 font-sans">
    <h1 className="text-4xl font-bold text-center mb-6">Welcome to Keystone</h1>
    <p className="text-center mb-8">Veritas is your AI guide. See what ReeseOS, Trinity & ReeseEffect can do!</p>
    {industries.map((ind, idx) => (
      <div key={idx} className="border p-4 mb-4 rounded shadow hover:bg-gray-100">
        <h2 className="text-2xl font-semibold">{ind.name}</h2>
        <p className="mt-2">{ind.msg}</p>
      </div>
    ))}
    <div className="text-center mt-8">
      <button className="bg-green-600 text-white px-6 py-3 rounded hover:bg-green-700" onClick={handleCheckout}>
        Build & Buy Now
      </button>
    </div>
  </div>
);

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
