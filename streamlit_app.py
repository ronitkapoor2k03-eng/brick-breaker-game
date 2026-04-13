import streamlit as st

st.set_page_config(page_title="Brick Breaker Game", layout="wide")

st.title("🧱 BRICK BREAKER - Arcade Classic")
st.markdown("*Use **LEFT** and **RIGHT** arrow keys to control the paddle*")

# The complete working game HTML
game_html = """
<div style="display: flex; justify-content: center; margin: 20px 0;">
    <canvas id="gameCanvas" width="800" height="600" style="border: 3px solid white; border-radius: 10px; background: black; box-shadow: 0 10px 30px rgba(0,0,0,0.3);"></canvas>
</div>

<script>
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');
    
    let score = 0;
    let lives = 3;
    let gameRunning = true;
    
    const paddleWidth = 100;
    const paddleHeight = 12;
    let paddleX = (canvas.width - paddleWidth) / 2;
    
    const ballRadius = 8;
    let ballX = canvas.width / 2;
    let ballY = canvas.height - 50;
    let ballDX = 3;
    let ballDY = -3;
    
    const brickRowCount = 5;
    const brickColumnCount = 8;
    const brickWidth = 75;
    const brickHeight = 20;
    const brickPadding = 10;
    const brickOffsetTop = 60;
    const brickOffsetLeft = 30;
    
    let bricks = [];
    for(let c = 0; c < brickColumnCount; c++) {
        bricks[c] = [];
        for(let r = 0; r < brickRowCount; r++) {
            bricks[c][r] = { x: 0, y: 0, status: 1 };
        }
    }
    
    let rightPressed = false;
    let leftPressed = false;
    
    document.addEventListener('keydown', (e) => {
        if(e.key === 'ArrowRight') rightPressed = true;
        if(e.key === 'ArrowLeft') leftPressed = true;
    });
    
    document.addEventListener('keyup', (e) => {
        if(e.key === 'ArrowRight') rightPressed = false;
        if(e.key === 'ArrowLeft') leftPressed = false;
    });
    
    function collisionDetection() {
        for(let c = 0; c < brickColumnCount; c++) {
            for(let r = 0; r < brickRowCount; r++) {
                let b = bricks[c][r];
                if(b.status === 1) {
                    if(ballX > b.x && ballX < b.x + brickWidth && ballY > b.y && ballY < b.y + brickHeight) {
                        ballDY = -ballDY;
                        b.status = 0;
                        score++;
                        if(score === brickRowCount * brickColumnCount) {
                            alert("🎉 YOU WIN! 🎉\\nFinal Score: " + score);
                            resetGame();
                        }
                    }
                }
            }
        }
    }
    
    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Draw bricks
        for(let c = 0; c < brickColumnCount; c++) {
            for(let r = 0; r < brickRowCount; r++) {
                if(bricks[c][r].status === 1) {
                    const brickX = c * (brickWidth + brickPadding) + brickOffsetLeft;
                    const brickY = r * (brickHeight + brickPadding) + brickOffsetTop;
                    bricks[c][r].x = brickX;
                    bricks[c][r].y = brickY;
                    
                    const colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'];
                    ctx.fillStyle = colors[r % colors.length];
                    ctx.fillRect(brickX, brickY, brickWidth, brickHeight);
                    ctx.strokeStyle = '#333';
                    ctx.strokeRect(brickX, brickY, brickWidth, brickHeight);
                }
            }
        }
        
        // Draw paddle
        ctx.fillStyle = '#00FF00';
        ctx.fillRect(paddleX, canvas.height - paddleHeight, paddleWidth, paddleHeight);
        
        // Draw ball
        ctx.fillStyle = '#FFEB3B';
        ctx.beginPath();
        ctx.arc(ballX, ballY, ballRadius, 0, Math.PI * 2);
        ctx.fill();
        
        // Draw score and lives
        ctx.fillStyle = 'white';
        ctx.font = 'bold 20px Arial';
        ctx.fillText('Score: ' + score, 10, 30);
        ctx.fillText('Lives: ' + lives, canvas.width - 100, 30);
    }
    
    function update() {
        if(!gameRunning) return;
        
        if(rightPressed && paddleX < canvas.width - paddleWidth) paddleX += 7;
        if(leftPressed && paddleX > 0) paddleX -= 7;
        
        ballX += ballDX;
        ballY += ballDY;
        
        if(ballX + ballRadius > canvas.width || ballX - ballRadius < 0) ballDX = -ballDX;
        if(ballY - ballRadius < 0) ballDY = -ballDY;
        
        if(ballY + ballRadius > canvas.height - paddleHeight && 
           ballX > paddleX && ballX < paddleX + paddleWidth) {
            let hitPos = (ballX - paddleX) / paddleWidth;
            ballDX = (hitPos - 0.5) * 8;
            ballDY = -ballDY;
        }
        
        if(ballY + ballRadius > canvas.height) {
            lives--;
            if(lives === 0) {
                gameRunning = false;
                alert("💀 GAME OVER! 💀\\nFinal Score: " + score);
                resetGame();
            } else {
                ballX = canvas.width / 2;
                ballY = canvas.height - 50;
                ballDX = 3;
                ballDY = -3;
                paddleX = (canvas.width - paddleWidth) / 2;
            }
        }
        
        collisionDetection();
        draw();
        requestAnimationFrame(update);
    }
    
    function resetGame() {
        score = 0;
        lives = 3;
        gameRunning = true;
        paddleX = (canvas.width - paddleWidth) / 2;
        ballX = canvas.width / 2;
        ballY = canvas.height - 50;
        ballDX = 3;
        ballDY = -3;
        
        for(let c = 0; c < brickColumnCount; c++) {
            for(let r = 0; r < brickRowCount; r++) {
                bricks[c][r].status = 1;
            }
        }
    }
    
    update();
</script>

<div style="display: flex; justify-content: center; gap: 40px; margin-top: 20px;">
    <div style="background: rgba(0,0,0,0.7); padding: 10px 20px; border-radius: 10px;">
        <span style="color: white;">🏆 Score: </span>
        <span style="color: yellow; font-size: 24px; font-weight: bold;" id="scoreDisplay">0</span>
    </div>
    <div style="background: rgba(0,0,0,0.7); padding: 10px 20px; border-radius: 10px;">
        <span style="color: white;">❤️ Lives: </span>
        <span style="color: red; font-size: 24px; font-weight: bold;" id="livesDisplay">3</span>
    </div>
</div>
"""

st.components.v1.html(game_html, height=700, width=850)

with st.expander("🎮 How to Play"):
    st.markdown("""
    - **Left Arrow** - Move paddle left
    - **Right Arrow** - Move paddle right
    - Break all colorful bricks to win!
    - You have 3 lives - don't let the ball fall!
    """)
