// src/App.js

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