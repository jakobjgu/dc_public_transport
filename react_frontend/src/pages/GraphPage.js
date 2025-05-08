import React, { useState, useEffect, useRef, useMemo } from 'react';
import ForceGraph2D from 'react-force-graph-2d';
import { geoMercator } from 'd3-geo';
import { useParams } from 'react-router-dom';

// define the line→color map
const lineColorMap = {
  red:    '#DA291C',
  blue:   '#0039A6',
  silver: '#A5ACAF',
  green:  '#00963F',
  yellow: '#F9E300',
  orange: '#ED8B00'
};

export default function GraphPage() {
  const { dataset } = useParams(); // "exits" or "entries"
  const [graphData, setGraphData] = useState({ nodes: [], links: [] });
  // Define default day‐type and trip‐time as state:
  const [selectedDayType,  setSelectedDayType]  = useState('weekday');
  const [selectedTripTime, setSelectedTripTime] = useState('AM Peak');
  const fgRef = useRef();
  const width = window.innerWidth;
  const height = window.innerHeight;

  // Fetch graph (nodes+links+volumes)
  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(() => {
    // fetch(`http://${window.location.hostname}:5001/api/${dataset}`)
    fetch(`/api/${dataset}`)
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
  }, [dataset]);

    // compute max log for scaling
  const maxVol = useMemo(() => 
    Math.max(1, ...graphData.nodes.map(n => n.volumes[selectedDayType]?.[selectedTripTime] || 0)),
    [graphData, selectedDayType, selectedTripTime]
  );
  const maxLog = useMemo(() => Math.log(maxVol + 1), [maxVol]);
  
  const [zoomScale, setZoomScale] = useState(1);

  const minSize = 0.5;
  const maxSize = 15;
  const exponent = 10;

  if (!graphData.nodes.length) return <div>Loading…</div>;

  return (
    <div style={{ height: '100vh' }}>
      {/* Controls */}
      <div style={{ padding: '10px', background: '#fff' }}>
        <select value={selectedDayType} onChange={e => setSelectedDayType(e.target.value)}>
          <option value="weekday">Weekday</option>
          <option value="saturday">Saturday</option>
          <option value="sunday">Sunday</option>
        </select>
        <select value={selectedTripTime} onChange={e => setSelectedTripTime(e.target.value)}>
          <option>AM Peak</option>
          <option>Midday</option>
          <option>PM Peak</option>
          <option>Evening</option>
          <option>Late Night</option>
        </select>
      </div>
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
    </div>
  );
}
