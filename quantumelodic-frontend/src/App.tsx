import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import CreateChart from './pages/CreateChart';
import Results from './pages/Results';
import './index.css';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/create" element={<CreateChart />} />
        <Route path="/results" element={<Results />} />
      </Routes>
    </BrowserRouter>
  );
}
