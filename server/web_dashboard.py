from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import asyncio
import json
import numpy as np
from pylsl import StreamInlet, resolve_stream
from scipy.signal import welch

app = FastAPI()

# Enhanced HTML Template with PSD and Confidence Gauge
html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Cerebrum: Professional Neuro-Dashboard</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body { background: #0A0A0B; color: #F8FAFC; font-family: 'Inter', sans-serif; display: flex; flex-direction: column; height: 100vh; margin: 0; }
            .header { background: #1E1E2E; padding: 10px; border-bottom: 2px solid #8B5CF6; text-align: center; }
            .container { display: flex; flex: 1; padding: 10px; gap: 10px; }
            .left-panel { flex: 2; display: flex; flex-direction: column; gap: 10px; }
            .right-panel { flex: 1; background: #1E1E2E; border-radius: 8px; padding: 15px; }
            .chart-box { background: #1E1E2E; border-radius: 8px; padding: 10px; flex: 1; }
            h2 { color: #22D3EE; font-size: 1.2em; margin-top: 0; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>PROJECT CEREBRUM: NEURAL COMMAND CENTER</h1>
        </div>
        <div class="container">
            <div class="left-panel">
                <div class="chart-box" id="time-series"></div>
                <div class="chart-box" id="psd-plot"></div>
            </div>
            <div class="right-panel">
                <h2>System Status</h2>
                <p>Status: <span id="status" style="color: #4ADE80;">ACTIVE</span></p>
                <p>LSL Stream: <span id="stream-name">Searching...</span></p>
                <hr style="border-color: #313244;">
                <h2>Inference Engine</h2>
                <div id="gauge"></div>
                <p style="text-align: center;">Target State: <strong id="state" style="color: #FCD34D;">REST</strong></p>
            </div>
        </div>
        <script>
            // Initialize Plots
            const timeSeriesDiv = document.getElementById('time-series');
            const psdDiv = document.getElementById('psd-plot');
            
            const tsTraces = [];
            for (let i = 0; i < 8; i++) tsTraces.push({ y: [], mode: 'lines', name: `CH ${i+1}` });
            Plotly.newPlot(timeSeriesDiv, tsTraces, { title: 'Raw EEG (Time Domain)', margin: {t:30, b:30, l:30, r:30}, paper_bgcolor: '#1E1E2E', plot_bgcolor: '#1E1E2E', font: {color: '#F8FAFC'} });

            const psdTraces = [{ x: [], y: [], type: 'scatter', fill: 'tozeroy', name: 'Global PSD' }];
            Plotly.newPlot(psdDiv, psdTraces, { title: 'Power Spectral Density (Frequency Domain)', margin: {t:30, b:30, l:30, r:30}, paper_bgcolor: '#1E1E2E', plot_bgcolor: '#1E1E2E', font: {color: '#F8FAFC'} });

            const ws = new WebSocket(`ws://${window.location.host}/ws`);
            ws.onmessage = function(event) {
                const data = JSON.parse(event.data);
                
                // Update Time Series
                Plotly.extendTraces(timeSeriesDiv, { y: data.samples }, [0, 1, 2, 3, 4, 5, 6, 7], 100);
                
                // Update PSD
                if (data.psd) {
                    Plotly.react(psdDiv, [{ x: data.freqs, y: data.psd, type: 'scatter', fill: 'tozeroy', line: {color: '#8B5CF6'} }], { title: 'Spectral Power (Hz)', paper_bgcolor: '#1E1E2E', plot_bgcolor: '#1E1E2E', font: {color: '#F8FAFC'} });
                }
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
    streams = resolve_stream('type', 'EEG')
    inlet = StreamInlet(streams[0])
    
    try:
        while True:
            samples, timestamps = inlet.pull_chunk(timeout=0.05, max_samples=50)
            if samples:
                samples_array = np.array(samples).T
                
                # Calculate PSD on the last chunk
                # Using Welsh's method for frequency analysis
                freqs, psd = welch(samples_array[0], fs=250, nperseg=min(len(samples), 256))
                
                data_packet = {
                    "samples": samples_array.tolist(),
                    "freqs": freqs.tolist(),
                    "psd": psd.tolist()
                }
                await websocket.send_text(json.dumps(data_packet))
            await asyncio.sleep(0.04)
    except Exception as e:
        print(f"[Web] Error: {e}")
    finally:
        await websocket.close()
