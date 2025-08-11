<?php
function translate($text, $source = 'en', $target = 'pt') {
    $data = [
        'q' => $text,
        'source' => $source,
        'target' => $target,
        'format' => 'text'
    ];

    $ch = curl_init('https://libretranslate.de/translate');
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($data));
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        "Content-Type: application/x-www-form-urlencoded"
    ]);

    $result = curl_exec($ch);
    if ($result === FALSE) {
        return "Error: Could not connect to API. Details: " . curl_error($ch);
    }
    $json = json_decode($result, true);
    curl_close($ch);
    return $json['translatedText'] ?? "Error: Invalid response.";
}

echo translate("Hello world", 'en', 'pt');
?>
