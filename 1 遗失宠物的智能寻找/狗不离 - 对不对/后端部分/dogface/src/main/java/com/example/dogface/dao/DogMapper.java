package com.example.dogface.dao;

import com.example.dogface.domain.DogInfo;
import org.apache.ibatis.annotations.Mapper;

import java.util.List;

@Mapper
public interface DogMapper {
    List<DogInfo> getAllDogs();

    DogInfo getDogInfoByUsername(String username);

    void insertDogInfo(DogInfo dogInfo);
}
