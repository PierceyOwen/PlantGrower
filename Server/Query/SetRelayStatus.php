<?php
    class relay{
        public $link='';

        function __construct($ID, $WaterStatus, $HumidifierStatus, $SMSensorStatus, $LightStatus){
            $this->connect();
            $this->storeInDB($ID, $WaterStatus, $HumidifierStatus, $SMSensorStatus, $LightStatus);
        }
        
        function connect(){
            $this->link = mysqli_connect('192.168.0.162','doev3','Wowc78wowc!!#') or die('Cannot connect to the DB');
            mysqli_select_db($this->link,'AutoGrow') or die('Cannot select the DB');
        }
        
        function storeInDB($ID, $WaterStatus, $HumidifierStatus, $SMSensorStatus, $LightStatus){
            $query = "update Tents set WaterStatus='".$WaterStatus."', HumidifierStatus='".$HumidifierStatus."', SMSensorStatus='".$SMSensorStatus."', LightStatus='".$LightStatus."' where plantID='".$ID."' ";
            $result = mysqli_query($this->link,$query) or die('Errant query:  '.$query);
        }
    
    }

    #if($_GET['ID'] != '' and  $_GET['WaterStatus'] != '' and $_GET['HumidifierStatus'] != '' and $_GET['SMSensorStatus'] != '' and $_GET['LightStatus'] != ''){
    $plant=new relay($_GET['ID'],$_GET['WaterStatus'],$_GET['HumidifierStatus'],$_GET['SMSensorStatus'],$_GET['LightStatus']);
    #}
?>