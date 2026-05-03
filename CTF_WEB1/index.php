<?php
// Включаем отображение ошибок для симуляции уязвимости
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

$flag = "CTF{NZT_f0ll}";

// Симулируем "сложную" внутреннюю функцию
function processUserData($data, $secret_key) {
    // Если передали массив вместо строки, strlen выбросит TypeError в PHP 8+
    // или Warning в более старых версиях (в зависимости от настроек)
    // Мы принудительно вызовем исключение, если тип неверный
    if (is_array($data)) {
        throw new InvalidArgumentException("Data processing error: Expected string, got array. Context dumped.");
    }
    
    // Эмуляция уязвимой логики
    $result = substr($data, 0, 5) . $secret_key;
    return $result;
}

?>

<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>NZTmedicine | Партнерский портал</title>
</head>
<body>
    <h1>Проверка статуса партнера</h1>
    <p>Введите ваш ID (только цифры):</p>
    
    <form method="POST">
        
        <input type="text" name="user_id" placeholder="Например: 42">
        <button type="submit">Проверить</button>
    </form>

    <hr>

    <?php
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        $user_id = $_POST['user_id'];
        
        echo "<h3>Результат:</h3>";
        
        // Вот здесь кроется уязвимость: мы не обернули это в try-catch
        // и передаем $flag как аргумент в функцию. 
        // Если функция упадет, $flag может "засветиться" в логах ошибки.
        
        processUserData($user_id, $flag);
        
        echo "Партнер с таким ID не найден в системе.";
    }
    ?>
</body>
</html>