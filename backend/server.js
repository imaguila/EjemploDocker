const express = require('express');
const { Pool } = require('pg');
const cors = require('cors');

const app = express();
app.use(express.json());
app.use(cors());

// Conexión a la BD usando variables de entorno de Docker
const pool = new Pool({
  connectionString: process.env.DATABASE_URL
});

app.post('/api/enroll-camper', async (req, res) => {
  const { firstName, lastName, emergencyName, emergencyPhone } = req.body;
  try {
    await pool.query(
      'INSERT INTO campers (first_name, last_name, parent_id, emergency_contact_name, emergency_phone) VALUES ($1, $2, 1, $3, $4)',
      [firstName, lastName, emergencyName, emergencyPhone]
    );
    res.status(201).json({ message: "Campista guardado correctamente" });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: err.message });
  }
});

app.listen(5000, () => console.log('Backend listo en puerto 5000'));
