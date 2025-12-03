import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Landing from './pages/Landing'
import GenesisPack from './pages/GenesisPack'
import TaxAssistPack from './pages/TaxAssistPack'
import Success from './pages/Success'
import AdminPacksPage from './pages/AdminPacksPage'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/packs/genesis-mission" element={<GenesisPack />} />
        <Route path="/packs/tax-assist" element={<TaxAssistPack />} />
        <Route path="/success" element={<Success />} />
        <Route path="/admin" element={<AdminPacksPage />} />
      </Routes>
    </Router>
  )
}

export default App

