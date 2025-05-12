/**
 * App.js
 * ──────
 * Top-level SPA component. 
 * Keeps `dataset` in state (null | "entries" | "exits") and
 * switches between:
 *  - LandingPage (dataset === null)
 *  - GraphPage   (dataset set)
 */

import React, { useState } from 'react';
import LandingPage from './pages/LandingPage';
import GraphPage   from './pages/GraphPage';

export default function App() {
  const [dataset, setDataset] = useState(null);

  return dataset === null ? (
    <LandingPage onSelect={setDataset} />
  ) : (
    <GraphPage dataset={dataset} onBack={() => setDataset(null)} />
  );
}