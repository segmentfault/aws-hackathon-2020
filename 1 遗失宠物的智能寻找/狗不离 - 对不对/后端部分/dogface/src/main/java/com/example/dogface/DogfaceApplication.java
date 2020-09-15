package com.example.dogface;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
@MapperScan("com.example.dogface")
public class DogfaceApplication {

    public static void main(String[] args) {
        SpringApplication.run(DogfaceApplication.class, args);
    }

}
