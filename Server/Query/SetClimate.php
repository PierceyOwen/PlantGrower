<?php
class dht11{
 public $link='';
 function __construct($ID, $temperature, $humidity){
  $this->connect();
  $this->storeInDB($ID, $temperature, $humidity);
 }
 
 function connect(){
  $this->link = mysqli_connect('192.168.0.162','doev3','Wowc78wowc!!#') or die('Cannot connect to the DB');
  mysqli_select_db($this->link,'AutoGrow') or die('Cannot select the DB');
 }
 
 function storeInDB($ID, $temperature, $humidity){
  $query = "update Tents set Humidity='".$humidity."', Temperature='".$temperature."' where ID='".$ID."'";
  $result = mysqli_query($this->link,$query) or die('Errant query:  '.$query);
 }
 
}

if($_GET['ID'] != '' and $_GET['temperature'] != '' and  $_GET['humidity'] != ''){
 $dht11=new dht11($_GET['ID'],$_GET['temperature'],$_GET['humidity']);
}
?>