import json
from uuid import uuid4

from django.db import models
from django_kafka.producer import producer


class BenchmarkTest(models.Model):
    SMALL_TEST = "small"
    MEDIUM_TEST = "medium"
    LARGE_TEST = "large"
    TEST_TYPE_CHOICES = [
        (SMALL_TEST, "Small Test"),
        (MEDIUM_TEST, "Medium Test"),
        (LARGE_TEST, "Large Test"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    test_type = models.CharField(
        max_length=10, choices=TEST_TYPE_CHOICES, default=SMALL_TEST
    )
    topic = models.CharField(max_length=255, default="init_benchmark_tests")
    init_consumer_at = models.DateTimeField(
        verbose_name="Quando a mensagem foi consumida", null=True, blank=True
    )
    ended_consumer_at = models.DateTimeField(
        verbose_name="Quando a mensagem foi processada", null=True, blank=True
    )
    is_finished = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def time_processing(self):
        if self.init_consumer_at and self.ended_consumer_at:
            return (self.ended_consumer_at - self.init_consumer_at).total_seconds()
        return None

    @property
    def full_init_consumer_at(self):
        if self.init_consumer_at:
            return self.init_consumer_at.strftime("%Y-%m-%d %H:%M:%S")
        return None

    @property
    def full_ended_consumer_at(self):
        if self.ended_consumer_at:
            return self.ended_consumer_at.strftime("%Y-%m-%d %H:%M:%S")
        return None

    def __str__(self):
        return self.test_type

    def producer_init_task(self):
        message = {
            "id": str(self.id),
            "test_type": self.test_type,
        }
        message_str = json.dumps(message)
        producer(topic=self.topic, message=message_str.encode("utf-8"))
