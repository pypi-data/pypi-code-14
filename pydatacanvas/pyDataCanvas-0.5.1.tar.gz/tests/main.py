#!/usr/bin/env python
# -*- coding: utf-8 -*-
# screwjack生成的脚本

from datacanvas.new_runtime import BasicRuntime, DataCanvas
dc = DataCanvas(__name__)


@dc.basic_runtime(spec_json="spec.json")   ## 生命在调用自己的时候，走dc的basic_runtime进行装饰器执行
def my_module(rt, params, inputs, outputs):
    # TODO : Fill your code here
    print "Done"


if __name__ == "__main__":
    dc.run()
