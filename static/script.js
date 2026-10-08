const form = document.getElementById("studentForm");
const table = document.getElementById("studentTable");
const search = document.getElementById("search");
const message = document.getElementById("message");
const studentId = document.getElementById("studentId");
const cancelEdit = document.getElementById("cancelEdit");
const formTitle = document.getElementById("formTitle");
const submitBtn = document.getElementById("submitBtn");

let students = [];

function showMessage(text, type = "success") {
  message.textContent = text;
  message.className = type;
  setTimeout(() => { message.textContent = ""; message.className = ""; }, 3000);
}

async function loadStudents() {
  const q = encodeURIComponent(search.value.trim());
  const response = await fetch(`/api/students?search=${q}`);
  students = await response.json();
  render();
}

function render() {
  table.innerHTML = "";
  document.getElementById("empty").style.display = students.length ? "none" : "block";

  students.forEach(s => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${escapeHtml(s.name)}</td>
      <td>${escapeHtml(s.roll_no)}</td>
      <td>${escapeHtml(s.class_name)}</td>
      <td>${Number(s.marks).toFixed(2)}</td>
      <td>${escapeHtml(s.contact)}</td>
      <td>
        <button class="edit" onclick="editStudent(${s.id})">Edit</button>
        <button class="delete" onclick="deleteStudent(${s.id})">Delete</button>
      </td>`;
    table.appendChild(row);
  });

  document.getElementById("total").textContent = students.length;
  const marks = students.map(s => Number(s.marks));
  document.getElementById("average").textContent =
    marks.length ? (marks.reduce((a,b) => a+b, 0) / marks.length).toFixed(2) : "0";
  document.getElementById("highest").textContent =
    marks.length ? Math.max(...marks).toFixed(2) : "0";
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, c => ({
    "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#039;"
  }[c]));
}

function editStudent(id) {
  const s = students.find(x => x.id === id);
  if (!s) return;
  studentId.value = s.id;
  document.getElementById("name").value = s.name;
  document.getElementById("roll_no").value = s.roll_no;
  document.getElementById("class_name").value = s.class_name;
  document.getElementById("marks").value = s.marks;
  document.getElementById("contact").value = s.contact;
  formTitle.textContent = "Update Student";
  submitBtn.textContent = "Update Student";
  cancelEdit.classList.remove("hidden");
  window.scrollTo({top: 0, behavior: "smooth"});
}

function resetForm() {
  form.reset();
  studentId.value = "";
  formTitle.textContent = "Add Student";
  submitBtn.textContent = "Add Student";
  cancelEdit.classList.add("hidden");
}

cancelEdit.addEventListener("click", resetForm);

form.addEventListener("submit", async e => {
  e.preventDefault();
  const payload = {
    name: document.getElementById("name").value.trim(),
    roll_no: document.getElementById("roll_no").value.trim(),
    class_name: document.getElementById("class_name").value.trim(),
    marks: document.getElementById("marks").value,
    contact: document.getElementById("contact").value.trim()
  };

  const id = studentId.value;
  const response = await fetch(id ? `/api/students/${id}` : "/api/students", {
    method: id ? "PUT" : "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(payload)
  });
  const result = await response.json();

  if (!response.ok) {
    showMessage(result.error || "Something went wrong.", "error");
    return;
  }

  showMessage(result.message);
  resetForm();
  loadStudents();
});

async function deleteStudent(id) {
  if (!confirm("Are you sure you want to delete this student?")) return;
  const response = await fetch(`/api/students/${id}`, {method: "DELETE"});
  const result = await response.json();
  if (!response.ok) {
    showMessage(result.error, "error");
    return;
  }
  showMessage(result.message);
  loadStudents();
}

let timer;
search.addEventListener("input", () => {
  clearTimeout(timer);
  timer = setTimeout(loadStudents, 250);
});

loadStudents();
