proyecto-fullstack/
├── docker-compose.yml
├── backend/                <-- El Cerebro (Python)
│   ├── Dockerfile
│   ├── requirements.txt
│   └── main.py
└── frontend/               <-- La Cara (Nginx + HTML)
    ├── Dockerfile
    ├── nginx.conf          <-- Configuración del puente
    └── index.html          <-- Tu web

    docker compose up --build

 http://localhost
