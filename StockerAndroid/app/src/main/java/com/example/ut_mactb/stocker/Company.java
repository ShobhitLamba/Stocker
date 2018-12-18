package com.example.ut_mactb.stocker;

public class Company {

    private String name;
    private int accuracy;

    public Company(String name, int accuracy){
        //contructor
        this.name= name;
        this.accuracy=accuracy;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getAccuracy() {
        return accuracy;
    }

    public void setAccuracy(int accuracy) {
        this.accuracy = accuracy;
    }

}
