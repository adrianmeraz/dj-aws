import boto3
from botocore.exceptions import ClientError

from djaws.cloudformation.exceptions import CFError
from djaws import decorators as aws_decorators
from djaws.utils import ClientErrorResponse


def cf_session(*args, **kwargs):
    session = boto3.session.Session()
    return session.client('cloudformation', *args, **kwargs,)


@aws_decorators.wrap_and_reraise_cloudformation_errors
def describe_stacks(cf_client, stack_name):
    try:
        r_stack = cf_client.describe_stacks(StackName=stack_name)
    except ClientError as e:
        raise CFClientErrorResponse(e.response).to_cf_exception
    else:
        return r_stack


class CFClientErrorResponse(ClientErrorResponse):
    EXC_MAP = dict()

    @property
    def to_cf_exception(self):
        return self.EXC_MAP.get(self.exception_class, CFError)(self.__dict__)
