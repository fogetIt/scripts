# -*- coding: utf-8 -*-
# @Date:   2018-01-17 09:41:19
# @Last Modified time: 2018-01-17 09:41:29


class InstantiatedError(Exception):

    def __init__(self, err="This class can't be instantiated."):
        super(InstantiatedError, self).__init__(err)


class NoInstance(object):

    @staticmethod
    def __new__(cls, *args, **kwargs):
        raise InstantiatedError


class MongodbPipeline(BasePipeline):

    def __init__(self):
        self.logger = logger_facade(os.path.splitext((os.path.basename(__file__)))[0])
        import pymongo
        client = pymongo.MongoClient(
            "mongodb://%s:%d" % (
                str(Config.MONGODB_HOST),
                int(Config.MONGODB_PORT)
            )
        )
        self.__db = client[str(Config.ENGINE)]

    def save(self, result):
        key_id = result.get("key_id", None)
        if key_id:
            result["__timer__"] = int(time.time())
            self.__db[str(Config.SCRIPT)].update_one(
                {"key_id": key_id},
                {"$set": result},
                upsert=True
            )
            self.logger.info(json.dumps(result, ensure_ascii=False))
        else:
            self.logger.error(result)
            raise Exception("key_id is needed when p.put({'key_id':'xxx', ...})")


class PipelineProxy(object):

    def __init__(self):
        self.pipeline = None
        self.pipeline_factory()

    def pipeline_factory(self):
        self.pipeline = eval("{}Pipeline()".format(str(Config.PIPELINE)))

    def save(self, result):
        self.pipeline.save(result)
