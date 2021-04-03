package com.cats.lostandfound.service;

import com.cats.lostandfound.entity.Message;
import com.cats.lostandfound.entity.Photo;
import com.cats.lostandfound.mapper.PhotoMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@Transactional(rollbackFor = RuntimeException.class)
public class PhotoService {

    @Autowired
    private PhotoMapper photoMapper;

    public Message<Photo> addPhoto(Photo photo) {
        Message<Photo> result = new Message<>();
        result.setSuccess(false);
        result.setDetail(null);
        try {
            photoMapper.addPhoto(photo);
            result.setSuccess(true);
            result.setMsg("上传成功");
            result.setDetail(photo);
        } catch (Exception e) {
            result.setMsg(e.getMessage());
            e.printStackTrace();
        }
        return result;
    }

    public Message<Photo> deleteByPostId(long post_id) {
        Message<Photo> result = new Message<>();
        result.setSuccess(false);
        result.setDetail(null);
        try {
            photoMapper.deleteByPostId(post_id);
            result.setSuccess(true);
            result.setMsg("删除成功");
        } catch (Exception e) {
            result.setMsg(e.getMessage());
            e.printStackTrace();
        }
        return result;
    }

    public Message<Photo> deleteByPhotoId(long photo_id) {
        Message<Photo> result = new Message<>();
        result.setSuccess(false);
        result.setDetail(null);
        try {
            photoMapper.deleteByPhotoId(photo_id);
            result.setSuccess(true);
            result.setMsg("删除成功");
        } catch (Exception e) {
            result.setMsg(e.getMessage());
            e.printStackTrace();
        }
        return result;
    }

    public Message<List<Photo>> findPhotosByPostId(long post_id) {
        Message<List<Photo>> result = new Message<>();
        result.setSuccess(false);
        result.setDetail(null);
        try {
            List<Photo> list = photoMapper.findPhotosByPostId(post_id);
            result.setSuccess(true);
            result.setDetail(list);
            result.setMsg("查询成功");
        } catch (Exception e) {
            result.setMsg(e.getMessage());
            e.printStackTrace();
        }
        return result;
    }

    public Message<Photo> findCoverByPostId(long post_id) {
        Message<Photo> result = new Message<>();
        result.setSuccess(false);
        result.setDetail(null);
        try {
            Photo cover = photoMapper.findCoverByPostId(post_id);
            result.setSuccess(true);
            result.setDetail(cover);
            result.setMsg("查询成功");
        } catch (Exception e) {
            result.setMsg(e.getMessage());
            e.printStackTrace();
        }
        return result;
    }
}
