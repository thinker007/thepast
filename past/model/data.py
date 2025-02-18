#-*- coding:utf-8 -*-

import datetime

from past import config
from past.utils.escape import json_decode

## User数据接口 
class AbsUserData(object):

    def __init__(self, data):
        if data:
            self.data = data
        else:
            self.data = {}
        if isinstance(data, basestring):
            self.data = json_decode(data)

    def get_user_id(self):
        raise NotImplementedError

    def get_uid(self):
        raise NotImplementedError

    def get_nickname(self):
        return ""

    def get_intro(self):
        return ""

    def get_signature(self):
        return ""

    def get_avatar(self):
        return ""

    def get_icon(self):
        return ""
    
    def get_email(self):
        return ""

## 豆瓣user数据接口
class DoubanUser(AbsUserData):
    def __init__(self, data):
        super(DoubanUser, self).__init__(data)

    def get_user_id(self):
        id_ = self.data.get("id", {}).get("$t")
        if id_:
            return (id_.rstrip("/").split("/"))[-1]
        return None

    def get_uid(self):
        return self.data.get("uid", {}).get("$t")

    def get_nickname(self):
        return self.data.get("title", {}).get("$t")

    def get_intro(self):
        return self.data.get("content", {}).get("$t")

    def get_signature(self):
        return self.data.get("signature", {}).get("$t")

    def get_avatar(self):
        icon = self.get_icon()
        user_id = self.get_user_id()

        return icon.replace(user_id, "l%s" % user_id)

    def get_icon(self):
        links = {}
        _links = self.data.get("link", [])
        for x in _links:
            rel = x.get("@rel")
            links[rel] = x.get("@href")
        return links.get("icon", "")

## 豆瓣user2数据接口
class DoubanUser2(AbsUserData):
    def __init__(self, data):
        super(DoubanUser2, self).__init__(data)

    def get_user_id(self):
        return self.data.get("id")

    def get_uid(self):
        return self.data.get("uid")

    def get_nickname(self):
        return self.data.get("screen_name")

    def get_intro(self):
        return self.data.get("description")

    def get_signature(self):
        return ""

    def get_avatar(self):
        return self.data.get("large_avatar")

    def get_icon(self):
        return self.data.get("small_avatar")

## 新浪微博user数据接口
class SinaWeiboUser(AbsUserData):

    def __init__(self, data):
        super(SinaWeiboUser, self).__init__(data)

    def get_user_id(self):
        return self.data.get("idstr","")

    def get_uid(self):
        return self.data.get("domain", "")

    def get_nickname(self):
        return self.data.get("screen_name", "")

    def get_intro(self):
        return self.data.get("description", "")

    def get_signature(self):
        return ""

    def get_avatar(self):
        return self.data.get("avatar_large", "")

    def get_icon(self):
        return self.data.get("profile_image_url", "")

    def get_email(self):
        return ""

## Twitter user数据接口
class TwitterUser(AbsUserData):

    def __init__(self, data):
        super(TwitterUser, self).__init__(data)

    def get_user_id(self):
        return self.data.get("id_str","")

    def get_uid(self):
        return self.data.get("name", "")

    def get_nickname(self):
        return self.data.get("screen_name", "")

    def get_intro(self):
        return self.data.get("description", "")

    def get_signature(self):
        return ""

    def get_avatar(self):
        return self.data.get("profile_image_url", "")

    def get_icon(self):
        return self.data.get("profile_image_url", "")

    def get_email(self):
        return ""

## qq weibo user 数据接口
class QQWeiboUser(AbsUserData):

    def __init__(self, data):
        super(QQWeiboUser, self).__init__(data)

    def get_user_id(self):
        return self.data.get("openid","")

    def get_uid(self):
        return self.data.get("name", "")

    def get_nickname(self):
        return self.data.get("nick", "")

    def get_intro(self):
        return self.data.get("introduction", "")

    def get_signature(self):
        return ""

    def get_avatar(self):
        r = self.data.get("head", "")
        if r:
            return r + "/100"
        return r

    def get_icon(self):
        r = self.data.get("head", "")
        if r:
            return r + "/40"
        return r

    def get_email(self):
        return self.data.get("email", "")

    def get_birthday(self):
        return "%s-%s-%s" % (self.data.get("birth_year", ""),
            self.data.get("birth_month", ""), self.data.get("birth_day"))

## 第三方数据接口
class AbsData(object):
    
    def __init__(self, site, category, data):
        self.site = site
        self.category = category
        self.data = data or {}
        if isinstance(data, basestring):
            try:
                self.data = json_decode(data)
            except Exception, e:
                import traceback; print traceback.format_exc()
                self.data = {}

    ## 注释以微博为例
    ##原始的数据，json_decode之后的
    def get_data(self):
        return self.data
    
    ##原微博的id
    def get_origin_id(self):
        raise NotImplementedError
    
    ##原微博的创建时间
    def get_create_time(self):
        raise NotImplementedError
    
    ##如果有title的话，比如豆瓣广播
    def get_title(self):
        return ""

    ##原微博的内容
    def get_content(self):
        return ""

    ##原微博本身是个转发，获取被转发的内容
    def get_retweeted_data(self):
        return None

    ##原微博附带的图片，返回结果为list
    def get_images(self):
        return []
    
    ##原微博的作者，如果能获取到的话
    ##XXX
    def get_user(self):
        return None

    ##原微博的uri，可以点过去查看（有可能获取不到或者很麻烦，比如sina就很变态）
    ###XXX
    def get_origin_uri(self):
        return ""

class DoubanData(AbsData):
    
    def __init__(self, category, data):
        super(DoubanData, self).__init__( 
                config.OPENID_TYPE_DICT[config.OPENID_DOUBAN], category, data)

# 日记
class DoubanNoteData(DoubanData):
    def __init__(self, data):
        super(DoubanNoteData, self).__init__(
                config.CATE_DOUBAN_NOTE, data)

    def get_origin_id(self):
        id_ = self.data.get("id", {}).get("$t")
        if id_:
            return (id_.rstrip("/").split("/"))[-1]
        return None

    def get_create_time(self):
        return self.data.get("published",{}).get("$t")

    def get_title(self):
        return self.data.get("title", {}).get("$t")

    def get_content(self):
        return self.data.get("content", {}).get("$t")

# 广播
class DoubanMiniBlogData(DoubanData):
    def __init__(self, data):
        super(DoubanMiniBlogData, self).__init__(
                config.CATE_DOUBAN_MINIBLOG, data)

    def get_origin_id(self):
        id_ = self.data.get("id", {}).get("$t")
        if id_:
            return (id_.rstrip("/").split("/"))[-1]
        return None

    def get_create_time(self):
        return self.data.get("published",{}).get("$t")

    def get_title(self):
        return self.data.get("title", {}).get("$t")

    def get_content(self):
        return self.data.get("content", {}).get("$t")
    
    def _get_links(self):
        links = {}
        _links = self.data.get("link", [])
        for x in _links:
            rel = x.get("@rel")
            links[rel] = x.get("@href", "").replace("/spic", "/lpic")
        return links

    def get_images(self):
        links = self._get_links()
        if links and links.get("image"):
            return [links.get("image")]
        return []

# 豆瓣新广播（豆瓣说）
class DoubanStatusData(DoubanData):
    def __init__(self, data):
        super(DoubanStatusData, self).__init__(
            config.CATE_DOUBAN_STATUS, data)

    def get_origin_id(self):
        return str(self.data.get("id", ""))

    def get_create_time(self):
        return self.data.get("created_at")

    def get_content(self):
        return self.data.get("text", "")

    def get_retweeted_data(self):
        r = self.data.get("reshared_status")
        if r:
            return DoubanStatusData(r)
        else:
            return None

    def get_images(self):
        o = []
        atts = self.get_attachments()
        for att in atts:
            medias = att and att.get_medias()
            for x in medias:
                if x and x.get_type() == 'image':
                    o.append(x.get_src())   
        return o

    def get_user(self):
        r = self.data.get("user")
        if r:
            return DoubanUser2(r)
        else:
            return None

    def get_origin_uri(self):
        u = self.get_user()
        if u:
            uid = u.get_uid()
            return config.DOUBAN_STATUS % (uid, self.get_origin_id())

    ### 特有的方法：
    def get_target_type(self):
        return self.data.get("target_type")

    def get_attachments(self):
        rs = self.data.get("attachments", [])
        return [_Attachment(r) for r in rs]

class _Attachment(object):
    def __init__(self, data):
        self.data = data or {}

    def get_description(self):
        return self.data.get("description")
    def get_title(self):
        return self.data.get("title")
    def get_href(self):
        return self.data.get("expaned_href") or self.data.get("href")
    def get_medias(self):
        rs = self.data.get("media", [])
        return [_Media(x) for x in rs]


class _Media(object):
    def __init__(self, data):
        self.data = data or {}

    def get_type(self):
        return self.data.get("type")
    def get_src(self):
        return self.data.get("original_src", "").replace("/spic/", "/lpic/")
    
class SinaWeiboData(AbsData):
    
    def __init__(self, category, data):
        super(SinaWeiboData, self).__init__( 
                config.OPENID_TYPE_DICT[config.OPENID_SINA], category, data)

# 新浪微博status
class SinaWeiboStatusData(SinaWeiboData):
    def __init__(self, data):
        super(SinaWeiboStatusData, self).__init__(
                config.CATE_SINA_STATUS, data)
    
    def get_origin_id(self):
        return self.data.get("idstr", "")

    def get_create_time(self):
        t = self.data.get("created_at", "")
        return datetime.datetime.strptime(t, "%a %b %d %H:%M:%S +0800 %Y")

    def get_title(self):
        return ""

    def get_content(self):
        return self.data.get("text", "") 
    
    def get_retweeted_data(self):
        re = self.data.get("retweeted_status")
        if re:
            return SinaWeiboStatusData(re)

    def get_user(self):
        return SinaWeiboUser(self.data.get("user"))

    def get_origin_pic(self):
        return self.data.get("original_pic", "")

    def get_thumbnail_pic(self):
        return self.data.get("thumbnail_pic", "")

    def get_middle_pic(self):
        return self.data.get("bmiddle_pic", "")

    def get_images(self, size="middle"):
        method = "get_%s_pic" % size
        if hasattr(self, method):
            i = getattr(self, method)()
            if i:
                return [i]
        return []
        

# twitter status
class TwitterStatusData(AbsData):
    def __init__(self, data):
        super(TwitterStatusData, self).__init__(
                config.OPENID_TYPE_DICT[config.OPENID_TWITTER], 
                config.CATE_TWITTER_STATUS, data)
    
    def get_origin_id(self):
        return str(self.data.get("id", ""))

    def get_create_time(self):
        t = self.data.get("created_at", "")
        return datetime.datetime.strptime(t, "%a %b %d %H:%M:%S +0000 %Y")

    def get_title(self):
        return ""

    def get_content(self):
        return self.data.get("text", "") 
    
    def get_retweeted_data(self):
        return None

    def get_user(self):
        return TwitterUser(self.data.get("user"))

    def get_origin_uri(self):
        u = self.get_user()
        if u:
            uid = u.get_user_id()
            status_id = self.get_origin_id()
            return config.TWITTER_STATUS % (uid, status_id)
        return None

# qqweibo status
class QQWeiboStatusData(AbsData):
    def __init__(self, data):
        super(QQWeiboStatusData, self).__init__(
                config.OPENID_TYPE_DICT[config.OPENID_QQ], 
                config.CATE_QQWEIBO_STATUS, data)
    
    def get_origin_id(self):
        return str(self.data.get("id", ""))

    def get_create_time(self):
        t = self.data.get("timestamp")
        if not t:
            return None
        t = float(t)
        return datetime.datetime.fromtimestamp(t)

    def get_title(self):
        return ""

    def get_content(self):
        return self.data.get("text", "") 
    
    def get_retweeted_data(self):
        return self.data.get("origtext", "") 

    def _get_images(self, size):
        r = []
        imgs = self.data.get("image")
        if imgs and imgs != "null" and isinstance(imgs, list):
            r = ["%s/%s" % (x, size) for x in imgs]
        return r
        
    def get_origin_pic(self):
        return self._get_images(size=2000)

    def get_thumbnail_pic(self):
        return self._get_images(size=160)

    def get_middle_pic(self):
        return self._get_images(size=460)

    def get_images(self, size="middle"):
        method = "get_%s_pic" % size
        if hasattr(self, method):
            return getattr(self, method)()
        return []

    def get_origin_uri(self):
        return self.data.get("fromurl")
