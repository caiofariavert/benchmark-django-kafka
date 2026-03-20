# -*- coding: utf-8 -*-
import logging
from time import sleep

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.main.models import BenchmarkTest

logger = logging.getLogger("django")


class Command(BaseCommand):
    help = "Generate initial groups with permissions"

    def handle(self, *args, **options):
        init = timezone.now()
        quantity_small = 10
        quantity_medium = 5
        quantity_large = 2
        total_testes = quantity_small + quantity_medium + quantity_large
        logger.info(f"Generating {total_testes} benchmark tests...")
        benchmarks = []
        now = timezone.now()
        for i in range(quantity_small):
            benchmark = BenchmarkTest()
            benchmark.test_type = BenchmarkTest.SMALL_TEST
            benchmark.created_at = now
            benchmark.save()
            benchmarks.append(benchmark)
        for i in range(quantity_medium):
            benchmark = BenchmarkTest()
            benchmark.test_type = BenchmarkTest.MEDIUM_TEST
            benchmark.created_at = now
            benchmark.save()
            benchmarks.append(benchmark)
        for i in range(quantity_large):
            benchmark = BenchmarkTest()
            benchmark.test_type = BenchmarkTest.LARGE_TEST
            benchmark.created_at = now
            benchmark.save()
            benchmarks.append(benchmark)
        logger.info(f"Created {total_testes} benchmark tests successfully!")
        logger.info("Sending messages to Kafka...")
        for benchmark in benchmarks:
            benchmark.producer_init_task()
        logger.info("Messages sent to Kafka successfully!")
        while total_testes > 0:
            benchmark: BenchmarkTest
            for benchmark in benchmarks:
                benchmark.refresh_from_db()
                if benchmark.is_finished:
                    total_testes -= 1
                    benchmarks.remove(benchmark)
                    logger.info(
                        f"Benchmark test {benchmark.id} finished! Remaining: {total_testes}"
                    )
            sleep(5)
        ended = timezone.now()
        time_taken = (ended - init).total_seconds()
        logger.info(
            "All benchmark tests finished successfully in {} seconds!".format(
                time_taken
            )
        )
