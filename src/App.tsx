import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Landing from './pages/Landing'
import GenesisPack from './pages/GenesisPack'
import TaxAssistPack from './pages/TaxAssistPack'
import Success from './pages/Success'
import AdminPacksPage from './pages/AdminPacksPage'
import AutomationsPage from './pages/AutomationsPage'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/packs/genesis-mission" element={<GenesisPack />} />
        <Route path="/packs/tax-assist" element={<TaxAssistPack />} />
        <Route path="/success" element={<Success />} />
        <Route path="/admin" element={<AdminPacksPage />} />
        <Route path="/admin/automations" element={<AutomationsPage />} />
      </Routes>
    </Router>
  )
}

export default App

