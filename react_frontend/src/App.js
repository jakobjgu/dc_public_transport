import React, { useState, useEffect, useRef, useMemo } from 'react';
import ForceGraph2D from 'react-force-graph-2d';
import { geoMercator } from 'd3-geo';

// define the line→color map
const lineColorMap = {
  red:    '#DA291C',
  blue:   '#0039A6',
  silver: '#A5ACAF',
  green:  '#00963F',
  yellow: '#F9E300',
  orange: '#ED8B00'
};

function App() {
  const [graphData, setGraphData] = useState({ nodes: [], links: [] });
  const width = window.innerWidth;
  const height = window.innerHeight;
  // Define default day‐type and trip‐time as state:
  const [selectedDayType,  setSelectedDayType]  = useState('weekday');
  const [selectedTripTime, setSelectedTripTime] = useState('AM Peak');
  const fgRef = useRef();

  // compute max volume and its log
  const maxVol = useMemo(() => 
    Math.max(1, ...graphData.nodes.map(n => n.volumes[selectedDayType]?.[selectedTripTime] || 0)),
    [graphData, selectedDayType, selectedTripTime]
  );
  const maxLog = useMemo(() => Math.log(maxVol + 1), [maxVol]);
  // define node sizing
  const minSize = 0.5;
  const maxSize = 15;
  const exponent = 10;
  
  const [zoomScale, setZoomScale] = useState(1);

  useEffect(() => {
    // fetch('/api/graph')
    fetch('http://3.85.243.81:5000/api/graph')
      .then(res => res.json())
      .then(({ nodes, links }) => {
        // 1. Build a Mercator projection fitting your data to the canvas
        const projection = geoMercator()
          .fitSize([width, height], {
            type: 'FeatureCollection',
            features: nodes.map(n => ({
              type: 'Feature',
              geometry: { type: 'Point', coordinates: [n.lon, n.lat] }
            }))
          });

        // 2. Map nodes to include x,y and pin them with fx,fy
        const mappedNodes = nodes.map(n => {
          const [x, y] = projection([n.lon, n.lat]);
          return { ...n, x, y, fx: x, fy: y };
        });

        setGraphData({ nodes: mappedNodes, links });
      })
      .catch(console.error);
  }, []);

  if (!graphData.nodes.length) return <div>Loading…</div>;

  return (
    <>
      {/* Add UI controls to change the default values for time and day */}
      <label>
        Day:
        <select value={selectedDayType}
                onChange={e => setSelectedDayType(e.target.value)}>
          <option value="weekday">Weekday</option>
          <option value="saturday">Saturday</option>
          <option value="sunday">Sunday</option>
        </select>
      </label>
      <label>
        Time:
        <select value={selectedTripTime}
                onChange={e => setSelectedTripTime(e.target.value)}>
          <option>AM Peak</option>
          <option>Midday</option>
          <option>PM Peak</option>
          <option>Evening</option>
          <option>Late Night</option>
        </select>
      </label>
  
      {/* Assign the values from the UI elements to the nodes */}
      <ForceGraph2D
        ref={fgRef}
        graphData={graphData}
        onZoom={transform => setZoomScale(transform.k)}  // capture current scale
        enableZoomPanInteraction={true}                  // ensure default zoom is enabled
  
        // 1) size nodes by exit-volume per day and time
        nodeVal={node => {
          const vol    = node.volumes[selectedDayType]?.[selectedTripTime] || 0;
          const logVol = Math.log(vol + 1);
          // normalize 0–1, then power‐scale, then map to size range
          const t = Math.pow(logVol / maxLog, exponent);
          return (minSize + t * (maxSize - minSize))/zoomScale;
        }}
        
        // 2) color nodes by their “line” attribute by referencing the linecolor map, fallback to grey if missing
        nodeColor={node => lineColorMap[node.line] || '#888'}
  
        // 3) tooltip showing station name + line
        nodeLabel={node => `${node.id} (Line ${node.line})`}
      />
    </>
  );
}

export default App;
