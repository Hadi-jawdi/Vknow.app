
// ── Timer ──
// ── Variables from template ──
let totalSeconds = timerMinutes * 60;
let answered = 0;
const total = questionsData.length;
alert("wored");
const timerEl = document.getElementById('timer');
const timerInterval = setInterval(() => {
  const m = Math.floor(totalSeconds / 60).toString().padStart(2, '0');
  const s = (totalSeconds % 60).toString().padStart(2, '0');
  timerEl.textContent = m + ':' + s;
  if (totalSeconds <= 60) timerEl.classList.add('bg-warning');
  if (totalSeconds <= 0) {
    clearInterval(timerInterval);
    submitTest();
  }
  totalSeconds--;
}, 1000);

// ── Option selection ──
document.querySelectorAll('.option-label').forEach(function(label) {
  label.addEventListener('click', function() {
    const radio = label.querySelector('.option-radio');
    const name = radio.name;
    document.querySelectorAll('input[name="' + name + '"]').forEach(function(r) {
      r.closest('.option-label').classList.remove('selected');
    });
    radio.checked = true;
    label.classList.add('selected');
    updateProgress();
  });
});

// ── Progress ──
function updateProgress() {
  answered = document.querySelectorAll('.option-radio:checked').length;
  const pct = (answered / total) * 100;
  document.getElementById('progress-bar').style.width = pct + '%';
}

// ── Submit ──
document.getElementById('submit-btn').addEventListener('click', submitTest);

async function submitTest() {
  clearInterval(timerInterval);

  const answers = {};
  questionsData.forEach(function(q) {
    const checked = document.querySelector('input[name="q_' + q.id + '"]:checked');
    if (checked) answers[q.id] = checked.value;
  });

  const res = await fetch(submitUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
    },
    body: JSON.stringify({ answers: answers, subject: subject, difficulty: difficulty })
  });

  const data = await res.json();
  showResults(data);
}

// ── Show Results ──
function showResults(data) {
  let html = '<div class="text-center mb-4">';
  const scoreClass = data.percentage >= 50 ? 'text-success' : 'text-danger';
  html += '<div class="display-4 fw-bold ' + scoreClass + '">' + data.score + '/' + data.total + '</div>';
  html += '<div class="fs-5 text-muted">' + data.percentage + '% درست</div>';
  html += '</div><hr>';

  data.results.forEach(function(r, i) {
    html += '<div class="mb-4">';
    html += '<p class="fw-semibold">' + (i + 1) + '. ' + r.question + '</p>';
    html += '<div class="d-flex flex-column gap-1">';

    r.options.forEach(function(opt, idx) {
      const optNum = idx + 1;
      let cls = 'border rounded p-2';
      if (optNum === r.correct_option) cls += ' bg-success text-white';
      else if (optNum === r.selected && !r.is_correct) cls += ' bg-danger text-white';
      html += '<div class="' + cls + '">' + optNum + '. ' + opt + '</div>';
    });

    html += '</div></div>';
  });

  document.getElementById('results-body').innerHTML = html;
  new bootstrap.Modal(document.getElementById('resultsModal')).show();
}