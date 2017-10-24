# -*- coding: utf8 -*-

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
from aliyunsdkecs.request.v20140526 import StopInstanceRequest

# 创建 AcsClient 实例
client = AcsClient(
    "LTAIXqKiBuSVT2",
    "BdCLWIc5oM6DuEQaW8ZrNnLCT",
    "cn-hangzhou"
);

# 创建 request，并设置参数
request = DescribeInstancesRequest.DescribeInstancesRequest()
request.set_PageSize(10)

# 发起 API 请求并打印返回
response = client.do_action_with_exception(request)
print response