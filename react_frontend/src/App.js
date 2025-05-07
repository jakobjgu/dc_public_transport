import React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import GraphPage from './pages/GraphPage';

function App() {
  return (
    <BrowserRouter>
      <nav style={{ padding: '1em', background: '#f0f0f0' }}>
        <Link to="/graph/exits" style={{ marginRight: '1em' }}>Exits</Link>
        <Link to="/graph/entries">Entries</Link>
      </nav>
      <Routes>
        <Route path="/graph/:dataset" element={<GraphPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;


// todo:
// - explain the different react components?
// - use nginx and /or reverse proxy
// - improve UI layout (HTML?) -> buttons are ugly
// - check EC2 usage
// - Use different routes to serve different datasets
//   - use entrances as opposed to exits.
//   - edge-width to represent average trip lenghts from station to station.
//   - Or maybe better: selector dropdown to pick station in a static map -> highlight the originator stations that end in the station-of-interest
//   - Also different react frontends? Or Multipage dashboard?
// - Finalize github.io and deploy!