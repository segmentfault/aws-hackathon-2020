package com.example.dogface.service;


import com.example.dogface.dao.DogMapper;
import com.example.dogface.domain.DogInfo;
import com.example.dogface.utils.FaceCodeUtil;
import javafx.util.Pair;
import org.apache.commons.io.FileUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.multipart.MultipartFile;

import javax.servlet.http.HttpServletRequest;
import java.io.File;
import java.io.IOException;
import java.util.*;

@Service
public class DogService {

    @Autowired
    DogMapper dogMapper;

    public void addDogInfo(MultipartFile imageFile,
                           String username) {
        String path = "./localdata/images/";
        File imageDir = new File(path);
        if (!imageDir.exists()) {
            imageDir.mkdir();
        }
        String suf = imageFile.getOriginalFilename()
                .substring(imageFile.getOriginalFilename().indexOf(".") + 1);
        UUID uuid = UUID.randomUUID();
        String imageName = uuid.toString() + String.valueOf(imageFile.getOriginalFilename().hashCode());
        String id = imageName;
        imageName = imageName + "." + suf;
        try {
            FileUtils.writeByteArrayToFile(new File(path+imageName),
                    imageFile.getBytes());
        } catch (IOException e) {
            e.printStackTrace();
        }
        String facecode = FaceCodeUtil.getFaceCode(imageFile);
        DogInfo dogInfo = new DogInfo();
        dogInfo.setUsername(username);
        dogInfo.setId(id);
        dogInfo.setFacecode(facecode);
        dogMapper.insertDogInfo(dogInfo);
    }

    public List<DogInfo> findDog(MultipartFile imageFile) {
        String facecode = FaceCodeUtil.getFaceCode(imageFile);
        int k = 3;
        List<DogInfo> dogInfos = dogMapper.getAllDogs();
        PriorityQueue<Pair<DogInfo,Double>> q = new PriorityQueue<>(new Comparator<Pair<DogInfo, Double>>() {
            @Override
            public int compare(Pair<DogInfo, Double> o1, Pair<DogInfo, Double> o2) {
                if (o1.getValue() - o2.getValue() < 0) {
                    return 1;
                }
                return 0;
            }
        }) ;
        for (DogInfo dogInfo : dogInfos) {
            double d = FaceCodeUtil.getDistance(dogInfo.getFacecode(), facecode);
            if (q.size() < k) {
                q.add(new Pair<>(dogInfo, d));
                continue;
            }
            if (d < q.element().getValue()) {
                q.remove();
                q.add(new Pair<>(dogInfo, d));
            }
        }
        List ans = new ArrayList<DogInfo>();
        for (Pair<DogInfo, Double> pair : q) {
            ans.add(pair.getKey());
        }
        return ans;
    }
}
