<?php

$dattim = date("Y-m-d H:i:s");
$time = date("Y, d, m, H, 0, 0");
$buero= round(exec("cat /sys/bus/w1/devices/10-00080277ad52/w1_slave | awk -F 't=' '{print $2}' ") / 1000, 1);
// $aussen1= round(exec("cat /sys/bus/w1/devices/10-000802779cc7/w1_slave | awk -F 't=' '{print $2}' ") / 1000, 1);



require_once('Tinkerforge/IPConnection.php');
require_once('Tinkerforge/BrickMaster.php');
require_once('Tinkerforge/BrickletTemperature.php');
require_once('Tinkerforge/BrickletLCD20x4.php');
require_once('Tinkerforge/BrickletAmbientLight.php');
require_once('Tinkerforge/BrickletBarometer.php');

use Tinkerforge\IPConnection;
use Tinkerforge\BrickMaster;
use Tinkerforge\BrickletTemperature;
// use Tinkerforge\BrickletLCD20x4;
// use Tinkerforge\BrickletAmbientLight;
// use Tinkerforge\BrickletBarometer;

$time = date("H:i");

$ipcon = new IPConnection();
$BrickletTemperature = new BrickletTemperature("Temp1", $ipcon);
// $BrickletLCD20x4 = new BrickletLCD20x4("9LY", $ipcon);
// $brickletAmbientLight = new BrickletAmbientLight("jxV", $ipcon);
// $brickletBarometer = new BrickletBarometer("jXQ", $ipcon);
$master = new BrickMaster("68USSm", $ipcon);

$ipcon->connect("192.168.2.156", 4223);

$temperature = $BrickletTemperature->getTemperature()/100.0;
// $illuminance = $brickletAmbientLight->getIlluminance()/10.0;
// $air_pressure = $brickletBarometer->getAirPressure()/1000.0;
// $temperatureb = $brickletBarometer->getChipTemperature()/100.0;
// $air_pressurea = $brickletBarometer->getAltitude()/100.0;
$getWifiConfiguration = $master->getWifiConfiguration();

// $aussen1 = $temperature; // Aussentemperatur Bricklet (Fenster Esszimmer)

	$cpu_temperature = round(exec("cat /sys/class/thermal/thermal_zone0/temp ") / 1000, 1);

//Uptime -- $uptime
	$uptime_array = explode(" ", exec("cat /proc/uptime"));
	$seconds = round($uptime_array[0], 0);
	$minutes = $seconds / 60;
	$hours = $minutes / 60;
	$days = floor($hours / 24);
	$hours = sprintf('%02d', floor($hours - ($days * 24)));
	$minutes = sprintf('%02d', floor($minutes - ($days * 24 * 60) - ($hours * 60)));
	if ($days == 0):
		$uptime = $hours . ":" .  $minutes . " (hh:mm)";
	elseif($days == 1):
		$uptime = $days . " Tag, " .  $hours . ":" .  $minutes . " Std.";
	else:
		$uptime = $days . " Tage, " .  $hours . ":" .  $minutes . " Std.";
	endif;

// CPU Usage -- $cpuload
	$output1 = null;
	$output2 = null;
	//First sample
	exec("cat /proc/stat", $output1);
	//Sleep before second sample
	sleep(1);
	//Second sample
	exec("cat /proc/stat", $output2);
	$cpuload = 0;
	for ($i=0; $i < 1; $i++)
	{
		//First row
		$cpu_stat_1 = explode(" ", $output1[$i+1]);
		$cpu_stat_2 = explode(" ", $output2[$i+1]);
		//Init arrays
		$info1 = array("user"=>$cpu_stat_1[1], "nice"=>$cpu_stat_1[2], "system"=>$cpu_stat_1[3], "idle"=>$cpu_stat_1[4]);
		$info2 = array("user"=>$cpu_stat_2[1], "nice"=>$cpu_stat_2[2], "system"=>$cpu_stat_2[3], "idle"=>$cpu_stat_2[4]);
		$idlesum = $info2["idle"] - $info1["idle"] + $info2["system"] - $info1["system"];
		$sum1 = array_sum($info1);
		$sum2 = array_sum($info2);
		//Calculate the cpu usage as a percent
		$load = (1 - ($idlesum / ($sum2 - $sum1))) * 100;
		$cpuload += $load;
	}
	$cpuload = round($cpuload, 2); //One decimal place
	
	

?>