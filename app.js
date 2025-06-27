$(document).ready(function () {
  loadTodos();

  // Handle form submission
  $("#todo-form").on("submit", function (e) {
    e.preventDefault();
    const todoInput = $("#todo-input");
    const todoText = todoInput.val().trim();

    if (todoText) {
      addTodo(todoText);
      todoInput.val("");
    }
  });

  // Load todos from file
  function loadTodos() {
    $.get("/todos", function (data) {
      const todos = data ? data.split("\n").filter((todo) => todo.trim()) : [];
      todos.forEach((todo) => {
        const [text, completed] = todo.split("|");
        if (text) {
          addTodoToList(text, completed === "true");
        }
      });
    }).fail(function () {
      // If file doesn't exist yet, that's ok
      console.log("No existing todos found");
    });
  }

  // Add new todo
  function addTodo(text) {
    addTodoToList(text, false);
    saveTodos();
  }

  // Add todo to the list in the UI
  function addTodoToList(text, completed) {
    const todoItem = $(`
            <li class="list-group-item todo-item ${
              completed ? "completed" : ""
            }">
                <div class="form-check">
                    <input class="form-check-input" type="checkbox" ${
                      completed ? "checked" : ""
                    }>
                    <span class="todo-text">${text}</span>
                </div>
                <button class="btn btn-danger btn-sm btn-delete">Delete</button>
            </li>
        `);

    // Handle checkbox change
    todoItem.find('input[type="checkbox"]').on("change", function () {
      $(this).closest(".todo-item").toggleClass("completed");
      saveTodos();
    });

    // Handle delete button
    todoItem.find(".btn-delete").on("click", function () {
      $(this).closest(".todo-item").remove();
      saveTodos();
    });

    $("#todo-list").append(todoItem);
  }

  // Save todos to file
  function saveTodos() {
    const todos = [];
    $(".todo-item").each(function () {
      const text = $(this).find(".todo-text").text();
      const completed = $(this).hasClass("completed");
      todos.push(`${text}|${completed}`);
    });

    $.ajax({
      url: "/save_todo",
      method: "POST",
      data: { todos: todos.join("\n") },
      success: function (response) {
        console.log("Todos saved successfully");
      },
      error: function (xhr, status, error) {
        console.error("Error saving todos:", error);
      },
    });
  }
});
