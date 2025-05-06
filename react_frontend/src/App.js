// src/App.js
import React, { useState, useEffect } from 'react';
import { ForceGraph2D } from 'react-force-graph';

function App() {
  const [graphData, setGraphData] = useState({ nodes: [], links: [] });

  useEffect(() => {
    fetch('http://localhost:5000/api/ridership')
      .then(res => res.json())
      .then(edges => {
        // Build nodes and links
        const nodes = {};
        edges.forEach(e => {
          nodes[e.from] = { id: e.from };
          nodes[e.to]   = { id: e.to   };
        });
        setGraphData({
          nodes: Object.values(nodes),
          links: edges.map(e => ({ source: e.from, target: e.to }))
        });
      });
  }, []);

  return (
    <div style={{ height: '100vh' }}>
      <ForceGraph2D
        graphData={graphData}
        nodeAutoColorBy="id"
        linkDirectionalArrowLength={3}
        linkDirectionalArrowRelPos={1}
      />
    </div>
  );
}

export default App;
