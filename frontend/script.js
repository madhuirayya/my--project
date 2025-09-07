console.log('script.js loaded successfully');
const API = (path) => `http://localhost:8000${path}`;

async function createCollege(){
  const name = document.getElementById('collegeName').value;
  const r = await fetch(API('/colleges'), {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({name})});
  alert(await r.text());
  listColleges();
}
async function listColleges(){
  console.log('Fetching colleges...');
  try {
    const r = await fetch(API('/colleges'));
    const d = await r.json();
    console.log('Colleges data:', d);
    document.getElementById('collegeList').innerHTML = d.map(c=>`#${c.id} - ${c.name}`).join('<br>');
  } catch (error) {
    console.error('Error fetching colleges:', error);
  }
}
async function createStudent(){
  const name = document.getElementById('studentName').value.trim();
  const email = document.getElementById('studentEmail').value.trim();
  const college_id_str = document.getElementById('studentCollegeId').value.trim();

  if (!name) {
    alert('Student name is required.');
    return;
  }
  if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    alert('Please enter a valid email address.');
    return;
  }
  const college_id = parseInt(college_id_str);
  if (isNaN(college_id) || college_id <= 0) {
    alert('College ID must be a positive integer.');
    return;
  }

  const r = await fetch(API('/students'), {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({name,email,college_id})});
  const responseText = await r.text();
  if (r.ok) {
    alert('Student created successfully!');
    // Clear form
    document.getElementById('studentName').value = '';
    document.getElementById('studentEmail').value = '';
    document.getElementById('studentCollegeId').value = '';
    listStudents();  // Refresh student list after creation
  } else {
    alert('Error: ' + responseText);
  }
}

async function listStudents(){
  const r = await fetch(API('/students'));
  const d = await r.json();
  // Assuming you want to display the student list somewhere, e.g., in an element with id 'studentList'
  document.getElementById('studentList').innerHTML = d.map(s => `#${s.id} ${s.name} (${s.email})`).join('<br>');
}
async function handleCreateEvent(){
  console.log('handleCreateEvent function defined and called');
  const title = document.getElementById('eventTitle').value.trim();
  const type = document.getElementById('eventType').value.trim();
  const start_time = document.getElementById('eventStart').value.trim();
  const end_time = document.getElementById('eventEnd').value.trim();
  const college_id_str = document.getElementById('eventCollegeId').value.trim();
  const description = document.getElementById('eventDesc').value.trim();

  console.log('Form values:', {title, type, start_time, end_time, college_id_str, description});

  const college_id = parseInt(college_id_str);
  if (isNaN(college_id) || college_id <= 0) {
    alert('College ID must be a positive integer.');
    return;
  }

  if (!title) {
    alert('Event title is required.');
    return;
  }
  if (!type) {
    alert('Event type is required.');
    return;
  }
  if (!start_time) {
    alert('Event start time is required.');
    return;
  }
  if (!end_time) {
    alert('Event end time is required.');
    return;
  }

  if (new Date(start_time) >= new Date(end_time)) {
    alert('Event end time must be after start time.');
    return;
  }

  // Convert datetime-local input to ISO string with seconds and timezone
  const startISO = new Date(start_time).toISOString();
  const endISO = new Date(end_time).toISOString();

  try {
    const requestData = {title,type,start_time: startISO,end_time: endISO,college_id,description};
    console.log('Creating event with data:', requestData);
    console.log('Request URL:', API('/events'));
    console.log('Request body:', JSON.stringify(requestData));

    const r = await fetch(API('/events'), {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify(requestData)
    });

    console.log('Response status:', r.status);
    console.log('Response headers:', Object.fromEntries(r.headers.entries()));

    const responseText = await r.text();
    console.log('Event creation response text:', responseText);
    if (r.ok) {
      alert('Event created successfully!');
      // Clear form
      document.getElementById('eventTitle').value = '';
      document.getElementById('eventType').value = '';
      document.getElementById('eventStart').value = '';
      document.getElementById('eventEnd').value = '';
      document.getElementById('eventCollegeId').value = '';
      document.getElementById('eventDesc').value = '';
      loadEvents();
    } else {
      alert('Error: ' + responseText);
    }
  } catch (error) {
    console.error('Error during event creation:', error);
    alert('Error during event creation: ' + error.message);
  }
}
async function loadEvents(){
  console.log('Loading events...');
  try {
    const cid = document.getElementById('filterCollegeId').value;
    const type = document.getElementById('filterType').value;
    const url = new URL(API('/events'));
    if(cid) url.searchParams.set('college_id', cid);
    if(type) url.searchParams.set('type', type);
    console.log('Events URL:', url.toString());
    const r = await fetch(url);
    if (!r.ok) {
      throw new Error(`Failed to fetch events: ${r.status} ${r.statusText}`);
    }
    const d = await r.json();
    console.log('Events data:', d);
    document.getElementById('events').innerHTML = d.map(e => `
      <div class="border rounded p-2">
        <div class="font-semibold">#${e.id} ${e.title}</div>
        <div class="text-xs">${e.type} | ${new Date(e.start_time).toLocaleString()} - ${new Date(e.end_time).toLocaleString()}</div>
        <button class="mt-2 px-2 py-1 border rounded" onclick="eventStats(${e.id})">Stats</button>
        <div id="stats-${e.id}" class="text-xs mt-1"></div>
      </div>
    `).join('');
  } catch (error) {
    console.error('Error loading events:', error);
  }
}
async function eventStats(eventId){
  const r = await fetch(API(`/reports/event-stats/${eventId}`));
  const d = await r.json();
  document.getElementById(`stats-${eventId}`).innerText = `Regs: ${d.registrations} | Att: ${d.attendance} (${d.attendance_percent}%) | Avg⭐: ${d.avg_feedback ?? 'N/A'}`;
}
async function registerStudent(){
  const student_id = parseInt(document.getElementById('regStudentId').value);
  const event_id = parseInt(document.getElementById('regEventId').value);
  const r = await fetch(API('/register'), {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({student_id,event_id})});
  alert(await r.text());
}
async function markAttendance(){
  const student_id = parseInt(document.getElementById('regStudentId').value);
  const event_id = parseInt(document.getElementById('regEventId').value);
  const r = await fetch(API('/attendance'), {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({student_id,event_id})});
  alert(await r.text());
}
async function sendFeedback(){
  const student_id = parseInt(document.getElementById('regStudentId').value);
  const event_id = parseInt(document.getElementById('regEventId').value);
  const rating = parseInt(document.getElementById('fbRating').value);
  const comment = document.getElementById('fbComment').value;
  const r = await fetch(API('/feedback'), {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({student_id,event_id,rating,comment})});
  alert(await r.text());
}
async function loadPopularity(){
  const r = await fetch(API('/reports/event-popularity'));
  const d = await r.json();
  document.getElementById('popularity').innerHTML = d.map(x=>`${x.title} — ${x.registrations} regs`).join('<br>');
}
async function studentReport(){
  const sid = document.getElementById('studentReportId').value;
  const r = await fetch(API(`/reports/student-participation/${sid}`));
  const d = await r.json();
  document.getElementById('studentReport').innerText = `Registered: ${d.registered_events}, Attended: ${d.attended_events}`;
}
async function topActive(){
  const r = await fetch(API('/reports/top-active'));
  const d = await r.json();
  document.getElementById('topActive').innerHTML = d.map((s,i)=>`#${i+1} ${s.name} - ${s.attended} events`).join('<br>');
}
// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing...');
    listColleges();
    loadEvents();
});
