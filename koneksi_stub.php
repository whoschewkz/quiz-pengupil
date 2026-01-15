<?php
// Mock database connection for CI / testing
class MockResult {
    public $data;
    public function __construct($data) {
        $this->data = $data;
    }
}

// Mock mysqli functions
function mysqli_query($connection, $query) {
    global $users;
    
    // Parse SELECT queries
    if (stripos($query, 'SELECT') === 0) {
        preg_match("/WHERE username = '([^']+)'/", $query, $matches);
        if ($matches) {
            $username = $matches[1];
            if (isset($users[$username])) {
                $result = new MockResult([$users[$username]]);
                return $result;
            }
        }
    }
    
    return new MockResult([]);
}

function mysqli_num_rows($result) {
    return count($result->data);
}

function mysqli_fetch_assoc($result) {
    if (count($result->data) > 0) {
        return array_shift($result->data);
    }
    return null;
}

function mysqli_real_escape_string($connection, $string) {
    return addslashes($string);
}

// Test user data
$users = [
    'user1' => [
        'username' => 'user1',
        'password' => '$2y$10$R9h7cIPz0gi.URNNX3kh2OPST9/PgBkqquzi.Ss7KIUgO2t0jKMm2' // password: 123456
    ]
];

$con = true;
?>
