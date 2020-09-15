package com.example.dogface.domain;

public class DogInfo {
    private String id;
    private String username;
    private String facecode;


    public DogInfo() {
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getFacecode() {
        return facecode;
    }

    public void setFacecode(String facecode) {
        this.facecode = facecode;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }
}
