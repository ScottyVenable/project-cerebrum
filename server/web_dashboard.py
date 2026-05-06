from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import asyncio
import json
import numpy as np
from pylsl import StreamInlet, resolve_stream

app = FastAPI()

# HTML Template for the Real-time Dashboard
html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Project Cerebrum: Web Dashboard</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body { background: #0A0A0B; color: #F8FAFC; font-family: 'Inter', sans-serif; }
            h1 { color: #8B5CF6; text-align: center; }
            #chart { width: 90%; margin: auto; }
        </style>
    </head>
    <body>
        <h1>Cerebrum Real-time Neural Monitor</h1>
        <div id="chart"></div>
        <script>
            const chartDiv = document.getElementById('chart');
            const traces = [];
            for (let i = 0; i < 8; i++) {
                traces.push({
                    y: [],
                    mode: 'lines',
                    name: `CH ${i+1}`,
                    line: { width: 1 }
                });
            }
            
            Plotly.newPlot(chartDiv, traces, {
                plot_bgcolor: '#0A0A0B',
                paper_bgcolor: '#0A0A0B',
                font: { color: '#F8FAFC' },
                xaxis: { title: 'Samples', showgrid: false },
                yaxis: { title: 'uV', showgrid: false }
            });

            const ws = new WebSocket(`ws://${window.location.host}/ws`);
            ws.onmessage = function(event) {
                const data = JSON.parse(event.data);
                Plotly.extendTraces(chartDiv, { y: data.samples }, [0, 1, 2, 3, 4, 5, 6, 7], 250);
            };
        </script>
    </body>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("[Web] Client connected to live stream.")
    
    # Connect to LSL
    streams = resolve_stream('type', 'EEG')
    inlet = StreamInlet(streams[0])
    
    try:
        while True:
            samples, timestamps = inlet.pull_chunk(timeout=0.1, max_samples=25)
            if samples:
                # Transpose and send as JSON
                data_packet = {"samples": np.array(samples).T.tolist()}
                await websocket.send_text(json.dumps(data_packet))
            await asyncio.sleep(0.04) # ~25Hz UI update
    except Exception as e:
        print(f"[Web] Stream closed: {e}")
    finally:
        await websocket.close()
