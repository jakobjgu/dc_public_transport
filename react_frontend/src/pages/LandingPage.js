/**
 * LandingPage.js
 * ─────────────
 * Hero splash with translucent white box over a full-screen background image.
 * Explains app purpose and lets user pick "Entries" or "Exits".
 *
 * Props:
 *  - onSelect(dataset: "entries" | "exits")  → callback to parent to switch view
 */

import React from 'react';
import background from '../assets/hero-bg.png'; // put your image in src/assets/

export default function LandingPage({ onSelect }) {
  return (
    <div
      style={{
        height: '100vh',
        backgroundImage: `url(${background})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        padding: '1rem',
      }}
    >
      <div
        style={{
          backgroundColor: 'rgba(255,255,255,0.9)', // nearly opaque white
          borderRadius: '8px',
          padding: '2rem',
          maxWidth: '600px',
          textAlign: 'center',
        }}
      >
        <h1 style={{ fontSize: '2.5rem', marginBottom: '0.5rem', color: '#222' }}>
          Welcome to Insight Data LLC
        </h1>
        <p style={{ fontSize: '1.125rem', marginBottom: '1.5rem', color: '#444' }}>
        Explore aggregated entry and exit volumes across the DC Metro stations for May 2012.
        Select a dataset below to visualize the network flow.
        </p>
        <button
          onClick={() => onSelect('entries')}
          style={{
            marginRight: '1rem',
            padding: '0.75rem 1.5rem',
            fontSize: '1rem',
            borderRadius: '4px',
            border: 'none',
            cursor: 'pointer',
            background: '#0039A6',
            color: '#fff',
          }}
        >
          View Entries
        </button>
        <button
          onClick={() => onSelect('exits')}
          style={{
            padding: '0.75rem 1.5rem',
            fontSize: '1rem',
            borderRadius: '4px',
            border: 'none',
            cursor: 'pointer',
            background: '#DA291C',
            color: '#fff',
          }}
        >
          View Exits
        </button>
      </div>
    </div>
  );
}
