package messageFormat;

import org.joda.time.DateTime;
import org.joda.time.format.DateTimeFormat;
import org.joda.time.format.DateTimeFormatter;

public class Message {
    private String deviceName;
    private String datetime;
    private double latitude;
    private double longitude;
    private double PM2_5;
    private double PM10;


    public Message(){

    }

    public Message(String deviceName,  String datetime, double latitude, double longitude, double PM2_5,  double PM10) {
        this.deviceName = deviceName;
        this.PM2_5 = PM2_5;
        this.PM10 = PM10;
        this.latitude = latitude;
        this.longitude = longitude;
        this.datetime = datetime;
    }

    public String getDatetime() {
        return datetime;
    }

    public void setDatetime(String datetime) {
        this.datetime = datetime;
    }

    public double getPm2_5() {
        return PM2_5;
    }

    public void setPM2_5(double pm2_5) {
        this.PM2_5 = pm2_5;
    }

    public double getPm10() {
        return PM10;
    }

    public void setPM10(double pm10) {
        this.PM10 = pm10;
    }

    public String toString(){
        return "DeviceName: "+getDeviceName()+" PM2_5: "+getPm2_5() + " PM10: "+getPm10()
                +"Lat: "+getLatitude()+" Long:"+getLongitude()+"DateTime: "+getDatetime();
    }

    public double getLatitude() {
        return latitude;
    }

    public void setLatitude(double latitude) {
        this.latitude = latitude;
    }

    public double getLongitude() {
        return longitude;
    }

    public void setLongitude(double longitude) {
        this.longitude = longitude;
    }

    public String getDeviceName() {
        return deviceName;
    }

    public void setDeviceName(String deviceName) {
        this.deviceName = deviceName;
    }

    public ErrorMessage validate() {
        DateTimeFormatter format = DateTimeFormat.forPattern("yyyy-MM-dd'T'HH:mm:ss.SSS'Z'");

        if(PM2_5 <= 0 || PM10 <= 0)
            return ErrorMessage.SensorProblem;
        else if("".equals(deviceName) || "".equals(datetime))
            return ErrorMessage.MissingParameters;
        else if(-90> latitude || latitude > 90 || -180 > longitude || longitude > 180)
            return ErrorMessage.IncorrectLocation;
        else if(format.parseDateTime(datetime).isAfter(DateTime.now()))
            return ErrorMessage.WrongDateTime;
        return  null;
    }

}
