<?php
class plant{
 public $link='';
 function __construct($ID, $Moisture){
  $this->connect();
  $this->storeInDB($ID, $Moisture);
 }
 
 function connect(){
  $this->link = mysqli_connect('192.168.0.162','doev3','Wowc78wowc!!#') or die('Cannot connect to the DB');
  mysqli_select_db($this->link,'AutoGrow') or die('Cannot select the DB');
 }
 
 function storeInDB($ID, $Moisture){
  $query = "update Plants set SoilMoisture='".$Moisture."' where plantID='".$ID."' ";
  $result = mysqli_query($this->link,$query) or die('Errant query:  '.$query);
 }
 
}

if($_GET['ID'] != '' and  $_GET['Moisture'] != ''){
 $plant=new plant($_GET['ID'],$_GET['Moisture']);
}
?>