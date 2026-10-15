# Source Generated with Decompyle++
# File: CustomFilesCache.pyc (Python 2.6)

import os
import time
import base64
import urllib2
import cPickle
import BigWorld
import binascii
import threading
import BigWorld
from debug_utils import *
from functools import partial
from helpers import getClientVersion
from Queue import Queue
import shelve as provider
import random
_MIN_LIFE_TIME = 15 * 60
_MAX_LIFE_TIME = 24 * 60 * 60
_LIFE_TIME_IN_MEMORY = 20 * 60
_CACHE_VERSION = 2
_CLIENT_VERSION = getClientVersion()

def _LOG_EXECUTING_TIME(startTime, methodName, deltaTime = 0.1):
    finishTime = time.time()
    if finishTime - startTime > deltaTime:
        LOG_WARNING('Method "%s" takes too much time %s' % (methodName, finishTime - startTime))
    


def parseHttpTime(t):
    if t is None:
        return None
    if type(t) == int:
        return t
    if type(t) == str:
        
        try:
            parts = t.split()
            weekdays = [
                'mon',
                'tue',
                'wed',
                'thu',
                'fri',
                'sat',
                'sun']
            months = [
                'jan',
                'feb',
                'mar',
                'apr',
                'may',
                'jun',
                'jul',
                'aug',
                'sep',
                'oct',
                'nov',
                'dec']
            tm_wday = weekdays.index(parts[0][:3].lower())
            tm_day = int(parts[1])
            tm_month = months.index(parts[2].lower()) + 1
            tm_year = int(parts[3])
            tm = parts[4].split(':')
            tm_hour = int(tm[0])
            tm_min = int(tm[1])
            tm_sec = int(tm[2])
            t = int(time.mktime((tm_year, tm_month, tm_day, tm_hour, tm_min, tm_sec, tm_wday, 0, -1)))
        except Exception:
            type(t) == int
            e = t is None
            LOG_ERROR(e, t)
            t = None
        

    return t


def makeHttpTime(dt):
    
    try:
        weekday = [
            'Mon',
            'Tue',
            'Wed',
            'Thu',
            'Fri',
            'Sat',
            'Sun'][dt.tm_wday]
        month = [
            'Jan',
            'Feb',
            'Mar',
            'Apr',
            'May',
            'Jun',
            'Jul',
            'Aug',
            'Sep',
            'Oct',
            'Nov',
            'Dec'][dt.tm_mon - 1]
        t = '%s, %02d %s %04d %02d:%02d:%02d GMT' % (weekday, dt.tm_mday, month, dt.tm_year, dt.tm_hour, dt.tm_min, dt.tm_sec)
    except Exception:
        e = None
        LOG_ERROR(e, dt)
        t = None

    return t


def getSafeDstUTCTime():
    t = time.gmtime()
    return int(time.mktime((t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec, t.tm_wday, 0, -1)))


class NotModifiedHandler(urllib2.BaseHandler):
    
    def http_error_304(self, req, fp, code, message, headers):
        addinfourl = urllib2.addinfourl(fp, headers, req.get_full_url())
        addinfourl.code = code
        return addinfourl



class CFC_OP_TYPE:
    DOWNLOAD = 1
    READ = 2
    WRITE = 3
    CHECK = 4


class WorkerThread(threading.Thread):
    
    def __init__(self):
        super(WorkerThread, self).__init__()
        self.input_queue = Queue(60)
        self._WorkerThread__terminate = False
        self.isBusy = False

    
    def add_task(self, task):
        callback = task['callback']
        
        try:
            self.input_queue.put(task, block = False)
        except:
            callback(None, None, None)


    
    def close(self):
        self.isBusy = False
        self._WorkerThread__terminate = True
        self.input_queue.put(None)

    
    def run(self):
        while True:
            task = self.input_queue.get()
            if task is None:
                break
            
            if self._WorkerThread__terminate:
                break
            
            
            try:
                self.isBusy = True
                type = task['opType']
                if type == CFC_OP_TYPE.DOWNLOAD:
                    self._WorkerThread__run_download(**None)
                elif type == CFC_OP_TYPE.READ:
                    self._WorkerThread__run_read(**None)
                elif type == CFC_OP_TYPE.WRITE:
                    self._WorkerThread__run_write(**None)
                elif type == CFC_OP_TYPE.CHECK:
                    self._WorkerThread__run_check(**None)
            except:
                LOG_CURRENT_EXCEPTION()

            self.isBusy = False
            self.input_queue.task_done()
        self.input_queue.task_done()

    
    def _WorkerThread__run_download(self, url, modified_time, callback, **params):
        startTime = time.time()
        
        try:
            fh = None
            file = None
            last_modified = None
            expires = None
            req = urllib2.Request(url)
            req.add_header('User-Agent', _CLIENT_VERSION)
            if modified_time and type(modified_time) == str:
                req.add_header('If-Modified-Since', modified_time)
                opener = urllib2.build_opener(NotModifiedHandler())
                fh = opener.open(req, timeout = 10)
                headers = fh.info()
                if hasattr(fh, 'code'):
                    code = fh.code
                    if code in (304, 200):
                        info = fh.info()
                        last_modified = info.getheader('Last-Modified')
                        expires = info.getheader('Expires')
                    
                    if code == 200:
                        file = fh.read()
                    
                
            else:
                opener = urllib2.build_opener(urllib2.BaseHandler())
                fh = opener.open(req, timeout = 10)
                info = fh.info()
                last_modified = info.getheader('Last-Modified')
                expires = info.getheader('Expires')
                file = fh.read()
            if expires is None:
                expires = makeHttpTime(time.gmtime())
            else:
                ctime = getSafeDstUTCTime()
                expiresTmp = parseHttpTime(expires)
                if expiresTmp > ctime + _MAX_LIFE_TIME or expiresTmp < ctime:
                    expires = makeHttpTime(time.gmtime(time.time() + _MAX_LIFE_TIME))
        except urllib2.HTTPError:
            e = None
            LOG_WARNING('Http error. Code: %d, url: %s' % (e.code, url))
        except urllib2.URLError:
            e = None
            LOG_WARNING('Url error. Reason: %s, url: %s' % (str(e.reason), url))
        except Exception:
            e = None
            LOG_ERROR("Client couldn't download file.", e, url)
        finally:
            if fh:
                fh.close()
            

        _LOG_EXECUTING_TIME(startTime, '__run_download', 10)
        callback(file, last_modified, expires)

    
    def _WorkerThread__run_read(self, name, db, callback, **params):
        file = None
        
        try:
            startTime = time.time()
            if db is not None and db.has_key(name):
                file = db[name]
            
            _LOG_EXECUTING_TIME(startTime, '__run_read')
        except Exception:
            e = None
            LOG_ERROR("Client couldn't read file.", e, name)

        callback(file, None, None)

    
    def _WorkerThread__run_write(self, name, data, db, callback, **params):
        
        try:
            startTime = time.time()
            if db is not None:
                db[name] = data
                if len(db.cache) > 20:
                    db.sync()
                
            
            _LOG_EXECUTING_TIME(startTime, '__run_write', 5)
        except:
            LOG_CURRENT_EXCEPTION()

        callback(None, None, None)

    
    def _WorkerThread__run_check(self, name, db, callback, **params):
        res = False
        
        try:
            startTime = time.time()
            if db is not None:
                res = db.has_key(name)
            
            _LOG_EXECUTING_TIME(startTime, '__run_check')
        except:
            LOG_CURRENT_EXCEPTION()

        callback(res, None, None)



class ThreadPool:
    
    def __init__(self, num = 8):
        num = max(2, num)
        self._ThreadPool__workers = []
        for i in range(num):
            self._ThreadPool__workers.append(WorkerThread())
        

    
    def start(self):
        for w in self._ThreadPool__workers:
            w.start()
        

    
    def close(self):
        for w in self._ThreadPool__workers:
            w.close()
        
        self._ThreadPool__workers = []

    
    def add_task(self, task):
        if len(self._ThreadPool__workers) == 0:
            return None
        type = task['opType']
        if type in (CFC_OP_TYPE.WRITE, CFC_OP_TYPE.READ, CFC_OP_TYPE.CHECK):
            self._ThreadPool__workers[0].add_task(task)
        else:
            workers = self._ThreadPool__workers[1:]
            for w in workers:
                if w.isBusy:
                    continue
                
                w.add_task(task)
                return None
            
            w = random.choice(workers)
            w.add_task(task)



class CustomFilesCache(object):
    
    def __init__(self):
        prefsFilePath = unicode(BigWorld.wg_getPreferencesFilePath(), 'utf-8', errors = 'ignore')
        self._CustomFilesCache__cacheDir = os.path.join(os.path.dirname(prefsFilePath), 'custom_data')
        self._CustomFilesCache__cacheDir = os.path.normpath(self._CustomFilesCache__cacheDir)
        self._CustomFilesCache__mutex = threading.RLock()
        self._CustomFilesCache__cache = { }
        self._CustomFilesCache__accessedCache = { }
        self._CustomFilesCache__processedCache = { }
        self._CustomFilesCache__written_cache = set()
        self._CustomFilesCache__db = None
        self._CustomFilesCache__prepareCache()
        self._CustomFilesCache__worker = ThreadPool()
        self._CustomFilesCache__worker.start()
        self._CustomFilesCache__startTimer()

    
    def close(self):
        self._CustomFilesCache__worker.close()
        self._CustomFilesCache__processedCache = { }
        if self._CustomFilesCache__db is not None:
            startTime = time.time()
            
            try:
                self._CustomFilesCache__db.close()
            except:
                LOG_CURRENT_EXCEPTION()

            _LOG_EXECUTING_TIME(startTime, 'close')
            self._CustomFilesCache__db = None
        

    
    def _CustomFilesCache__startTimer(self):
        self._CustomFilesCache__timer = BigWorld.callback(60, self._CustomFilesCache__idle)

    
    def get(self, url, callback, showImmediately = False):
        if callback is None:
            return None
        startDownload = True
        if url in self._CustomFilesCache__processedCache:
            startDownload = False
        
        self._CustomFilesCache__processedCache.setdefault(url, []).append(callback)
        if startDownload:
            self._CustomFilesCache__get(url, showImmediately, False)
        

    
    def _CustomFilesCache__get(self, url, showImmediately, checkedInCache):
        
        try:
            ctime = getSafeDstUTCTime()
            hash = base64.b32encode(url)
            self._CustomFilesCache__mutex.acquire()
            cache = self._CustomFilesCache__cache
            if hash in cache:
                data = cache[hash]
                if data is None:
                    LOG_DEBUG('readLocalFile, there is no file in memory.', url)
                    self._CustomFilesCache__readLocalFile(url, showImmediately)
                else:
                    self._CustomFilesCache__accessedCache[hash] = ctime
                    (expires, creation_time, _, file, _, last_modified) = data
                    expires = parseHttpTime(expires)
                    if expires is None:
                        LOG_ERROR('Unable to parse expires time.', url)
                        self._CustomFilesCache__postTask(url, None, True)
                        return None
                    if ctime - _MIN_LIFE_TIME <= expires:
                        pass
                    expires <= ctime + _MAX_LIFE_TIME + _MIN_LIFE_TIME
                    if 1:
                        LOG_DEBUG('postTask, Sends file to requester.', url, last_modified, data[0])
                        self._CustomFilesCache__postTask(url, file, True)
                    elif showImmediately:
                        LOG_DEBUG('postTask, Do not release callbacks. Sends file to requester.', url, last_modified, data[0])
                        self._CustomFilesCache__postTask(url, file, False)
                    
                    LOG_DEBUG('readRemoteFile, there is file in cache, check last_modified field.', url, last_modified, data[0])
                    self._CustomFilesCache__readRemoteFile(url, last_modified, showImmediately)
            elif checkedInCache:
                LOG_DEBUG('readRemoteFile, there is no file in cache.', url)
                self._CustomFilesCache__readRemoteFile(url, None, False)
            else:
                LOG_DEBUG('checkFile. Checking file in cache.', url, showImmediately)
                self._CustomFilesCache__checkFile(url, showImmediately)
        finally:
            self._CustomFilesCache__mutex.release()


    
    def _CustomFilesCache__idle(self):
        
        try:
            self._CustomFilesCache__mutex.acquire()
            cache = self._CustomFilesCache__cache
            accessed_cache = self._CustomFilesCache__accessedCache
            ctime = getSafeDstUTCTime()
            for (k, v) in accessed_cache.items():
                if v and abs(ctime - v) >= _LIFE_TIME_IN_MEMORY:
                    cache[k] = None
                    accessed_cache.pop(k, None)
                    LOG_DEBUG('Idle. Removing old file from memory.', k)
                    continue
        finally:
            self._CustomFilesCache__mutex.release()

        self._CustomFilesCache__startTimer()

    
    def _CustomFilesCache__readLocalFile(self, url, showImmediately):
        task = {
            'opType': CFC_OP_TYPE.READ,
            'db': self._CustomFilesCache__db,
            'name': base64.b32encode(url),
            'callback': partial(self._CustomFilesCache__onReadLocalFile, url, showImmediately) }
        self._CustomFilesCache__worker.add_task(task)

    
    def _CustomFilesCache__onReadLocalFile(self, url, showImmediately, file, d1, d2):
        data = file
        
        try:
            (crc, f, ver) = data[2:5]
            if crc != binascii.crc32(f) or _CACHE_VERSION != ver:
                LOG_DEBUG('Old file was found.', url)
                raise Exception, 'Invalid data.'
            _CACHE_VERSION != ver
        except:
            data = None

        
        try:
            hash = base64.b32encode(url)
            self._CustomFilesCache__mutex.acquire()
            cache = self._CustomFilesCache__cache
            if data is not None:
                cache[hash] = data
            else:
                cache.pop(hash, None)
                self._CustomFilesCache__accessedCache.pop(hash, None)
        finally:
            self._CustomFilesCache__mutex.release()

        self._CustomFilesCache__get(url, showImmediately, True)

    
    def _CustomFilesCache__checkFile(self, url, showImmediately):
        task = {
            'opType': CFC_OP_TYPE.CHECK,
            'db': self._CustomFilesCache__db,
            'name': base64.b32encode(url),
            'callback': partial(self._CustomFilesCache__onCheckFile, url, showImmediately) }
        self._CustomFilesCache__worker.add_task(task)

    
    def _CustomFilesCache__onCheckFile(self, url, showImmediately, res, d1, d2):
        if res is None:
            self._CustomFilesCache__postTask(url, None, True)
            return None
        if res:
            
            try:
                hash = base64.b32encode(url)
                self._CustomFilesCache__mutex.acquire()
                self._CustomFilesCache__cache[hash] = None
            finally:
                self._CustomFilesCache__mutex.release()

        
        self._CustomFilesCache__get(url, showImmediately, True)

    
    def _CustomFilesCache__readRemoteFile(self, url, modified_time, showImmediately):
        task = {
            'opType': CFC_OP_TYPE.DOWNLOAD,
            'url': url,
            'modified_time': modified_time,
            'callback': partial(self._CustomFilesCache__onReadRemoteFile, url, showImmediately) }
        self._CustomFilesCache__worker.add_task(task)

    
    def _CustomFilesCache__onReadRemoteFile(self, url, showImmediately, file, last_modified, expires):
        if file is None and last_modified is None:
            if showImmediately:
                LOG_DEBUG('__onReadRemoteFile, Error occurred. Release callbacks.', url)
                self._CustomFilesCache__processedCache.pop(url, None)
            else:
                self._CustomFilesCache__postTask(url, None, True)
            return None
        hash = base64.b32encode(url)
        ctime = getSafeDstUTCTime()
        fileChanged = False
        
        try:
            self._CustomFilesCache__mutex.acquire()
            cache = self._CustomFilesCache__cache
            if file is None and last_modified is not None:
                value = cache.get(hash, None)
                if value is None:
                    LOG_WARNING('File is expected in cache, but there is no file')
                    self._CustomFilesCache__postTask(url, None, True)
                    return None
                (crc, file) = value[2:4]
            else:
                crc = binascii.crc32(file)
                fileChanged = True
            packet = (expires, ctime, crc, file, _CACHE_VERSION, last_modified)
            cache[hash] = packet
        finally:
            self._CustomFilesCache__mutex.release()

        LOG_DEBUG('writeCache', url, last_modified, expires)
        self._CustomFilesCache__writeCache(hash, packet)
        if showImmediately and not fileChanged:
            LOG_DEBUG('__onReadRemoteFile, showImmediately = True. Release callbacks.', url)
            self._CustomFilesCache__processedCache.pop(url, None)
        else:
            self._CustomFilesCache__get(url, False, True)

    
    def _CustomFilesCache__prepareCache(self):
        
        try:
            cacheDir = self._CustomFilesCache__cacheDir
            if not os.path.isdir(cacheDir):
                os.makedirs(cacheDir)
            
            filename = os.path.join(cacheDir, 'icons')
            self._CustomFilesCache__db = provider.open(filename, flag = 'c', writeback = True)
        except:
            LOG_CURRENT_EXCEPTION()


    
    def _CustomFilesCache__writeCache(self, name, packet):
        if name in self._CustomFilesCache__written_cache:
            return None
        self._CustomFilesCache__written_cache.add(name)
        task = {
            'opType': CFC_OP_TYPE.WRITE,
            'db': self._CustomFilesCache__db,
            'name': name,
            'data': packet,
            'callback': partial(self._CustomFilesCache__onWriteCache, name) }
        self._CustomFilesCache__worker.add_task(task)

    
    def _CustomFilesCache__onWriteCache(self, name, d1, d2, d3):
        self._CustomFilesCache__written_cache.discard(name)

    
    def _CustomFilesCache__postTask(self, url, file, invokeAndReleaseCallbacks):
        BigWorld.callback(0.001, partial(self._CustomFilesCache__onPostTask, url, invokeAndReleaseCallbacks, file))

    
    def _CustomFilesCache__onPostTask(self, url, invokeAndReleaseCallbacks, file):
        if invokeAndReleaseCallbacks:
            cbs = self._CustomFilesCache__processedCache.pop(url, [])
        else:
            cbs = self._CustomFilesCache__processedCache.get(url, [])
        for cb in cbs:
            cb(url, file)
        



