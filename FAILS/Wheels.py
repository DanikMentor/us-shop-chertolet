from flask import Flask, render_template_string, jsonify
import random

app = Flask(__name__)

PRIZES = [
    {"id": 0, "label": "10% OFF", "weight": 25, "color": "#e74c3c"},
    {"id": 1, "label": "FREE COFFEE", "weight": 15, "color": "#3498db"},
    {"id": 2, "label": "GIFT CARD", "weight": 10, "color": "#f1c40f"},
    {"id": 3, "label": "ICE CREAM", "weight": 15, "color": "#9b59b6"},
    {"id": 4, "label": "MOVIE TICKET", "weight": 8, "color": "#e67e22"},
    {"id": 5, "label": "NO LUCK", "weight": 20, "color": "#95a5a6"},
    {"id": 6, "label": "TSHIRT", "weight": 5, "color": "#2ecc71"},
    {"id": 7, "label": "JACKPOT!", "weight": 2, "color": "#1abc9c"},
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fortune Wheel</title>
    <style>
        body {
            background: #121212;
            color: #ffffff;
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
        }

        .container {
            position: relative;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        /* Pointer on the right side */
        .pointer {
            position: absolute;
            right: -30px;
            top: 50%;
            transform: translateY(-50%);
            width: 0; 
            height: 0; 
            border-top: 25px solid transparent;
            border-bottom: 25px solid transparent;
            border-right: 50px solid #ff4757;
            z-index: 100;
            filter: drop-shadow(-4px 0 4px rgba(0,0,0,0.5));
        }

        .wheel-box {
            position: relative;
            width: 460px;
            height: 460px;
            border: 10px solid #222;
            border-radius: 50%;
            padding: 5px;
            background: #222;
            box-shadow: 0 0 30px rgba(0,0,0,0.8);
        }

        canvas {
            border-radius: 50%;
            transition: transform 5s cubic-bezier(0.15, 0, 0.1, 1);
        }

        .ui {
            margin-top: 40px;
            text-align: center;
        }

        #spin-btn {
            background: #27ae60;
            border: none;
            padding: 18px 50px;
            color: white;
            font-size: 22px;
            font-weight: bold;
            border-radius: 50px;
            cursor: pointer;
            box-shadow: 0 5px 15px rgba(39, 174, 96, 0.4);
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        #spin-btn:hover { background: #2ecc71; transform: translateY(-2px); }
        #spin-btn:active { transform: translateY(0); }
        #spin-btn:disabled { background: #444; cursor: not-allowed; box-shadow: none; }

        #status {
            margin-top: 25px;
            height: 40px;
            font-size: 26px;
            font-weight: bold;
            color: #f1c40f;
            text-shadow: 0 0 10px rgba(241, 196, 15, 0.3);
        }
    </style>
</head>
<body>

    <div class="container">
        <div class="pointer"></div>
        <div class="wheel-box">
            <canvas id="canvas" width="460" height="460"></canvas>
        </div>
    </div>

    <div class="ui">
        <button id="spin-btn">Spin to Win</button>
        <div id="status"></div>
    </div>

    <script>
        const prizes = {{ prizes|tojson }};
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        const btn = document.getElementById('spin-btn');
        const statusText = document.getElementById('status');

        const centerX = canvas.width / 2;
        const centerY = canvas.height / 2;
        const numSectors = prizes.length;
        const arcSize = (2 * Math.PI) / numSectors;

        let rotation = 0;

        function drawWheel() {
            prizes.forEach((prize, i) => {
                const angle = i * arcSize;
                
                // Draw sector
                ctx.beginPath();
                ctx.fillStyle = prize.color;
                ctx.moveTo(centerX, centerY);
                ctx.arc(centerX, centerY, centerX, angle, angle + arcSize);
                ctx.lineTo(centerX, centerY);
                ctx.fill();
                ctx.strokeStyle = '#121212';
                ctx.lineWidth = 2;
                ctx.stroke();

                // Draw text
                ctx.save();
                ctx.translate(centerX, centerY);
                ctx.rotate(angle + arcSize / 2);
                ctx.textAlign = "right";
                ctx.fillStyle = "#fff";
                ctx.font = "bold 16px Arial";
                // Adjust text position inside the sector
                ctx.fillText(prize.label, centerX - 30, 8);
                ctx.restore();
            });
        }

        async function spin() {
            btn.disabled = true;
            statusText.innerText = "Good Luck...";
            
            // Get winner from server
            const response = await fetch('/get_winner');
            const winner = await response.json();

            const spins = 360 * 6; // At least 6 full spins
            const sectorDeg = 360 / numSectors;
            
            /* The pointer is at 0 degrees (right side).
               To stop exactly at winner.id, we rotate the wheel so that
               the winner sector is centered at 0 degrees.
            */
            const stopAt = 360 - (winner.id * sectorDeg) - (sectorDeg / 2);
            
            rotation += spins + (stopAt - (rotation % 360));
            
            canvas.style.transform = `rotate(${rotation}deg)`;

            setTimeout(() => {
                statusText.innerText = "YOU WON: " + winner.label;
                btn.disabled = false;
            }, 5200);
        }

        btn.addEventListener('click', spin);
        drawWheel();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, prizes=PRIZES)

@app.route('/get_winner')
def get_winner():
    weights = [p['weight'] for p in PRIZES]
    winner = random.choices(PRIZES, weights=weights, k=1)[0]
    return jsonify(winner)

if __name__ == '__main__':
    app.run(debug=True)