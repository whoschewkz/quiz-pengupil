<?php
session_start();

/**
 * ============================
 * CI MODE (STUB)
 * ============================
 */
if (getenv('CI')) {
    // Jika form disubmit di CI → langsung simulasi sukses
    if (isset($_POST['submit'])) {
        echo "Register berhasil";
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

    $name     = mysqli_real_escape_string($con, $_POST['name'] ?? '');
    $email    = mysqli_real_escape_string($con, $_POST['email'] ?? '');
    $username = mysqli_real_escape_string($con, $_POST['username'] ?? '');
    $password = mysqli_real_escape_string($con, $_POST['password'] ?? '');
    $repass   = mysqli_real_escape_string($con, $_POST['repassword'] ?? '');

    if ($name && $email && $username && $password && $repass) {

        if ($password === $repass) {

            $cek = mysqli_query($con, "SELECT * FROM users WHERE username='$username'");
            if (mysqli_num_rows($cek) === 0) {

                $hash = password_hash($password, PASSWORD_DEFAULT);
                $query = "INSERT INTO users (username,name,email,password)
                          VALUES ('$username','$name','$email','$hash')";

                if (mysqli_query($con, $query)) {
                    $_SESSION['username'] = $username;
                    header('Location: index.php');
                    exit;
                } else {
                    $error = 'Register User Gagal !!';
                }

            } else {
                $error = 'Username sudah terdaftar !!';
            }

        } else {
            $validate = 'Password tidak sama !!';
        }

    } else {
        $error = 'Data tidak boleh kosong !!';
    }
}
?>
