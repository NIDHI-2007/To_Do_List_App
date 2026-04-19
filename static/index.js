const taskInput = document.getElementById('taskInput');
const addBtn = document.getElementById("addBtn");
const taskList = document.getElementById("taskList");
const completedCount = document.getElementById("completedCount");
const uncompletedCount = document.getElementById("uncompletedCount");

addBtn.addEventListener("click", addTask);

function addTask() {
    const taskText = taskInput.value.trim();

    if (taskText === "") {
        alert("Please enter a task");
        return;
    }

    const li = document.createElement("li");

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";

    const span = document.createElement("span");
    span.textContent = taskText;

    const deleteBtn = document.createElement("button");
    deleteBtn.textContent = "Delete";

    const editBtn = document.createElement("button");
    editBtn.textContent = "Edit";

    li.appendChild(checkbox);
    li.appendChild(span);
    li.appendChild(deleteBtn);
    li.appendChild(editBtn);

    taskList.appendChild(li);
    taskInput.value = "";

    updateCount();
}

taskList.addEventListener("change", function (e) {
  if (e.target.type === "checkbox") {
    const taskText = e.target.nextElementSibling;

    if (e.target.checked) {
      taskText.style.textDecoration = "line-through";
      taskText.style.color = "#aaa";
    } else {
      taskText.style.textDecoration = "none";
      taskText.style.color = "#fff";
    }
    updateCount();
  }
});

taskList.addEventListener("click", function (e) {
  if (e.target.textContent === "Delete") {
    e.target.parentElement.remove();
    updateCount();
  }
});

taskList.addEventListener("click", function (e) {
  if (e.target.textContent === "Edit") {
    const span = e.target.previousElementSibling;
    const newText = prompt("Edit task:", span.textContent);

    if (newText !== null && newText.trim() !== "") {
      span.textContent = newText.trim();
    }
  }
});

function updateCount() {
  const totalTasks = taskList.children.length;
  const completedTasks = taskList.querySelectorAll("input[type='checkbox']:checked").length;

  completedCount.textContent = completedTasks;
  uncompletedCount.textContent = totalTasks - completedTasks;
}

taskInput.addEventListener("keypress", function (e) {
  if (e.key === "Enter") {
    addTask();
  }
});  