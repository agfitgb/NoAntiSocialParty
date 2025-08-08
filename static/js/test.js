// test.js - 공용 스크립트 (index/test/result 각 페이지에서 일부 사용)
(function(){
  // test 페이지 전용 로직 (window.POL_QUESTIONS 가 전달됨)
  if(typeof window.POL_QUESTIONS !== 'undefined') {
    const questions = window.POL_QUESTIONS;
    let idx = 0;
    let answers = Array(questions.length).fill(null);
    const qcount = document.getElementById('qcount');
    const area = document.getElementById('questionArea');
    const bar = document.getElementById('bar');
    const nextBtn = document.getElementById('nextBtn');

    function render(){
      const q = questions[idx];
      qcount.innerText = (idx+1) + ' / ' + questions.length;
      area.innerHTML = `
        <div class="question">
          <div class="qtitle">${q.q}</div>
          <div class="small">1: 강하게 비동의 — 5: 강하게 동의</div>
          <div class="options">${[1,2,3,4,5].map(n=>`<button class="optbtn" data-val="${n}">${n}</button>`).join('')}</div>
        </div>`;
      attach();
      updateProgress();
    }
    function attach(){
      document.querySelectorAll('.optbtn').forEach(b=>{
        b.addEventListener('click', ()=>{
          const val = Number(b.dataset.val);
          answers[idx] = val;
          document.querySelectorAll('.optbtn').forEach(x=>{ x.style.borderColor = 'rgba(255,255,255,0.04)'; x.style.background='transparent' });
          b.style.borderColor = 'rgba(124,58,237,0.9)'; b.style.background = 'rgba(124,58,237,0.12)';
        });
      });
    }
    function updateProgress(){
      const filled = answers.filter(a=>a!==null).length;
      const pct = Math.round((filled/questions.length)*100);
      bar.style.width = pct + '%';
    }
    nextBtn.addEventListener('click', async ()=>{
      if(answers[idx]===null){ alert('먼저 답을 선택하세요'); return; }
      idx++;
      if(idx>=questions.length){
        // 제출
        const res = await fetch('/submit', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({answers})});
        const j = await res.json();
        location.href = '/result?id=' + j.id;
      } else {
        render();
      }
    });
    render();
  }
})();
