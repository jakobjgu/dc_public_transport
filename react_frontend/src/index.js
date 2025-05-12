// import React from "react";
// import ReactDOM from "react-dom/client";
// import 'bootstrap/dist/css/bootstrap.min.css';
// import { BrowserRouter } from "react-router-dom";
// import App from "./App";

// ReactDOM.createRoot(document.getElementById("root")).render(
//   // <React.StrictMode>
//   //     <BrowserRouter>
//         <App />
//   //     </BrowserRouter>
//   // </React.StrictMode>
// );
// src/index.js

import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';

const container = document.getElementById('root');
const root = createRoot(container);
root.render(<App />);

