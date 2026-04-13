import streamlit as st
import random

# Initialize game state in session_state
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
    st.session_state.score = 0
    st.session_state.lives = 3
    st.session_state.paddle_x = 350
    st.session_state.ball_x = 400
    st.session_state.ball_y = 500
    st.session_state.ball_dx = 3
    st.session_state.ball_dy = -3
    # Create bricks (5 rows x 8 columns)
    st.session_state.bricks = [[True for _ in range(8)] for _ in range(5)]

st.set_page_config(page_title="Brick Breaker Game", layout="wide")
st.title("🧱 Brick Breaker")

# Display score and lives
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Score", st.session_state.score)
with col2:
    st.metric("Lives", st.session_state.lives)
with col3:
    if st.button("New Game"):
        st.session_state.game_started = False
        st.session_state.score = 0
        st.session_state.lives = 3
        st.session_state.paddle_x = 350
        st.session_state.ball_x = 400
        st.session_state.ball_y = 500
        st.session_state.bricks = [[True for _ in range(8)] for _ in range(5)]
        st.rerun()

# Game controls
if not st.session_state.game_started:
    if st.button("Start Game 🎮"):
        st.session_state.game_started = True
        st.rerun()
else:
    # Paddle controls
    col_left, col_right = st.columns(2)
    with col_left:
        if st.button("⬅️ Move Left"):
            st.session_state.paddle_x = max(0, st.session_state.paddle_x - 50)
    with col_right:
        if st.button("➡️ Move Right"):
            st.session_state.paddle_x = min(700, st.session_state.paddle_x + 50)

# Game visualization using HTML/CSS canvas
game_html = f"""
<style>
    canvas {{
        border: 2px solid #333;
        background: #111;
        display: block;
        margin: 0 auto;
    }}
</style>
<canvas id="gameCanvas" width="800" height="600"></canvas>
<script>
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');
    
    let gameRunning = true;
    let score = {st.session_state.score};
    let lives = {st.session_state.lives};
    let paddleX = {st.session_state.paddle_x};
    let ballX = {st.session_state.ball_x};
    let ballY = {st.session_state.ball_y};
    let ballDX = {st.session_state.ball_dx};
    let ballDY = {st.session_state.ball_dy};
    
    // Brick setup
    const brickRowCount = 5;
    const brickColumnCount = 8;
    const brickWidth = 75;
    const brickHeight = 20;
    const brickPadding = 10;
    const brickOffsetTop = 60;
    const brickOffsetLeft = 30;
    
    let bricks = {st.session_state.bricks};
    
    const paddleWidth = 100;
    const paddleHeight = 12;
    const ballRadius = 8;
    
    document.addEventListener('keydown', keyDownHandler);
    document.addEventListener('keyup', keyUpHandler);
    
    let rightPressed = false;
    let leftPressed = false;
    
    function keyDownHandler(e) {{
        if(e.key == 'Right' || e.key == 'ArrowRight') {{
            rightPressed = true;
        }}
        else if(e.key == 'Left' || e.key == 'ArrowLeft') {{
            leftPressed = true;
        }}
    }}
    
    function keyUpHandler(e) {{
        if(e.key == 'Right' || e.key == 'ArrowRight') {{
            rightPressed = false;
        }}
        else if(e.key == 'Left' || e.key == 'ArrowLeft') {{
            leftPressed = false;
        }}
    }}
    
    function collisionDetection() {{
        for(let c=0; c<brickColumnCount; c++) {{
            for(let r=0; r<brickRowCount; r++) {{
                let b = bricks[r][c];
                if(b) {{
                    if(ballX > c*(brickWidth+brickPadding)+brickOffsetLeft && 
                       ballX < c*(brickWidth+brickPadding)+brickOffsetLeft+brickWidth && 
                       ballY > r*(brickHeight+brickPadding)+brickOffsetTop && 
                       ballY < r*(brickHeight+brickPadding)+brickOffsetTop+brickHeight) {{
                        ballDY = -ballDY;
                        bricks[r][c] = false;
                        score++;
                        if(score == brickRowCount*brickColumnCount) {{
                            alert("YOU WIN! Congratulations!");
                            document.location.reload();
                        }}
                    }}
                }}
            }}
        }}
    }}
    
    function draw() {{
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Draw bricks
        for(let c=0; c<brickColumnCount; c++) {{
            for(let r=0; r<brickRowCount; r++) {{
                if(bricks[r][c]) {{
                    ctx.fillStyle = '#FF5722';
                    ctx.fillRect(c*(brickWidth+brickPadding)+brickOffsetLeft, 
                                r*(brickHeight+brickPadding)+brickOffsetTop, 
                                brickWidth, brickHeight);
                    ctx.strokeStyle = '#333';
                    ctx.strokeRect(c*(brickWidth+brickPadding)+brickOffsetLeft, 
                                  r*(brickHeight+brickPadding)+brickOffsetTop, 
                                  brickWidth, brickHeight);
                }}
            }}
        }}
        
        // Draw paddle
        ctx.fillStyle = '#4CAF50';
        ctx.fillRect(paddleX, canvas.height-paddleHeight, paddleWidth, paddleHeight);
        
        // Draw ball
        ctx.fillStyle = '#FFEB3B';
        ctx.beginPath();
        ctx.arc(ballX, ballY, ballRadius, 0, Math.PI*2);
        ctx.fill();
        ctx.closePath();
        
        // Score and lives display
        ctx.fillStyle = 'white';
        ctx.font = '16px Arial';
        ctx.fillText("Score: " + score, 8, 20);
        ctx.fillText("Lives: " + lives, canvas.width-65, 20);
    }}
    
    function update() {{
        if(!gameRunning) return;
        
        // Paddle movement
        if(rightPressed && paddleX < canvas.width-paddleWidth) {{
            paddleX += 7;
        }}
        else if(leftPressed && paddleX > 0) {{
            paddleX -= 7;
        }}
        
        // Ball movement
        ballX += ballDX;
        ballY += ballDY;
        
        // Wall collisions
        if(ballX + ballRadius > canvas.width || ballX - ballRadius < 0) {{
            ballDX = -ballDX;
        }}
        if(ballY - ballRadius < 0) {{
            ballDY = -ballDY;
        }}
        
        // Paddle collision
        if(ballY + ballRadius > canvas.height-paddleHeight && 
           ballX > paddleX && ballX < paddleX + paddleWidth) {{
            ballDY = -ballDY;
        }}
        
        // Bottom wall (lose life)
        if(ballY + ballRadius > canvas.height) {{
            lives--;
            if(lives == 0) {{
                alert("GAME OVER! Final Score: " + score);
                document.location.reload();
            }} else {{
                ballX = canvas.width/2;
                ballY = canvas.height-30;
                ballDX = 3;
                ballDY = -3;
                paddleX = (canvas.width-paddleWidth)/2;
            }}
        }}
        
        collisionDetection();
        draw();
        requestAnimationFrame(update);
    }}
    
    update();
</script>
"""

st.components.v1.html(game_html, height=650, width=820)

st.markdown("""
### 🎮 How to Play:
- Use **LEFT** and **RIGHT** arrow keys to move the paddle
- Break all the orange bricks to win!
- Don't let the ball hit the bottom—you have 3 lives
- Green paddle + yellow ball = classic arcade fun!
""")
