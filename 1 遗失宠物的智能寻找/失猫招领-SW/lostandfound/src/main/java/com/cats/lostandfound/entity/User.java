package com.cats.lostandfound.entity;

/**
 * 用户信息
 */
public class User {
    private Long user_id;
    private String email;
    private String password;

    public Long getId() {
        return user_id;
    }

    public void setUserId(Long user_id) {
        this.user_id = user_id;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    @Override
    public String toString() {
        return "User{" +
                "id=" + user_id +
                ", email='" + email + '\'' +
                ", password='" + password + '\'' +
                '}';
    }
}