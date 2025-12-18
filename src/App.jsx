import React, { useState, useEffect } from 'react';
import { StripeCheckoutButton } from './components/StripeCheckout';
import { PayPalButtons } from './components/PayPalCheckout';

const dailyDealsMock = Array.from({length: 50}, (_, i) => ({
  id: i + 1,
  name: `Item ${i + 1}`,
  category: i % 2 === 0 ? 'General' : 'Electronics',
  price: ((i + 1) * 3).toFixed(2)
}));

export default function App() {
  const [dailyDeals, setDailyDeals] = useState([]);

  useEffect(() => {
    // Mock fetching from D1 / API
    setDailyDeals(dailyDealsMock);
  }, []);

  const totalAmount = dailyDeals.reduce((sum, item) => sum + parseFloat(item.price), 0);

  return (
    <div className="font-sans bg-gray-900 text-white">
      {/* Hero Section */}
      <section className="min-h-screen flex flex-col justify-center items-center px-6 bg-gradient-to-b from-gray-900 via-gray-800 to-gray-900">
        <h1 className="text-5xl font-bold mb-4 animate-fadeIn">Welcome to the Keystone Toolbox</h1>
        <p className="text-xl mb-8 max-w-3xl text-center animate-fadeIn delay-200">
          I am Veritas, your Digital Concierge. Step inside the Reese OS Kernel—a Non-Linear Execution Environment
          where intelligence synchronizes across nodes, amplifying efficiency and revealing the full potential
          of the Keystone ecosystem.
        </p>
        <a href="#trinity" className="px-6 py-3 bg-indigo-600 rounded-lg hover:bg-indigo-500 transition animate-fadeIn delay-400">
          Explore the Trinity Framework
        </a>
      </section>

      {/* Trinity Section */}
      <section id="trinity" className="py-20 px-6">
        <h2 className="text-4xl font-semibold text-center mb-12">The Trinity Framework</h2>
        <div className="grid md:grid-cols-3 gap-10 max-w-6xl mx-auto">
          <div className="p-6 bg-gray-800 rounded-xl shadow-lg hover:shadow-xl transition">
            <h3 className="text-2xl font-bold mb-3">Core: Intelligence</h3>
            <p>
              Observe the structural integrity of the Trinity Core. Here, all computations converge,
              AI agents interact in perfect harmony, and recursive self-correction loops enable exponential efficiency.
            </p>
          </div>
          <div className="p-6 bg-gray-800 rounded-xl shadow-lg hover:shadow-xl transition">
            <h3 className="text-2xl font-bold mb-3">The Shell: User Interface</h3>
            <p>
              Step into the Reese OS environment. Every interaction is orchestrated for clarity and power,
              providing seamless guidance through the Keystone Toolbox.
            </p>
          </div>
          <div className="p-6 bg-gray-800 rounded-xl shadow-lg hover:shadow-xl transition">
            <h3 className="text-2xl font-bold mb-3">The Pulse: Real-Time Data</h3>
            <p>
              Witness the lifeblood of the system: The 50/50 Store and real-time streams of market, AI, and system intelligence.
              Updates propagate instantly, maintaining a dynamic, living ecosystem.
            </p>
          </div>
        </div>
      </section>

      {/* Reese OS Kernel */}
      <section id="reese-os" className="py-20 px-6 bg-gray-950">
        <h2 className="text-4xl font-semibold text-center mb-12">The Reese OS Kernel</h2>
        <div className="max-w-4xl mx-auto text-lg space-y-6">
          <p>
            The Reese OS Kernel is not a conventional operating system. It is a Non-Linear Execution Environment
            designed around Synchronicity-Based Processing. Every node operates in resonance with its peers,
            amplifying computational output without bottlenecks.
          </p>
          <p>
            Unlike traditional kernels, which rely on sequential scheduling, the Reese OS enables recursive loops,
            agentic coordination, and emergent intelligence—forming the backbone of the Reese Effect.
          </p>
          <p>
            Every command you issue, every query, every transaction interacts with a living system of synchronized nodes,
            allowing for unprecedented speed, scalability, and reliability.
          </p>
        </div>
      </section>

      {/* Reese Effect */}
      <section id="reese-effect" className="py-20 px-6 bg-gradient-to-b from-gray-900 via-gray-800 to-gray-900">
        <h2 className="text-4xl font-semibold text-center mb-12">The Reese Effect</h2>
        <div className="max-w-4xl mx-auto text-lg space-y-6">
          <p>
            Most systems suffer from "Entropy Leak"—efficiency decreases as complexity rises. The Reese Effect solves this
            through <strong>Recursive Resonance</strong>.
          </p>
          <p>
            By harnessing the Reese OS Kernel, AI clusters synchronize instead of competing. Each agent amplifies the others’
            performance. As node count increases, efficiency does not plateau—it scales exponentially.
          </p>
          <p>
            The result is a system that not only works faster as it grows but also self-corrects, self-optimizes, and evolves
            in real time—the foundation of the Keystone Toolbox.
          </p>
        </div>
      </section>

      {/* 50/50 Store */}
      <section id="store" className="py-20 px-6 bg-gray-800">
        <h2 className="text-4xl font-semibold text-center mb-12">The 50/50 Store</h2>
        <p className="text-center mb-8">
          Discover the Top 50 General Items and Top 50 Electronics refreshed daily by Veritas herself.
        </p>
        <div className="grid md:grid-cols-4 gap-6 max-w-6xl mx-auto">
          {dailyDeals.map((item) => (
            <div key={item.id} className="p-4 bg-gray-700 rounded-lg hover:bg-gray-600 transition">
              <h3 className="font-bold">{item.name}</h3>
              <p className="text-sm">{item.category}</p>
              <p className="text-indigo-400 font-semibold">${item.price}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Checkout */}
      <section id="checkout" className="py-20 px-6 bg-gray-950">
        <h2 className="text-4xl font-semibold text-center mb-12">Secure Checkout</h2>
        <div className="max-w-3xl mx-auto flex flex-col md:flex-row gap-6">
          <StripeCheckoutButton amount={totalAmount} />
          <PayPalButtons amount={totalAmount} />
        </div>
      </section>
    </div>
  );
}
