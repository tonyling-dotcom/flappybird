// Game configuration
let config = null;
let gameSettings = null;
let levels = null;
let currentLevel = 0;
let highScore = 0;

// Canvas and context
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Game state
let gameState = 'start'; // start, playing, paused, gameover, levelup
let score = 0;
let coins = 0;
let frameCount = 0;

// Images
const images = {
    player: new Image(),
    enemy: new Image(),
    map: new Image()
};

// Audio
const audio = {
    flap: new Audio('/static/audio/flap.mp3'),
    enemy: new Audio('/static/audio/enemy.mp3'),
    gameover: new Audio('/static/audio/gameover.mp3'),
    bg: new Audio('/static/audio/bg.mp3')
};

// Building colors
const BUILDING_COLORS = [
    [100, 149, 237],  // Cornflower blue
    [255, 127, 80],   // Coral
    [144, 238, 144],  // Light green
    [255, 218, 185],  // Peach
    [221, 160, 221]   // Plum
];

// Game objects
let player = null;
let walls = [];
let enemies = [];
let projectiles = [];
let coinsList = [];
let particles = [];

// Timers
let lastWallTime = 0;
let lastEnemyTime = 0;
let lastCoinTime = 0;

// Player class
class Player {
    constructor() {
        this.x = 150;
        this.y = canvas.height / 2;
        this.velocity = 0;
        this.size = gameSettings.player_size;
        this.angle = 0;
    }

    flap() {
        this.velocity = gameSettings.flap_strength;
        if (audio.flap) audio.flap.play().catch(() => {});
    }

    update() {
        this.velocity += gameSettings.gravity;
        this.y += this.velocity;
        
        // Rotation based on velocity
        this.angle = Math.min(Math.max(this.velocity * 3, -30), 90);
        
        // Boundaries
        if (this.y < 0) {
            this.y = 0;
            this.velocity = 0;
        }
        if (this.y + this.size > canvas.height) {
            this.y = canvas.height - this.size;
            this.velocity = 0;
            gameOver();
        }
    }

    draw() {
        ctx.save();
        ctx.translate(this.x + this.size / 2, this.y + this.size / 2);
        ctx.rotate((this.angle * Math.PI) / 180);
        ctx.drawImage(images.player, -this.size / 2, -this.size / 2, this.size, this.size);
        ctx.restore();
    }

    getRect() {
        return {
            x: this.x,
            y: this.y,
            width: this.size,
            height: this.size
        };
    }
}

// Wall class
class Wall {
    constructor() {
        const level = levels[currentLevel];
        this.width = gameSettings.wall_width;
        this.gap = level.wall_gap;
        this.x = canvas.width;
        this.gapY = Math.random() * (canvas.height - this.gap - 200) + 100;
        this.speed = level.wall_speed;
        this.scored = false;
        this.color = BUILDING_COLORS[Math.floor(Math.random() * BUILDING_COLORS.length)];
    }

    update() {
        this.x -= this.speed;
    }

    draw() {
        // Top building
        this.drawBuilding(this.x, 0, this.width, this.gapY);
        // Bottom building
        this.drawBuilding(this.x, this.gapY + this.gap, this.width, canvas.height - this.gapY - this.gap);
    }

    drawBuilding(x, y, width, height) {
        const [r, g, b] = this.color;
        ctx.fillStyle = `rgb(${r}, ${g}, ${b})`;
        ctx.fillRect(x, y, width, height);
        
        // Windows
        const windowSize = 8;
        const windowSpacing = 15;
        ctx.fillStyle = 'rgba(255, 255, 100, 0.6)';
        
        for (let wx = x + 10; wx < x + width - 10; wx += windowSpacing) {
            for (let wy = y + 10; wy < y + height - 10; wy += windowSpacing) {
                ctx.fillRect(wx, wy, windowSize, windowSize);
            }
        }
        
        // Border
        ctx.strokeStyle = 'rgba(0, 0, 0, 0.3)';
        ctx.lineWidth = 2;
        ctx.strokeRect(x, y, width, height);
    }

    checkCollision(rect) {
        const overlap = (
            rect.x < this.x + this.width &&
            rect.x + rect.width > this.x &&
            (rect.y < this.gapY || rect.y + rect.height > this.gapY + this.gap)
        );
        return overlap;
    }

    checkPassed(playerX) {
        if (!this.scored && this.x + this.width < playerX) {
            this.scored = true;
            return true;
        }
        return false;
    }
}

// Enemy class
class Enemy {
    constructor() {
        const level = levels[currentLevel];
        this.size = gameSettings.enemy_size;
        this.x = canvas.width;
        this.y = Math.random() * (canvas.height - this.size - 100) + 50;
        this.speed = level.enemy_speed;
        this.shootInterval = level.enemy_shoot_interval;
        this.lastShot = Date.now();
        this.scored = false;
    }

    update() {
        this.x -= this.speed;
        
        // Shoot projectiles
        if (Date.now() - this.lastShot > this.shootInterval) {
            this.shoot();
            this.lastShot = Date.now();
        }
    }

    shoot() {
        projectiles.push(new Projectile(this.x, this.y + this.size / 2));
        if (audio.enemy) audio.enemy.play().catch(() => {});
    }

    draw() {
        ctx.drawImage(images.enemy, this.x, this.y, this.size, this.size);
    }

    checkCollision(rect) {
        return (
            rect.x < this.x + this.size &&
            rect.x + rect.width > this.x &&
            rect.y < this.y + this.size &&
            rect.y + rect.height > this.y
        );
    }
}

// Projectile class
class Projectile {
    constructor(x, y) {
        const level = levels[currentLevel];
        this.x = x;
        this.y = y;
        this.size = gameSettings.projectile_size;
        this.speed = level.projectile_speed;
    }

    update() {
        this.x -= this.speed;
    }

    draw() {
        ctx.fillStyle = '#FF4444';
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size / 2, 0, Math.PI * 2);
        ctx.fill();
        
        // Glow effect
        ctx.strokeStyle = 'rgba(255, 68, 68, 0.5)';
        ctx.lineWidth = 3;
        ctx.stroke();
    }

    checkCollision(rect) {
        const centerX = this.x;
        const centerY = this.y;
        const radius = this.size / 2;
        
        const closestX = Math.max(rect.x, Math.min(centerX, rect.x + rect.width));
        const closestY = Math.max(rect.y, Math.min(centerY, rect.y + rect.height));
        
        const distanceX = centerX - closestX;
        const distanceY = centerY - closestY;
        
        return (distanceX * distanceX + distanceY * distanceY) < (radius * radius);
    }
}

// Coin class
class Coin {
    constructor() {
        const level = levels[currentLevel];
        this.size = gameSettings.coin_size;
        this.x = canvas.width;
        this.y = Math.random() * (canvas.height - this.size - 100) + 50;
        this.speed = level.coin_speed;
        this.angle = 0;
        this.collected = false;
    }

    update() {
        this.x -= this.speed;
        this.angle += 5;
    }

    draw() {
        ctx.save();
        ctx.translate(this.x + this.size / 2, this.y + this.size / 2);
        ctx.rotate((this.angle * Math.PI) / 180);
        
        // Draw coin
        ctx.fillStyle = '#FFD700';
        ctx.beginPath();
        ctx.arc(0, 0, this.size / 2, 0, Math.PI * 2);
        ctx.fill();
        
        // Inner circle
        ctx.fillStyle = '#FFA500';
        ctx.beginPath();
        ctx.arc(0, 0, this.size / 3, 0, Math.PI * 2);
        ctx.fill();
        
        // Symbol
        ctx.fillStyle = '#FFD700';
        ctx.font = `bold ${this.size / 2}px Arial`;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('$', 0, 0);
        
        ctx.restore();
    }

    checkCollision(rect) {
        return (
            rect.x < this.x + this.size &&
            rect.x + rect.width > this.x &&
            rect.y < this.y + this.size &&
            rect.y + rect.height > this.y
        );
    }
}

// Particle class for effects
class Particle {
    constructor(x, y, color) {
        this.x = x;
        this.y = y;
        this.vx = (Math.random() - 0.5) * 5;
        this.vy = (Math.random() - 0.5) * 5;
        this.life = 1.0;
        this.color = color;
        this.size = Math.random() * 5 + 2;
    }

    update() {
        this.x += this.vx;
        this.y += this.vy;
        this.life -= 0.02;
    }

    draw() {
        ctx.globalAlpha = this.life;
        ctx.fillStyle = this.color;
        ctx.fillRect(this.x, this.y, this.size, this.size);
        ctx.globalAlpha = 1.0;
    }
}

// Initialize game
async function init() {
    // Load config
    const response = await fetch('/api/config');
    config = await response.json();
    gameSettings = config.game_settings;
    levels = config.levels;
    
    // Load high score
    const hsResponse = await fetch('/api/highscore');
    const hsData = await hsResponse.json();
    highScore = hsData.high_score;
    document.getElementById('high-score').textContent = highScore;
    
    // Load images
    images.player.src = '/static/images/player.png';
    images.enemy.src = '/static/images/enemy.png';
    images.map.src = '/static/images/map.png';
    
    // Setup audio
    audio.bg.loop = true;
    audio.bg.volume = 0.3;
    
    // Event listeners
    document.getElementById('start-btn').addEventListener('click', startGame);
    document.getElementById('restart-btn').addEventListener('click', restartGame);
    document.getElementById('continue-btn').addEventListener('click', continueGame);
    
    document.addEventListener('keydown', handleKeyDown);
    canvas.addEventListener('click', handleClick);
    
    // Start game loop
    gameLoop();
}

// Start game
function startGame() {
    gameState = 'playing';
    score = 0;
    coins = 0;
    currentLevel = 0;
    frameCount = 0;
    
    player = new Player();
    walls = [];
    enemies = [];
    projectiles = [];
    coinsList = [];
    particles = [];
    
    lastWallTime = Date.now();
    lastEnemyTime = Date.now();
    lastCoinTime = Date.now();
    
    document.getElementById('start-screen').classList.add('hidden');
    
    // Start background music
    audio.bg.play().catch(() => {});
    
    updateUI();
}

// Restart game
function restartGame() {
    document.getElementById('gameover-screen').classList.add('hidden');
    startGame();
}

// Continue after level up
function continueGame() {
    document.getElementById('levelup-screen').classList.add('hidden');
    gameState = 'playing';
}

// Game over
function gameOver() {
    if (gameState === 'gameover') return;
    
    gameState = 'gameover';
    
    if (audio.gameover) audio.gameover.play().catch(() => {});
    audio.bg.pause();
    
    // Update high score
    if (score > highScore) {
        highScore = score;
        document.getElementById('new-high-score').classList.remove('hidden');
        
        // Save to server
        fetch('/api/highscore', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ score: score })
        });
    } else {
        document.getElementById('new-high-score').classList.add('hidden');
    }
    
    document.getElementById('final-score').textContent = score;
    document.getElementById('final-level').textContent = levels[currentLevel].name;
    document.getElementById('final-coins').textContent = coins;
    document.getElementById('gameover-screen').classList.remove('hidden');
}

// Level up
function levelUp() {
    if (currentLevel < levels.length - 1) {
        currentLevel++;
        gameState = 'levelup';
        
        document.getElementById('level-name').textContent = levels[currentLevel].name;
        document.getElementById('levelup-screen').classList.remove('hidden');
    }
}

// Handle input
function handleKeyDown(e) {
    if (gameState === 'playing') {
        if (e.code === 'Space' || e.code === 'ArrowUp') {
            e.preventDefault();
            player.flap();
        }
    }
}

function handleClick() {
    if (gameState === 'playing') {
        player.flap();
    }
}

// Update game
function update() {
    if (gameState !== 'playing') return;
    
    frameCount++;
    
    // Update player
    player.update();
    
    // Spawn walls
    const level = levels[currentLevel];
    if (Date.now() - lastWallTime > level.wall_spawn_interval) {
        walls.push(new Wall());
        lastWallTime = Date.now();
    }
    
    // Spawn enemies
    if (Date.now() - lastEnemyTime > level.enemy_spawn_interval) {
        enemies.push(new Enemy());
        lastEnemyTime = Date.now();
    }
    
    // Spawn coins
    if (Date.now() - lastCoinTime > level.coin_spawn_interval) {
        coinsList.push(new Coin());
        lastCoinTime = Date.now();
    }
    
    // Update walls
    walls = walls.filter(wall => {
        wall.update();
        
        if (wall.checkPassed(player.x)) {
            score += gameSettings.score_per_wall;
            updateUI();
        }
        
        if (wall.checkCollision(player.getRect())) {
            gameOver();
        }
        
        return wall.x + wall.width > 0;
    });
    
    // Update enemies
    enemies = enemies.filter(enemy => {
        enemy.update();
        
        if (enemy.checkCollision(player.getRect())) {
            if (!enemy.scored) {
                score += gameSettings.score_per_enemy;
                enemy.scored = true;
                createParticles(enemy.x, enemy.y, '#FF6B6B');
                updateUI();
            }
        }
        
        return enemy.x + enemy.size > 0;
    });
    
    // Update projectiles
    projectiles = projectiles.filter(projectile => {
        projectile.update();
        
        if (projectile.checkCollision(player.getRect())) {
            gameOver();
            return false;
        }
        
        return projectile.x > 0;
    });
    
    // Update coins
    coinsList = coinsList.filter(coin => {
        coin.update();
        
        if (!coin.collected && coin.checkCollision(player.getRect())) {
            coin.collected = true;
            coins++;
            score += gameSettings.score_per_coin;
            createParticles(coin.x, coin.y, '#FFD700');
            updateUI();
            return false;
        }
        
        return coin.x + coin.size > 0;
    });
    
    // Update particles
    particles = particles.filter(particle => {
        particle.update();
        return particle.life > 0;
    });
    
    // Check level up
    if (score >= level.required_score && currentLevel < levels.length - 1) {
        levelUp();
    }
}

// Draw game
function draw() {
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw background
    if (images.map.complete) {
        ctx.drawImage(images.map, 0, 0, canvas.width, canvas.height);
    } else {
        ctx.fillStyle = '#87CEEB';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
    }
    
    // Draw game objects
    walls.forEach(wall => wall.draw());
    enemies.forEach(enemy => enemy.draw());
    projectiles.forEach(projectile => projectile.draw());
    coinsList.forEach(coin => coin.draw());
    particles.forEach(particle => particle.draw());
    
    if (player && gameState !== 'start') {
        player.draw();
    }
}

// Game loop
function gameLoop() {
    update();
    draw();
    requestAnimationFrame(gameLoop);
}

// Update UI
function updateUI() {
    document.getElementById('current-score').textContent = score;
    document.getElementById('high-score').textContent = highScore;
    document.getElementById('level-display').textContent = levels[currentLevel].name;
    document.getElementById('coins-display').textContent = coins;
}

// Create particle effect
function createParticles(x, y, color) {
    for (let i = 0; i < 10; i++) {
        particles.push(new Particle(x, y, color));
    }
}

// Initialize when page loads
window.addEventListener('load', init);

