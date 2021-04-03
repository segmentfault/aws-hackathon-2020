package com.cats.lostandfound.service;

import com.cats.lostandfound.mapper.UserMapper;
import com.cats.lostandfound.entity.Message;
import com.cats.lostandfound.entity.User;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Transactional(rollbackFor = RuntimeException.class)
public class UserService {

    @Autowired
    private UserMapper userMapper;
    /**
     * 注册
     * @param user 参数封装
     * @return Result
     */
    public Message<User> regist(User user) {
        Message<User> result = new Message<>();
        result.setSuccess(false);
        result.setDetail(null);
        try {
            User existUser = userMapper.findUserByEmail(user.getEmail());
            if(existUser != null){
                //如果邮箱已存在
                result.setMsg("邮箱已被注册");

            }else{
                userMapper.regist(user);
                result.setMsg("注册成功");
                result.setSuccess(true);
                result.setDetail(user);
            }
        } catch (Exception e) {
            result.setMsg(e.getMessage());
            e.printStackTrace();
        }
        return result;
    }
    /**
     * 登录
     * @param user 用户名和密码
     * @return Result
     */
    public Message<User> login(User user) {
        Message<User> result = new Message<>();
        result.setSuccess(false);
        result.setDetail(null);
        try {
            Long userId= userMapper.login(user);
            if(userId == null){
                result.setMsg("邮箱或密码错误");
            }else{
                result.setMsg("登录成功");
                result.setSuccess(true);
                user.setUserId(userId);
                result.setDetail(user);
            }
        } catch (Exception e) {
            result.setMsg(e.getMessage());
            e.printStackTrace();
        }
        return result;
    }
}