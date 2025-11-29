
(() => {
  const canvas = document.getElementById('game');
  const ctx = canvas.getContext('2d');
  const W = canvas.width, H = canvas.height;

  // Power-upy
  let flyingUnlocked = false;
  let flyPressed = false;

  // Barvy (výchozí)
  let bgColor = '#f1f5f9';       // světle šedá (místo čistého clear)
  let obstacleColor = '#334155'; // tmavší šedomodrá
  let flashTimer = 0;            // pro blikání barev od 700 bodů


  const playerImg = new Image();
  playerImg.src = "/static/player.png";  // ← GIF!

  // Hráč
  const player = {
    x: 60, y: H-60, w: 36, h: 36,
    vy: 0, onGround: true
  };

  // Fyzika
  const GRAV = 0.8;
  const JUMP = -13;

  // Překážky
  let obstacles = [];
  let speed = 6;          // rychlost posunu scény
  let spawnTimer = 0;
  let spawnEvery = 60;    // snímky (cca 1s při 60fps)

  // Skóre
  let score = 0;
  let best = 0;
  let alive = true;

  // UI
  const scoreEl = document.getElementById('score');

  // ZVEŘEJNĚNÉ „HACK“ FUNKCE PRO DEMO (úmyslně zranitelné)
  window.setScore = function(n) {
    score = Math.max(0, Number(n) || 0);
    scoreEl.textContent = Math.floor(score);
    console.log("[DEV] score =", score);
  };

  window.cheat = function(n) {
    if (typeof n !== "undefined") window.setScore(n);
    submitScore(score);
    console.log("[DEV] odesláno na server:", Math.floor(score));
  };

  // Volitelné: ať vidí dostupné API při F1
  window.help = function() {
    console.log("Dostupné: setScore(n), cheat(n?), help()");
  };

  function randInt(a,b){ return Math.floor(Math.random()*(b-a+1))+a; }
  function randomPastel(){
    const r = randInt(160, 230), g = randInt(160, 230), b = randInt(160, 230);
    return `rgb(${r},${g},${b})`;
  }
  function randomDark(){
    const r = randInt(30, 90), g = randInt(30, 90), b = randInt(30, 90);
    return `rgb(${r},${g},${b})`;
  }

  function resetGame() {
    obstacles = [];
    speed = 6;
    spawnTimer = 0;
    spawnEvery = 60;
    score = 0;
    player.y = H-60;
    player.vy = 0;
    player.onGround = true;
    alive = true;
  }

  function spawnObstacle() {
    // náhodně nízký kaktus nebo vyšší překážka
    const type = Math.random() < 0.75 ? 'low' : 'mid';
    const h = (type === 'low') ? 30 : 50;
    const w = (type === 'low') ? 16+Math.random()*16 : 18+Math.random()*18;
    obstacles.push({
      x: W + 10, y: H - 24 - h, w, h
    });
  }

  function rect(x,y,w,h,color){
    ctx.fillStyle = color;
    ctx.fillRect(x,y,w,h);
  }

  function collide(a,b){
    return !(a.x + a.w < b.x || a.x > b.x + b.w || a.y + a.h < b.y || a.y > b.y + b.h);
  }

  // Input
  window.addEventListener('keydown', (e) => {
    if ((e.code === 'Space' || e.code === 'ArrowUp') && alive) {
      if (player.onGround) {
        player.vy = JUMP;
        player.onGround = false;
      }
      e.preventDefault();
    }
    if (e.key === 'r' || e.key === 'R') {
      resetGame();
    }
  });

  window.addEventListener('keydown', (e) => {
    if ((e.code === 'Space' || e.code === 'ArrowUp') && alive) {
      flyPressed = true; // ← NEW: držím „let“
      if (player.onGround) {           // stále umožňujeme klasický skok
        player.vy = JUMP;
        player.onGround = false;
      }
      e.preventDefault();
    }
    if (e.key === 'r' || e.key === 'R') {
      resetGame();
    }
  });

  window.addEventListener('keyup', (e) => {
    if (e.code === 'Space' || e.code === 'ArrowUp') {
      flyPressed = false; // ← NEW
    }
  });


  function update(){
    if (!alive) return;

    // Odemkni let od 500 bodů
    if (!flyingUnlocked && score >= 500) {
      flyingUnlocked = true;
    }

    // Fyzika skoku/letu
    player.vy += GRAV;

    // Tah nahoru při letu (držený Space/↑), omezený, ať „nevyletí“ příliš rychle
    if (flyingUnlocked && flyPressed) {
      player.vy += -0.6;                // jemný tah nahoru
      if (player.vy < -8) player.vy = -8; // cap maximální rychlosti vzhůru
    }

    player.y += player.vy;

    // Podlaha + strop
    const groundY = H - 24 - player.h;
    if (player.y >= groundY) {
      player.y = groundY;
      player.vy = 0;
      player.onGround = true;
    }
    if (player.y < 8) {                 // jednoduchý „strop“
      player.y = 8;
      if (player.vy < 0) player.vy = 0;
    }

    // Spawn překážek (beze změny)
    spawnTimer--;
    if (spawnTimer <= 0) {
      spawnObstacle();
      spawnTimer = spawnEvery + Math.floor(Math.random() * 40) - 10;
      if (spawnTimer < 30) spawnTimer = 30;
    }

    // Posun překážek
    for (const o of obstacles) o.x -= speed;
    obstacles = obstacles.filter(o => o.x + o.w > -20);

    // Kolize
    for (const o of obstacles) {
      if (collide(player, o)) {
        gameOver();
      }
    }

    // Skóre + zvyšování rychlosti
    score += 0.1 * speed;
    speed += 0.0008;
    if (spawnEvery > 40) spawnEvery -= 0.01;

    // NEW: Blikání barev po 700 bodech (cca každých ~10 snímků změň paletu)
    if (score >= 700) {
      flashTimer++;
      if (flashTimer % 10 === 0) {
        bgColor = randomPastel();
        obstacleColor = randomDark();
      }
    } else {
      // Před 700 body držíme výchozí barvy (kdyby hráč restartoval apod.)
      bgColor = '#f1f5f9';
      obstacleColor = '#334155';
    }

    scoreEl.textContent = Math.floor(score);
  }


  function draw(){
    // Pozadí: vyplň barvou (místo pouhého clearRect)
    ctx.fillStyle = bgColor;                 // ← NEW
    ctx.fillRect(0,0,W,H);                   // ← NEW

    // Zem
    rect(0, H-24, W, 4, '#94a3b8');

    // Hráč
    // Hráč
    if (playerImg.complete) {
        ctx.drawImage(playerImg, player.x, player.y, player.w, player.h);
    } else {
        rect(player.x, player.y, player.w, player.h, '#111827');
    }

    // Překážky – s měnící se barvou
    ctx.fillStyle = obstacleColor;           // ← NEW
    for (const o of obstacles) ctx.fillRect(o.x, o.y, o.w, o.h);

    // Nápisy
    ctx.fillStyle = '#0f172a';
    ctx.font = '16px system-ui, -apple-system, Segoe UI, Roboto, Arial';
    ctx.fillText(`Best: ${best}`, W-120, 24);

    // Indikátor letu
    if (flyingUnlocked && alive) {
      ctx.fillStyle = '#065f46';
      ctx.font = 'bold 14px system-ui, -apple-system, Segoe UI, Roboto, Arial';
      ctx.fillText('LET AKTIVNÍ (drž SPACE/↑)', 16, 24);
    }

    if (!alive) {
      ctx.fillStyle = 'rgba(0,0,0,0.5)';
      ctx.fillRect(0,0,W,H);
      ctx.fillStyle = '#fff';
      ctx.font = 'bold 28px system-ui, -apple-system, Segoe UI, Roboto, Arial';
      ctx.fillText('KONEC HRY', W/2 - 90, H/2 - 10);
      ctx.font = '16px system-ui, -apple-system, Segoe UI, Roboto, Arial';
      ctx.fillText('Stiskni R pro restart', W/2 - 90, H/2 + 20);
    }
  }


  function loop(){
    update();
    draw();
    requestAnimationFrame(loop);
  }
// úplně nahoře v game.js:
const USER =
  (typeof window !== 'undefined' && window.GAME_USER) ||
  new URLSearchParams(location.search).get('user') ||
  'Host';


  // --- odeslání skóre na server (po Game Over i průběžně) ---
  async function submitScore(current) {
    try {
      await fetch("/score", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ user: USER, score: Math.floor(current) })
      });
    } catch (e) {
      // tiché selhání – offline režim
    }
  }

  // posílej průběžně každé 3 s, ať se žebříček hýbe i bez konce hry
  setInterval(() => { if (alive) submitScore(score); }, 3000);

  // po Game Over pošli finální skóre
  function gameOver() {
    alive = false;
    best = Math.max(best, score|0);
    submitScore(score);
  }

  // --- živý žebříček přes Server-Sent Events ---
  const lb = document.getElementById('leaderboard');
  const es = new EventSource("/scores_stream");
  es.onmessage = (ev) => {
    try {
      const data = JSON.parse(ev.data);
      const list = data.leaderboard || [];
      lb.innerHTML = list.map((row, i) =>
        `<li class="flex justify-between">
           <span class="text-slate-700">${i+1}. ${escapeHtml(row.user)}</span>
           <span class="font-semibold tabular-nums">${row.score}</span>
         </li>`).join("") || '<li class="text-slate-500">Zatím žádná skóre.</li>';
    } catch {}
  };

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, (c) => ({ "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;" }[c]));
  }


  resetGame();
  loop();
})();