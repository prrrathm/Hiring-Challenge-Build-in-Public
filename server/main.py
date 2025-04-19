from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import random
from routers import game

app = FastAPI()


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>WebSocket Array Sum Game</title>
    </head>
    <body>
        <h1>Array Sum Game</h1>
        <button onclick="startGame()">Start Game</button>
        <div id="gameArea" style="display: none;">
            <p>Array 1: <span id="array1"></span></p>
            <p>Array 2: <span id="array2"></span></p>
            <input type="number" id="answerInput" placeholder="Enter number to add" min="0">
            <button onclick="submitAnswer()">Submit Answer</button>
        </div>
        <div id="messages"></div>
<script>
    let ws = null;
    
    function startGame() {
        // Reset UI
        document.getElementById('gameArea').style.display = 'none';
        document.getElementById('array1').textContent = '';
        document.getElementById('array2').textContent = '';
        document.getElementById('messages').innerHTML = '';
        document.getElementById('answerInput').value = '';
        
        // Close existing WebSocket if open
        if (ws && ws.readyState !== WebSocket.CLOSED) {
            ws.close();
        }
        
        // Create new WebSocket connection
        ws = new WebSocket("ws://localhost:8000/ws");
        
        ws.onmessage = function(event) {
            const data = JSON.parse(event.data);
            const messages = document.getElementById('messages');
            
            if (data.type === "arrays") {
                document.getElementById('array1').textContent = data.array1.join(', ');
                document.getElementById('array2').textContent = data.array2.join(', ');
                document.getElementById('gameArea').style.display = 'block';
            } else if (data.type === "result") {
                messages.innerHTML += `<p>${data.message}</p>`;
                if (data.correct) {
                    document.getElementById('gameArea').style.display = 'none';
                }
            } else if (data.type === "error") {
                messages.innerHTML += `<p>${data.message}</p>`;
            }
        };
        
        ws.onopen = function() {
            messages.innerHTML += "<p>Connected to server</p>";
            ws.send(JSON.stringify({type: "start"}));
        };
        
        ws.onclose = function() {
            messages.innerHTML += "<p>Disconnected from server</p>";
        };
        
        ws.onerror = function() {
            messages.innerHTML += "<p>Error connecting to server</p>";
        };
    }
    
    function submitAnswer() {
        if (ws && ws.readyState === WebSocket.OPEN) {
            const answer = document.getElementById('answerInput').value;
            if (answer !== '' && !isNaN(answer) && parseInt(answer) >= 0) {
                ws.send(JSON.stringify({type: "answer", answer: parseInt(answer)}));
                document.getElementById('answerInput').value = '';
            } else {
                document.getElementById('messages').innerHTML += "<p>Please enter a valid non-negative number</p>";
            }
        } else {
            document.getElementById('messages').innerHTML += "<p>Not connected to server</p>";
        }
    }
</script>
    </body>
</html>
"""

app.include_router(game.router, prefix="/game", tags=["Game"])

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    correct_answer = None
    
    try:
        while True:
            data = await websocket.receive_json()
            
            if data["type"] == "start":
                # Generate arrays until array1's sum is greater than array2's
                while True:
                    array1 = [random.randint(1, 10) for _ in range(3)]
                    array2 = [random.randint(1, 10) for _ in range(3)]
                    sum1 = sum(array1)
                    sum2 = sum(array2)
                    
                    # Ensure array1's sum is greater than array2's
                    if sum1 > sum2:
                        break
                    # If not, swap the arrays
                    elif sum1 < sum2:
                        array1, array2 = array2, array1
                        sum1, sum2 = sum2, sum1
                        break
                    # If sums are equal, try again
                    else:
                        continue
                
                correct_answer = sum1 - sum2
                
                await websocket.send_json({
                    "type": "arrays",
                    "array1": array1,
                    "array2": array2
                })
                
            elif data["type"] == "answer":
                user_answer = data.get("answer")
                
                if user_answer == correct_answer:
                    await websocket.send_json({
                        "type": "result",
                        "message": "✅ Correct! The sums are now equal.",
                        "correct": True
                    })
                    correct_answer = None  # Reset for next game
                else:
                    await websocket.send_json({
                        "type": "result",
                        "message": f"❌ Wrong answer. The correct number was {correct_answer}",
                        "correct": False
                    })
                    
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"Error: {e}")
        await websocket.send_json({
            "type": "error",
            "message": "An error occurred on the server"
        })
    finally:
        try:
            await websocket.close()
        except:
            pass