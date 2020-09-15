package com.example.dogface.controller;

import com.example.dogface.domain.Account;
import com.example.dogface.service.AccountService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import javax.servlet.http.HttpServletRequest;

@RestController
@CrossOrigin
public class AccountController {
    @Autowired
    AccountService accountService;

    @RequestMapping(value = "account/signin", method = RequestMethod.GET)
    public ResponseEntity signIn(@RequestParam("username") String username,
                                 @RequestParam("password") String password,
                                 HttpServletRequest request){

        Account account = accountService.getAccount(username,password);
        if(account != null){
            request.getSession().setAttribute("account",account);
            return new ResponseEntity("OK", HttpStatus.OK);
        }else{
            return new ResponseEntity("Invalid username or password. Signon failed.", HttpStatus.OK);
        }
    }

    @RequestMapping(value = "account/signout", method = RequestMethod.GET)
    public void signOut(HttpServletRequest request){
        request.getSession().setAttribute("account",null);
    }

    @RequestMapping(value = "account/accountinfo", method = RequestMethod.GET)
    public ResponseEntity AccountInfo(HttpServletRequest request){
        String username = (String) request.getSession().getAttribute("account");
        Account account = accountService.getAccount(username);
        return new ResponseEntity(account, HttpStatus.OK);
    }

    @PostMapping("account/regist")
    public ResponseEntity reigst(@RequestBody Account account){
        if (accountService.getAccount(account.getUsername()) != null) {
            return new ResponseEntity("Username already exists", HttpStatus.OK);
        }
        accountService.insertAccount(account);
        return new ResponseEntity("OK", HttpStatus.OK);
    }


}
