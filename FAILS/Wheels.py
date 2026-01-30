from flask import Flask, render_template_string, jsonify
import random

app = Flask(__name__)

# Laika datuma bāze
user_data = {
    "bonuses": 10
}

PRIZES = [
    {"id": 0, "label": "Никита", "weight": 10, "color": "#e74c3c"},
    {"id": 1, "label": "Арсений", "weight": 10, "color": "#3498db"},
    {"id": 2, "label": "Костя", "weight": 10, "color": "#f1c40f"},
    {"id": 3, "label": "Саня", "weight": 10, "color": "#9b59b6"},
    {"id": 4, "label": "Максон", "weight": 10,"color": "#e67e22"},
    {"id": 5, "label": "Алекс", "weight": 10, "color": "#95a5a6"},
    {"id": 6, "label": "Валик", "weight": 10, "color": "#2ecc71"},
    {"id": 7, "label": "Руслан", "weight": 10, "color": "#1abc9c"},
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fortune Wheel</title>
    <style>
        body {
            background: #121212;
            color: #ffffff;
            font-family: 'Segoe UI', Roboto, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
        }

        /* Bonus table */
        .bonus-display {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 20px;
            padding: 10px 25px;
            background: #1e1e1e;
            border-radius: 12px;
            border: 1px solid #333;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        }
        #bonus-count { color: #f1c40f; }

        .container {
            position: relative;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .pointer {
            position: absolute;
            right: -30px;
            top: 50%;
            transform: translateY(-50%);
            width: 0; height: 0; 
            border-top: 25px solid transparent;
            border-bottom: 25px solid transparent;
            border-right: 50px solid #ff4757;
            z-index: 100;
        }

        .wheel-box {
            position: relative;
            width: 460px; height: 460px;
            border: 10px solid #222;
            border-radius: 50%;
            background: #222;
            box-shadow: 0 0 30px rgba(0,0,0,0.8);
        }

        canvas { border-radius: 50%; transition: transform 5s cubic-bezier(0.15, 0, 0.1, 1); }

        .ui { margin-top: 40px; text-align: center; }

        #spin-btn {
            background: #27ae60;
            border: none;
            padding: 18px 40px;
            color: white;
            font-size: 20px;
            font-weight: bold;
            border-radius: 50px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
        }

        #spin-btn:hover { background: #2ecc71; transform: scale(1.05); }
        #spin-btn:disabled { background: #444; cursor: not-allowed; transform: none; }

        #status { margin-top: 25px; height: 40px; font-size: 24px; font-weight: bold; color: #f1c40f; }
    </style>
</head>
<body>

    <div class="bonus-display">
        Bonusu skaits: <span id="bonus-count">...</span>
    </div>

    <div class="container">
        <div class="pointer"></div>
        <div class="wheel-box">
            <canvas id="canvas" width="460" height="460"></canvas>
        </div>
    </div>

    <div class="ui">
        <button id="spin-btn">Cena: 1 bonuss</button>
        <div id="status"></div>
    </div>

    <script>
        const prizes = {{ prizes|tojson }};
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        const btn = document.getElementById('spin-btn');
        const statusText = document.getElementById('status');
        const bonusCounter = document.getElementById('bonus-count');

        const centerX = canvas.width / 2;
        const centerY = canvas.height / 2;
        const numSectors = prizes.length;
        const arcSize = (2 * Math.PI) / numSectors;
        let rotation = 0;

        // Saņemam pašreizējās prēmijas par lejupielādi
        async function fetchBonuses() {
            const res = await fetch('/get_bonuses');
            const data = await res.json();
            bonusCounter.innerText = data.bonuses;
            if (data.bonuses < 1) {
                btn.disabled = true;
                btn.innerText = "Nepietiekami bonusi";
            }
        }

        function drawWheel() {
            prizes.forEach((prize, i) => {
                const angle = i * arcSize;
                ctx.beginPath();
                ctx.fillStyle = prize.color;
                ctx.moveTo(centerX, centerY);
                ctx.arc(centerX, centerY, centerX, angle, angle + arcSize);
                ctx.lineTo(centerX, centerY);
                ctx.fill();
                ctx.strokeStyle = '#121212';
                ctx.lineWidth = 2;
                ctx.stroke();

                ctx.save();
                ctx.translate(centerX, centerY);
                ctx.rotate(angle + arcSize / 2);
                ctx.textAlign = "right";
                ctx.fillStyle = "#fff";
                ctx.font = "bold 16px Arial";
                ctx.fillText(prize.label, centerX - 30, 8);
                ctx.restore();
            });
        }

        async function spin() {
            btn.disabled = true;
            statusText.innerText = "Veiksme smaida...";
            
            const response = await fetch('/get_winner');
            const data = await response.json();

            if (data.error) {
                statusText.innerText = data.error;
                return;
            }

            const spins = 360 * 6;
            const sectorDeg = 360 / numSectors;
            const stopAt = 360 - (data.winner.id * sectorDeg) - (sectorDeg / 2);
            
            rotation += spins + (stopAt - (rotation % 360));
            canvas.style.transform = `rotate(${rotation}deg)`;

            setTimeout(() => {
                statusText.innerText = "Jūs esat uzvarējis: " + data.winner.label;
                fetchBonuses(); // Atjaunojam bilanci pēc spēles
                btn.disabled = false;
            }, 5200);
        }

        btn.addEventListener('click', spin);
        drawWheel();
        fetchBonuses();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, prizes=PRIZES)

@app.route('/get_bonuses')
def get_bonuses():
    return jsonify({"bonuses": user_data["bonuses"]})

@app.route('/get_winner')
def get_winner():
    # Pārbaude servera pusē
    if user_data["bonuses"] < 1:
        return jsonify({"error": "Nepietiekami bonusi"}), 400
    
    # Bonusa norakstīšana
    user_data["bonuses"] -= 1
    
    weights = [p['weight'] for p in PRIZES]
    winner = random.choices(PRIZES, weights=weights, k=1)[0]
    return jsonify({"winner": winner})

if __name__ == '__main__':
    app.run(debug=True)