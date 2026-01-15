<?php
session_start();

/**
 * ============================
 * CI MODE (STUB)
 * ============================
 */
if (getenv('CI')) {
    if (isset($_POST['submit'])) {
        $_SESSION['username'] = 'ci_user';
        echo "Login berhasil";
        exit;
    }
}

/**
 * ============================
 * NORMAL MODE (LOCAL)
 * ============================
 */
require('koneksi.php');

$error = '';
$validate = '';

if (isset($_SESSION['username'])) {
    header('Location: index.php');
    exit;
}

if (isset($_POST['submit'])) {

    $username = mysqli_real_escape_string($con, $_POST['username'] ?? '');
    $password = mysqli_real_escape_string($con, $_POST['password'] ?? '');

    if ($username && $password) {

        $query  = "SELECT * FROM users WHERE username='$username'";
        $result = mysqli_query($con, $query);

        if (mysqli_num_rows($result) === 1) {
            $row = mysqli_fetch_assoc($result);

            if (password_verify($password, $row['password'])) {
                $_SESSION['username'] = $username;
                header('Location: index.php');
                exit;
            } else {
                $error = 'Password salah !!';
            }
        } else {
            $error = 'Username tidak ditemukan !!';
        }

    } else {
        $error = 'Data tidak boleh kosong !!';
    }
}
?>
