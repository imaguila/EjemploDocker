import React, { useState } from 'react';
import './App.css';

function App() {
  const [form, setForm] = useState({ firstName: '', lastName: '', emergencyName: '', emergencyPhone: '' });
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Fetch al backend (Docker mapea localhost:5000 desde el navegador)
      const res = await fetch('http://localhost:5000/api/enroll-camper', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form)
      });
      if (res.ok) alert('¡Guardado!');
      else alert('Error');
    } catch (err) { console.error(err); alert('Error de conexión'); }
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Registro Campamento (Docker)</h1>
      <form onSubmit={handleSubmit}>
        <input placeholder="Nombre" onChange={e => setForm({...form, firstName: e.target.value})} /><br/>
        <input placeholder="Apellido" onChange={e => setForm({...form, lastName: e.target.value})} /><br/>
        <input placeholder="Contacto Emergencia" onChange={e => setForm({...form, emergencyName: e.target.value})} /><br/>
        <input placeholder="Teléfono" onChange={e => setForm({...form, emergencyPhone: e.target.value})} /><br/>
        <button type="submit">Guardar</button>
      </form>
    </div>
  );
}

export default App;
