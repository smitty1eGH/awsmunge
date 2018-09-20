import pytest

from awsmunge import awsret2dict,flatten_awsret
from data.ec2_describe_instances import x

def test_awsmunge():
    assert type(awsret2dict(x))==dict

def test_flatten_awsret():
    flatten_awsret(x)
