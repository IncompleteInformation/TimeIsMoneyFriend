<?php
// sample script to query newswire for the daily history of draenic dust on US Medivh

function demo() {
    $db = @new mysqli('newswire.theunderminejournal.com', '', '', 'newsstand');
    if ($db->connect_error) {
        echo "Connect error: {$db->connect_error}\n";
        return;
    }
    $db->set_charset("utf8");

    $sql = <<<'EOF'
    select *
    from tblItemHistoryMonthly h
    join tblRealm r on h.house = r.house
    where r.region = ?
    and r.slug = ?
    and h.item = ?
    and h.bonusset = ?
    order by h.month asc
EOF;

    $region = 'US';
    $slug = 'medivh';
    $itemId = 109693;
    $bonusSet = 0;

    $stmt = $db->prepare($sql);
    $stmt->bind_param('ssii', $region, $slug, $itemId, $bonusSet);
    $stmt->execute();

    $row = [];
    $params = [];
    $fields = $stmt->result_metadata()->fetch_fields();
    foreach ($fields as $field) {
        $params[] = &$row[$field->name];
    }
    call_user_func_array([$stmt, 'bind_result'], $params);

    while ($stmt->fetch()) {
        $year = 2014 + floor(($row['month'] - 1) / 12);
        $month = ($row['month'] - 1) % 12 + 1;
        $monthPadded = ($month < 10 ? '0' : '') . $month;
        for ($x = 1; $x <= 31; $x++) {
            $dayPadded = ($x < 10 ? '0' : '') . $x;
            if (is_null($row["qty$dayPadded"])) {
                continue;
            }
            echo sprintf("%d-%s-%s: %sg, %d max qty seen\n", $year, $monthPadded, $dayPadded, round($row["mktslvr$dayPadded"]/100, 2), $row["qty$dayPadded"]);
        }
    }
    $stmt->close();

    $db->close();
}

header('Content-type: text/plain');
echo file_get_contents(__FILE__);
echo "\n\n/*\n\n";
demo();
echo "\n*/\n";