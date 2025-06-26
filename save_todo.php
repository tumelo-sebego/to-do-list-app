<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['todos'])) {
    $todos = $_POST['todos'];
    file_put_contents('todos.txt', $todos);
    echo 'success';
} else {
    http_response_code(400);
    echo 'error';
}
?>
