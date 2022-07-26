import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import { Navbar } from "./components/Navbar";
import { About } from "./components/About";
import { Users } from "./components/Users";

function App() {
  return (
    <Router>
      <Navbar />

      <div className="container p-4">
        <Routes>
          <Route path="/about" component={About} />
          <Route path="/" component={Users} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
