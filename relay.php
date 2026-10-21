<?php
// Relays the attendance page's requests to the Google Apps Script web app,
// so phones in Iran never talk to Google directly.
// Test in a browser: relay.php?ping=1
$GAS = 'https://script.google.com/macros/s/AKfycbym7MpYvKkwFJaLuTStK0Khs7pWmp6TOLL65VHstiXWGhsV_0GUtCEEu0hRE8RaqzfGCw/exec';
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
$ping = isset($_GET['ping']);
$ch = curl_init($ping ? $GAS . '?action=attPing' : $GAS);
curl_setopt_array($ch, [
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_FOLLOWLOCATION => true,
  CURLOPT_MAXREDIRS => 5,
  CURLOPT_TIMEOUT => 40,
  CURLOPT_CONNECTTIMEOUT => 15,
]);
if (!$ping) {
  curl_setopt($ch, CURLOPT_POST, true);
  curl_setopt($ch, CURLOPT_POSTFIELDS, file_get_contents('php://input'));
  curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: text/plain;charset=utf-8']);
}
$out = curl_exec($ch);
$code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
$err = curl_error($ch);
curl_close($ch);
if ($out === false || $code >= 400) {
  http_response_code(502);
  echo json_encode(['ok' => false, 'error' => 'relay: ' . ($err ?: 'HTTP ' . $code)], JSON_UNESCAPED_UNICODE);
  exit;
}
echo $out;
