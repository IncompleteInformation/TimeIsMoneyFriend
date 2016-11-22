<?php

//Get Data from BattleNet

function getWholeAH() {
	$key = 'zs54fyqy2mycxjd2pv9rmev2db6x8k59';
	$server = 'malganis';
	$fetch_url = "https://us.api.battle.net/wow/auction/data/{$server}?locale=en_US&apikey={$key}";

	//Create JSON object and parse it into a php associated array if possible
	$responseJson	= file_get_contents($fetch_url);
	$responseObj	= json_decode($responseJson);
	$db_url = $responseObj->files[0]->url;
	
	echo $db_url;
	return $db_url;
}

function parseAH($db_url,$itemID){
	$responseJson	= file_get_contents($db_url);
	$responseObj	= json_decode($responseJson);
	$auctions		= $responseObj->auctions;
	$filteredAuctions = array();
	
	foreach ($auctions as $auction){
		if ($auction->item == $itemID) {
			array_push($filteredAuctions,$auction);
		}
	}
	return $filteredAuctions;
}

function calcStats($filteredAuctions){
	$allPrices = array();
	$marketVolume = 0;
	
	foreach ($filteredAuctions as $auction){
		$marketVolume += $auction->quantity;
		$price = $auction->buyout / $auction->quantity / 10000;
		array_push($allPrices,$price);
	}
	
	$meanPrice		= array_sum($allPrices) / count($allPrices);
	$stdDev			= stats_standard_deviation($allPrices);
	$minPrice		= min($allPrices);	
	
	printf("UNADJUSTED DATA:\n");
	printf("\nMinimum Price: %.2f\nMean Price: %.2f\nStandard Deviation: %.2f\n", $minPrice, $meanPrice, $stdDev);
	
	$allPrices	= removeOutliers($allPrices);
	$meanPrice		= array_sum($allPrices) / count($allPrices);
	$stdDev			= stats_standard_deviation($allPrices);
	$minPrice		= min($allPrices);
	
	printf("\n");
	printf("OUTLIERS REMOVED:\n");
	printf("\nMinimum Price: %.2f\nMean Price: %.2f\nStandard Deviation: %.2f\n", $minPrice, $meanPrice, $stdDev);
}

function removeOutliers($unfiltered){
	$stdDev			= stats_standard_deviation($unfiltered);
	$meanPrice		= array_sum($unfiltered) / count($unfiltered);
	$filtered		= array();
	foreach ($unfiltered as $price){
		if ($price < $meanPrice + $stdDev*2){
			array_push($filtered, $price);
		}
	}
	return $filtered;
}

$wholeAH = getWholeAH();
$itemID = 124106;

$filteredAH = parseAH($wholeAH,$itemID);

calcStats($filteredAH);
