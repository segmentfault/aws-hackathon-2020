from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf

import os
import pickle
import numpy as np
import skimage as sk
import matplotlib.pyplot as plt
import tensorflow.keras.backend as K
from offline_training import *
from math import isnan

SIZE = (224,224,3)

def define_triplets_batch(filenames,labels,nbof_triplet = 21 * 3):
    triplet_train = []
    y_triplet = np.empty(nbof_triplet)
    classes = np.unique(labels)
    for i in range(0,nbof_triplet,3):
        classAP = classes[np.random.randint(len(classes))]
        keep = np.equal(labels,classAP)
        keep_classAP = filenames[keep]
        keep_classAP_idx = labels[keep]
        idx_image1 = np.random.randint(len(keep_classAP))
        idx_image2 = np.random.randint(len(keep_classAP))
        while idx_image1 == idx_image2:
            idx_image2 = np.random.randint(len(keep_classAP))

        triplet_train += [keep_classAP[idx_image1]]
        triplet_train += [keep_classAP[idx_image2]]
        y_triplet[i] = keep_classAP_idx[idx_image1]
        y_triplet[i+1] = keep_classAP_idx[idx_image2]
        classN = classes[np.random.randint(len(classes))]
        while classN==classAP:
            classN = classes[np.random.randint(len(classes))]
        keep = np.equal(labels,classN)
        keep_classN = filenames[keep]
        keep_classN_idx = labels[keep]
        idx_image3 = np.random.randint(len(keep_classN))
        triplet_train += [keep_classN[idx_image3]]
        y_triplet[i+2] = keep_classN_idx[idx_image3]
        
    return triplet_train, y_triplet

def define_hard_triplets_batch(filenames,labels,predict,nbof_triplet=21*3, use_neg=True, use_pos=True):
    assert nbof_triplet%3 == 0
    
    _,idx_classes = np.unique(labels,return_index=True)
    classes = labels[np.sort(idx_classes)]
    
    triplets = []
    y_triplets = np.empty(nbof_triplet)
    
    for i in range(0,nbof_triplet,3):
        keep = np.equal(labels,classes[np.random.randint(len(classes))])
        keep_filenames = filenames[keep]
        keep_labels = labels[keep]
        
        idx_image1 = np.random.randint(len(keep_labels))
        
        
        if use_pos:
            dist_class = np.sum(np.square(predict[keep]-predict[keep][idx_image1]),axis=-1)

            idx_image2 = np.argmax(dist_class)
        else:
            idx_image2 = np.random.randint(len(keep_labels))
            i = 0
            while idx_image1==idx_image2:
                idx_image2 = np.random.randint(len(keep_labels))
                i += 1
                if i == 1000:
                    print("[Error: define_hard_triplets_batch] Endless loop.")
                    break
        
        triplets += [keep_filenames[idx_image1]]
        y_triplets[i] = keep_labels[idx_image1]
        triplets += [keep_filenames[idx_image2]]
        y_triplets[i+1] = keep_labels[idx_image2]
        
        
        not_keep = np.logical_not(keep)
        
        if use_neg:
            dist_other = np.sum(np.square(predict[not_keep]-predict[keep][idx_image1]),axis=-1)
            idx_image3 = np.argmin(dist_other) 
        else:
            idx_image3 = np.random.randint(len(filenames[not_keep]))
            
        triplets += [filenames[not_keep][idx_image3]]
        y_triplets[i+2] = labels[not_keep][idx_image3]

    return np.array(triplets), y_triplets

def define_adaptive_hard_triplets_batch(filenames,labels,predict,nbof_triplet=21*3, use_neg=True, use_pos=True):

    assert nbof_triplet%3 == 0
    
    _,idx_classes = np.unique(labels,return_index=True)
    classes = labels[np.sort(idx_classes)]
    
    triplets = []
    y_triplets = np.empty(nbof_triplet)
    pred_triplets = np.empty((nbof_triplet,predict.shape[-1]))
    
    for i in range(0,nbof_triplet,3):

        keep = np.equal(labels,classes[np.random.randint(len(classes))])
        keep_filenames = filenames[keep]
        keep_labels = labels[keep]
        

        idx_image1 = np.random.randint(len(keep_labels))
        

        if use_pos:
            dist_class = np.sum(np.square(predict[keep]-predict[keep][idx_image1]),axis=-1)

            idx_image2 = np.argmax(dist_class)
        else:
            idx_image2 = np.random.randint(len(keep_labels))
            j = 0
            while idx_image1==idx_image2:
                idx_image2 = np.random.randint(len(keep_labels))
                j += 1
                if j == 1000:
                    print("[Error: define_hard_triplets_batch] Endless loop.")
                    break
        
        triplets += [keep_filenames[idx_image1]]
        y_triplets[i] = keep_labels[idx_image1]
        pred_triplets[i] = predict[keep][idx_image1]
        triplets += [keep_filenames[idx_image2]]
        y_triplets[i+1] = keep_labels[idx_image2]
        pred_triplets[i+1] = predict[keep][idx_image2]
        
        not_keep = np.logical_not(keep)
        
        if use_neg:
            dist_other = np.sum(np.square(predict[not_keep]-predict[keep][idx_image1]),axis=-1)
            idx_image3 = np.argmin(dist_other) 
        else:
            idx_image3 = np.random.randint(len(filenames[not_keep]))
            
        triplets += [filenames[not_keep][idx_image3]]
        y_triplets[i+2] = labels[not_keep][idx_image3]
        pred_triplets[i+2] = predict[not_keep][idx_image3]

    return np.array(triplets), y_triplets, pred_triplets

def load_images(filenames):
    h,w,c = SIZE
    images = np.empty((len(filenames),h,w,c))
    for i,f in enumerate(filenames):
        images[i] = sk.io.imread(f)/255.0
    return images

def image_generator(filenames, labels, batch_size=63, use_aug=True, datagen=datagen):
    while True:
        f_triplet, y_triplet = define_triplets_batch(filenames, labels, batch_size)
        i_triplet = load_images(f_triplet)
        if use_aug:
            i_triplet = apply_transform(i_triplet, datagen)
        yield (i_triplet, y_triplet)

def hard_image_generator(filenames, labels, predict, batch_size=63, use_neg=True, use_pos=True, use_aug=True, datagen=datagen):
    while True:
        f_triplet, y_triplet = define_hard_triplets_batch(filenames, labels, predict, batch_size, use_neg=use_neg, use_pos=use_pos)
        i_triplet = load_images(f_triplet)
        if use_aug:
            i_triplet = apply_transform(i_triplet, datagen)
        yield (i_triplet, y_triplet)

def predict_generator(filenames, batch_size=32):

    for i in range(0,len(filenames),batch_size):
        images_batch = load_images(filenames[i:i+batch_size])
        yield images_batch

def online_hard_image_generator(
    filenames,
    labels,
    model,
    batch_size=63,
    nbof_subclasses=10,
    use_neg=True,
    use_pos=True,
    use_aug=True,
    datagen=datagen):

    while True:

        classes = np.unique(labels)
        subclasses = np.random.choice(classes,size=nbof_subclasses,replace=False)
        
        keep_classes = np.equal(labels,subclasses[0])
        for i in range(1,len(subclasses)):
            keep_classes = np.logical_or(keep_classes,np.equal(labels,subclasses[i]))
        subfilenames = filenames[keep_classes]
        sublabels = labels[keep_classes]
        predict = model.predict_generator(predict_generator(subfilenames, 32),
                                          steps=np.ceil(len(subfilenames)/32))
        
        f_triplet, y_triplet = define_hard_triplets_batch(subfilenames, sublabels, predict, batch_size, use_neg=use_neg, use_pos=use_pos)
        i_triplet = load_images(f_triplet)
        if use_aug:
            i_triplet = apply_transform(i_triplet, datagen)
        yield (i_triplet, y_triplet)

def online_adaptive_hard_image_generator(
    filenames,  
    labels, 
    model, 
    loss, 
    batch_size      =63, 
    nbof_subclasses =10,  
    use_aug         =True, 
    datagen         =datagen):
    
    hard_triplet_ratio = 0
    nbof_hard_triplets = 0
    while True:
        classes = np.unique(labels)
        subclasses = np.random.choice(classes,size=int(nbof_subclasses*hard_triplet_ratio)+2,replace=False)
        
        keep_classes = np.equal(labels,subclasses[0])
        for i in range(1,len(subclasses)):
            keep_classes = np.logical_or(keep_classes,np.equal(labels,subclasses[i]))
        subfilenames = filenames[keep_classes]
        sublabels = labels[keep_classes]
        predict = model.predict_generator(predict_generator(subfilenames, 32),
                                          steps=int(np.ceil(len(subfilenames)/32)))
        
        
        
        
        
        f_triplet_hard, y_triplet_hard, predict_hard = define_adaptive_hard_triplets_batch(subfilenames, sublabels, predict, nbof_hard_triplets*3, use_neg=True, use_pos=True)
        f_triplet_soft, y_triplet_soft, predict_soft = define_adaptive_hard_triplets_batch(subfilenames, sublabels, predict, batch_size-nbof_hard_triplets*3, use_neg=False, use_pos=False)

        f_triplet = np.append(f_triplet_hard,f_triplet_soft)
        y_triplet = np.append(y_triplet_hard,y_triplet_soft)

        predict = np.append(predict_hard, predict_soft, axis=0)
        
        hard_triplet_ratio = np.exp(-loss * 10 / batch_size)

        if isnan(hard_triplet_ratio):
            hard_triplet_ratio = 0
        nbof_hard_triplets = int(batch_size//3 * hard_triplet_ratio)
        
        i_triplet = load_images(f_triplet)
        if use_aug:
            i_triplet = apply_transform(i_triplet, datagen)
        
        yield (i_triplet, y_triplet)


