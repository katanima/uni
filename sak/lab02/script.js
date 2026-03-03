class Hand {
    // zainicjuj parametry bazowe
    constructor(ctx, length, width) {
        this.ctx = ctx;
        this.length = length;
        this.width = width;
    }

    // wyrenderuj wskazówkę poprzez obrót canvas
    draw(angle) {
        this.ctx.save();
        this.ctx.rotate(angle);
        this.ctx.beginPath();
        this.ctx.lineWidth = this.width;
        this.ctx.moveTo(0, 0);
        this.ctx.lineTo(0, -this.length);
        this.ctx.stroke();
        this.ctx.restore();
    }
}

class Clock {
    constructor() {
        this.canvas = document.getElementById("canvas");
        this.ctx = this.canvas.getContext("2d");
        this.radius = this.canvas.width / 2;

        this.ctx.translate(this.radius, this.radius);

        // utworzenie wskazówek
        this.secondHand = new Hand(this.ctx, this.radius * 0.9, 2);
        this.minuteHand = new Hand(this.ctx, this.radius * 0.7, 4);
        this.hourHand   = new Hand(this.ctx, this.radius * 0.5, 6);

        this.running = true;
        this.frameId = null;
        this.offset = 0;
        this.pauseTime = 0;
        this.startTime = Date.now();
    }

    // rysuj tarczę zegara
    drawFace() {
        this.ctx.beginPath();
        this.ctx.arc(0, 0, this.radius - 5, 0, 2 * Math.PI);
        this.ctx.stroke();
    }

    animate() {
        if (!this.running) return;

        const date = new Date();

        // pobierz aktualną godzinę
        const sec = date.getUTCSeconds();
        const min = date.getUTCMinutes();
        const hour = date.getUTCHours();

        this.ctx.clearRect(-this.radius, -this.radius, this.canvas.width, this.canvas.height);

        this.drawFace();

        // oblicz nachylenie wskazówek
        const secAngle = sec * Math.PI / 30;
        const minAngle = min * Math.PI / 30;
        const hourAngle = hour * Math.PI / 6 + min * Math.PI / 360;

        // renderuj wskazówki
        this.secondHand.draw(secAngle);
        this.minuteHand.draw(minAngle);
        this.hourHand.draw(hourAngle);

        this.frameId = requestAnimationFrame(() => this.animate());
    }

    // zapauzuj zegar
    pause() {
        if (!this.running) return;
        this.running = false;
        cancelAnimationFrame(this.frameId);
    }

    // wznów zegar
    resume() {
        if (this.running) return;
        this.running = true;
        this.animate();
    }

    // przełączanie stanów
    toggle() {
        this.running ? this.pause() : this.resume();
    }
}

const clock = new Clock();
clock.animate();

// sprawdź czy została wciśnieta spacja
// jeśli tak, przełącz stan
document.addEventListener("keydown", function(e) {
    if (e.code === "Space") {
        e.preventDefault();
        clock.toggle();
    }
});