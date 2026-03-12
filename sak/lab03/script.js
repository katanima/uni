
    (function() {
    class Particle {
        constructor() {
            this.x = 0;
            this.y = 0;
            this.vx = 0;
            this.vy = 0;
            this.hue = 0;
            this.alpha = 1.0;
            this.decay = 0.015;
            this.active = false;
        }

        // reinicjalizacja cząsteczek
        init(x, y, vx, vy, hue, alpha = 1.0, decay = 0.015) {
            this.x = x;
            this.y = y;
            this.vx = vx;
            this.vy = vy;
            this.hue = hue;
            this.alpha = alpha;
            this.decay = decay;
            this.active = true;
        }

        update(gravity, canvasHeight) {
            if (!this.active) return;
            this.x += this.vx;
            this.y += this.vy;

            // grawitacja i opór powietrza
            this.vy += gravity;
            this.vx *= 0.98;
            this.vy *= 0.98;

            // zanikanie
            this.alpha -= this.decay;

            // kolizja z podłożem
            if (this.y >= canvasHeight) {
                this.y = canvasHeight;
                this.vy *= -0.6;
                this.vx *= 0.9;
            }

            // dezaktywacja
            if (this.alpha <= 0.02) {
                this.active = false;
            }
        }

        draw(ctx) {
            if (!this.active) return;
            ctx.fillStyle = `hsla(${this.hue}, 100%, 60%, ${this.alpha})`;
            ctx.beginPath();
            ctx.arc(this.x, this.y, 2.8, 0, Math.PI * 2);
            ctx.fill();
        }
    }

    class Firework {
    constructor(startX, startY, targetX, targetY, baseHue = null) {
    this.x = startX;
    this.y = startY;
    this.targetX = targetX;
    this.targetY = targetY;

    // losowanie koloru
    this.baseHue = (baseHue !== null) ? baseHue : Math.random() * 360;

    // prędkość rakiety
    const speed = 9;
    const dx = targetX - startX;
    const dy = targetY - startY;
    const dist = Math.hypot(dx, dy);
    if (dist < 0.1) {
    // zabezpieczenie przed dzieleniem przez zero
    this.vx = 0;
    this.vy = 0;
} else {
    this.vx = (dx / dist) * speed;
    this.vy = (dy / dist) * speed;
}

    this.exploded = false;
    this.active = true;
}

    // sprawdza czy dotarła do celu
    update(gravity, canvasHeight) {
    if (this.exploded || !this.active) return;

    // przesuń rakietę
    this.x += this.vx;
    this.y += this.vy;

    // mały opór
    this.vx *= 0.995;
    this.vy *= 0.995;

    // czy osiągnęła cel?
    const distToTarget = Math.hypot(this.targetX - this.x, this.targetY - this.y);
    if (distToTarget < 8 || this.y >= canvasHeight - 2) {
    this.exploded = true;
    this.active = false;
}
}

    // generuje cząsteczki eksplozji
    explode(particleCount = 80) {
    const particles = [];
    const hueVariation = 30;   // ±30

    for (let i = 0; i < particleCount; i++) {
    // losowy kąt w radianach
    const angle = Math.random() * Math.PI * 2;
    const speed = 2 + Math.random() * 6;
    const vx = Math.cos(angle) * speed;
    const vy = Math.sin(angle) * speed;

    // losowanie kolor
    const hueOffset = (Math.random() * hueVariation * 2) - hueVariation;
    let hue = (this.baseHue + hueOffset) % 360;
    if (hue < 0) hue += 360;

    // stwórz cząstkę
    const p = new Particle();
    const decay = 0.01 + Math.random() * 0.02;
    p.init(this.x, this.y, vx, vy, hue, 1.0, decay);
    particles.push(p);
}
    return particles;
}

    draw(ctx) {
    if (!this.active || this.exploded) return;
    // rysuj rakietę jako jasną kropkę
    ctx.fillStyle = `hsl(${this.baseHue}, 100%, 70%)`;
    ctx.beginPath();
    ctx.arc(this.x, this.y, 4, 0, 2 * Math.PI);
    ctx.fill();
    // mały ogon
    ctx.fillStyle = 'rgba(255, 180, 0, 0.7)';
    ctx.beginPath();
    ctx.arc(this.x - this.vx * 0.7, this.y - this.vy * 0.7, 2.5, 0, 2 * Math.PI);
    ctx.fill();
}
}

    class FireworkShow {
    constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');

    // tablice
    this.particles = [];
    this.rockets = [];

    // parametry
    this.gravity = 0.15;
    this.particleCount = 120;

    // ustawienia automatycznego pokazu
    this.autoFireInterval = 1200;
    this.lastAutoFire = performance.now();

    // obsługa zdarzeń myszy
    this.canvas.addEventListener('click', (e) => this.handleClick(e));

    this.setupSliders();

    // start pętli animacji
    this.animate = this.animate.bind(this);
    this.animate();
}

    handleClick(e) {
    const rect = this.canvas.getBoundingClientRect();
    const scaleX = this.canvas.width / rect.width;
    const scaleY = this.canvas.height / rect.height;

    const mouseX = (e.clientX - rect.left) * scaleX;
    const mouseY = (e.clientY - rect.top) * scaleY;

    const startX = mouseX;
    const startY = this.canvas.height;

    // stwórz rakietę
    const newFirework = new Firework(startX, startY, mouseX, mouseY);
    this.rockets.push(newFirework);
}

    setupSliders() {
    const gravitySlider = document.getElementById('gravitySlider');
    const countSlider = document.getElementById('countSlider');

    gravitySlider.addEventListener('input', (e) => {
    this.gravity = parseFloat(e.target.value);
});

    countSlider.addEventListener('input', (e) => {
    this.particleCount = parseInt(e.target.value, 10);
});
}

    // automatyczne odpalanie fajerwerków
    autoFire(now) {
    if (now - this.lastAutoFire > this.autoFireInterval) {
    this.lastAutoFire = now;

    // losowa pozycja X w granicach canvas
    const randX = 100 + Math.random() * (this.canvas.width - 200);
    const randY = 100 + Math.random() * (this.canvas.height - 200);

    // start z dołu
    const startX = randX;
    const startY = this.canvas.height;

    // losowy odcień
    const hue = Math.random() * 360;
    const rocket = new Firework(startX, startY, randX, randY, hue);
    this.rockets.push(rocket);
}
}

    updateAndDraw() {
    const ctx = this.ctx;
    const canvas = this.canvas;

    ctx.fillStyle = 'rgba(0, 0, 0, 0.25)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.globalCompositeOperation = 'source-over';

    for (let i = this.rockets.length - 1; i >= 0; i--) {
    const r = this.rockets[i];
    r.update(this.gravity, canvas.height);
    r.draw(ctx);

    // jeśli wybuchła
    if (r.exploded) {
    const newParticles = r.explode(this.particleCount);
    this.particles.push(...newParticles);
    // rakieta zostanie usunięta przez filter
}
}

    // usuń nieaktywne rakiety
    this.rockets = this.rockets.filter(r => r.active && !r.exploded);

    ctx.globalCompositeOperation = 'lighter';

    // aktualizuj i rysuj cząsteczki
    for (let p of this.particles) {
    p.update(this.gravity, canvas.height);
    p.draw(ctx);
}

    // usuń nieaktywne cząsteczki
    this.particles = this.particles.filter(p => p.active);

    ctx.globalCompositeOperation = 'source-over';

    // aktualizacja liczników w UI
    document.getElementById('rocketCount').innerText = this.rockets.length;
    document.getElementById('particleCount').innerText = this.particles.length;
}

    animate(timestamp) {
    this.autoFire(timestamp);

    this.updateAndDraw();
    requestAnimationFrame(this.animate);
}
}

    window.addEventListener('load', () => {
    const canvas = document.getElementById('fireworksCanvas');
    new FireworkShow(canvas);
});

})();