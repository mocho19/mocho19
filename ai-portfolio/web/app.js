'use strict';
let apps = [], selected = null, lastResult = null;
const $ = id => document.getElementById(id);
const icons = ['⌕', '◈', '▤', '⌁', '§', '↗', '☷'];
const pretty = value => JSON.stringify(value, null, 2);
function node(tag, text, className) { const el = document.createElement(tag); if (text !== undefined) el.textContent = text; if (className) el.className = className; return el; }
function route() {
  const slug = location.hash.slice(1); selected = apps.find(app => app.slug === slug);
  $('overview').hidden = !!selected; $('workspace').hidden = !selected;
  document.querySelectorAll('.nav-item').forEach(el => el.classList.toggle('active', el.dataset.slug === slug));
  $('crumb').textContent = selected ? selected.title.toUpperCase() : 'OVERVIEW';
  if (!selected) return;
  $('skill').textContent = selected.skill.toUpperCase(); $('app-title').textContent = selected.title;
  $('app-description').textContent = selected.description; $('number').textContent = String(apps.indexOf(selected) + 1).padStart(2, '0');
  $('input-label').textContent = selected.input_label; $('input').value = selected.example_input;
  resetResult(); count();
}
function count() { $('char-count').textContent = `${$('input').value.length.toLocaleString()} / 16,000`; }
function resetResult() { $('result').hidden = true; $('error').hidden = true; $('empty-result').hidden = false; $('result-badge').textContent = 'READY'; lastResult = null; }
function renderData(data) {
  $('data').replaceChildren();
  for (const [key, value] of Object.entries(data || {})) {
    const section = node('section', undefined, 'datum'); section.append(node('h3', key.replaceAll('_', ' ')));
    if (Array.isArray(value) && value.every(x => typeof x === 'string')) { const list = node('ul'); value.forEach(x => list.append(node('li', x))); section.append(list); }
    else if (typeof value === 'string') section.append(node('p', value));
    else section.append(node('pre', pretty(value)));
    $('data').append(section);
  }
}
$('input').addEventListener('input', count);
$('reset').addEventListener('click', () => { if (selected) { $('input').value = selected.example_input; resetResult(); count(); } });
$('mode').addEventListener('change', () => { $('mode-note').textContent = $('mode').value === 'live' ? 'Sends input to your Foundry deployment. Model usage is billed by Azure.' : 'Runs locally. No model calls or external changes.'; });
$('run').addEventListener('click', async () => {
  if (!selected || !$('input').value.trim()) return;
  const slug = selected.slug; const button = $('run'); button.disabled = true; button.textContent = 'Processing workflow…';
  $('error').hidden = true; $('result-badge').textContent = 'RUNNING';
  try {
    const response = await fetch('/api/run', {method:'POST', headers:{'Content-Type':'application/json', 'X-Portfolio-Request':'1'}, body:JSON.stringify({project:slug, live:$('mode').value === 'live', payload:{text:$('input').value, as_of:$('as-of').value || '2026-11-22'}})});
    const result = await response.json(); if (!response.ok) throw new Error(result.error || 'Request failed');
    if (!selected || selected.slug !== slug) return;
    lastResult = result; $('empty-result').hidden = true; $('result').hidden = false;
    $('summary').textContent = result.summary; renderData(result.data);
    $('sources').textContent = pretty(result.sources || []); $('trace').textContent = pretty(result.trace || []); $('raw').textContent = pretty(result);
    $('result-badge').textContent = result.mode === 'foundry-live' ? 'FOUNDRY LIVE' : 'OFFLINE COMPLETE';
  } catch (error) { if (selected && selected.slug === slug) { $('error').textContent = error.message; $('error').hidden = false; $('result-badge').textContent = 'CHECK INPUT'; } }
  finally { button.disabled = false; button.replaceChildren(document.createTextNode('Run workflow '), node('span', '↗')); }
});
$('download').addEventListener('click', () => { if (!lastResult) return; const url = URL.createObjectURL(new Blob([pretty(lastResult)], {type:'application/json'})); const a = node('a'); a.href = url; a.download = `${lastResult.project}-result.json`; a.click(); URL.revokeObjectURL(url); });
async function init() {
  try {
    const response = await fetch('/api/apps'); if (!response.ok) throw new Error('Could not load applications.');
    const catalog = await response.json(); apps = catalog.apps;
    $('mode').options[1].disabled = !catalog.live_enabled;
    apps.forEach((app, index) => {
      const nav = node('a', undefined, 'nav-item'); nav.href = `#${app.slug}`; nav.dataset.slug = app.slug; nav.append(node('span', String(index + 1).padStart(2, '0')), document.createTextNode(app.title)); $('nav').append(nav);
      const card = node('a', undefined, 'card'); card.href = `#${app.slug}`;
      const top = node('div', undefined, 'card-top'); top.append(node('span', `APPLICATION ${String(index + 1).padStart(2, '0')}`), node('span', icons[index], 'card-icon'));
      const bottom = node('div', undefined, 'card-bottom'); bottom.append(node('span', app.skill, 'tag'), node('span', '↗', 'card-arrow'));
      card.append(top, node('h3', app.title), node('p', app.description), bottom); $('cards').append(card);
    }); route();
  } catch (error) { $('cards').append(node('p', error.message, 'error')); }
}
window.addEventListener('hashchange', route); init();
