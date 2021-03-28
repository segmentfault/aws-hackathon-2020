package com.example.dogface.service;

import com.example.dogface.dao.AccountMapper;
import com.example.dogface.domain.Account;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class AccountService {
    @Autowired
    AccountMapper accountMapper;

    public Account getAccount(String username) {
        return accountMapper.getAccountByUsername(username);
    }

    public Account getAccount(String username, String password) {
        Account account = new Account();
        account.setUsername(username);
        account.setPassword(password);
        return accountMapper.getAccountByUsernameAndPassword(account);
    }

    public void insertAccount(Account account) {
        accountMapper.insertAccount(account);
    }

    public void updateAccount(Account account) {
        accountMapper.updateAccount(account);
    }

}
