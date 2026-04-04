// Navigation
const pageMap = {
  'page-home': 'tab-home', 'page-book': 'tab-book',
  'page-price': 'tab-price', 'page-promo': 'tab-promo', 'page-profile': 'tab-profile'
};
function goPage(id) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  if (pageMap[id]) document.getElementById(pageMap[id]).classList.add('active');
  window.scrollTo(0, 0);
  if (id === 'page-book') showStep(1);
}
// Booking steps
function showStep(n) {
  document.querySelectorAll('.step-page').forEach(s => s.classList.remove('active'));
  const el = document.getElementById('step-' + n);
  if (el) { el.classList.add('active'); window.scrollTo(0,0); }
}
function nextStep(n) { showStep(n); }
function prevStep(n) { showStep(n); }
function showSuccess() {
  document.querySelectorAll('.step-page').forEach(s => s.classList.remove('active'));
  document.getElementById('step-success').classList.add('active');
  window.scrollTo(0,0);
}
function selectBarber(el) { document.querySelectorAll('.barber-row').forEach(r => r.classList.remove('sel')); el.classList.add('sel'); }
function selSlot(el) { document.querySelectorAll('.slot:not(.busy)').forEach(s => s.classList.remove('sel')); el.classList.add('sel'); }
function selSvc(el) { document.querySelectorAll('.svc-row').forEach(s => s.classList.remove('sel')); el.classList.add('sel'); }
function filterCat(el) { document.querySelectorAll('.ctab').forEach(t => t.classList.remove('active')); el.classList.add('active'); }
// Build dates
function buildDates() {
  const days=['Вс','Пн','Вт','Ср','Чт','Пт','Сб'], months=['янв','фев','мар','апр','май','июн','июл','авг','сен','окт','ноя','дек'];
  const wrap = document.getElementById('dateScroll');
  if (!wrap) return;
  const today = new Date();
  for (let i=0; i<14; i++) {
    const d = new Date(today); d.setDate(today.getDate()+i);
    const c = document.createElement('div');
    c.className = 'date-chip' + (i===0?' sel':'');
    c.innerHTML = `<div class="dc-day">${days[d.getDay()]}</div><div class="dc-num">${d.getDate()}</div><div class="dc-mon">${months[d.getMonth()]}</div>`;
    c.onclick = () => { document.querySelectorAll('.date-chip').forEach(x=>x.classList.remove('sel')); c.classList.add('sel'); };
    wrap.appendChild(c);
  }
}
buildDates();
// Toast
let tt;
function showToast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg; t.classList.add('show');
  clearTimeout(tt); tt = setTimeout(()=>t.classList.remove('show'), 2200);
}
// Telegram WebApp
if (window.Telegram?.WebApp) { Telegram.WebApp.ready(); Telegram.WebApp.expand(); }
