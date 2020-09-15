package com.example.dogface.controller;

import com.example.dogface.domain.Account;
import com.example.dogface.service.DogService;
import org.apache.commons.io.FileUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import javax.servlet.http.HttpServletRequest;
import java.io.File;
import java.io.IOException;
import java.util.UUID;

@RestController
@CrossOrigin
public class DogController {

    @Autowired
    DogService dogService;

    @RequestMapping(value = "dog/adddog", method = RequestMethod.POST)
    public ResponseEntity addDog(@RequestParam("image") MultipartFile imageFile,
                                 HttpServletRequest request) {
        Account account = (Account) request.getSession().getAttribute("account");
        dogService.addDogInfo(imageFile, account.getUsername());
        return new ResponseEntity("OK", HttpStatus.OK);

    }

}
