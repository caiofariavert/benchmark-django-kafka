import json
import logging

from confluent_kafka import Consumer, Message
from django.utils import timezone

from apps.main.models import BenchmarkTest
from apps.main.utils import large_task, medium_task, small_task

logger = logging.getLogger("django")


def init_benchmark_tests_consumer(consumer: Consumer, msg: Message):
    consumer_logic(consumer, msg)


def medium_benchmark_tests_consumer(consumer: Consumer, msg: Message):
    consumer_logic(consumer, msg)


def large_benchmark_tests_consumer(consumer: Consumer, msg: Message):
    consumer_logic(consumer, msg)


def consumer_logic(consumer: Consumer, msg: Message):
    init = timezone.now()
    data = json.loads(msg.value().decode())
    benchmark_id = data["id"]
    logger.info(
        f"Received benchmark test {benchmark_id} of type {data['test_type']} from Kafka!"
    )
    func_to_call = {
        "small": small_task,
        "medium": medium_task,
        "large": large_task,
    }
    test_type = data["test_type"]
    func = func_to_call.get(test_type)
    if func:
        func()
        benchmark = BenchmarkTest.objects.filter(id=benchmark_id)
        if benchmark:
            benchmark = benchmark.first()
            benchmark.init_consumer_at = init
            benchmark.ended_consumer_at = timezone.now()
            benchmark.is_finished = True
            benchmark.save()
    logger.info(f"Benchmark test {benchmark_id} of type {test_type} processed!")
