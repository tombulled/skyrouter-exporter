import os
import typing

import fastapi
import fastapi.responses
import prometheus_client
import skyrouter
import skyrouter.models

HOST: typing.Optional[str] = os.getenv("HOST")
USERNAME: typing.Optional[str] = os.getenv("USERNAME")
PASSWORD: typing.Optional[str] = os.getenv("PASSWORD")

router: skyrouter.SkyRouter = skyrouter.SkyRouter(
    host=HOST, username=USERNAME, password=PASSWORD
)

registry: prometheus_client.CollectorRegistry = prometheus_client.CollectorRegistry()

metrics: typing.Dict[str, str] = dict(
    transmitted_packets="Total number of transmitted packets since last boot",
    received_packets="Total number of received packets since last boot",
    transmitted_bytes_per_second="Total number of bytes transmitted per second",
    received_bytes_per_second="Total number of bytes received per second",
    collision_packets="Total number of packet collisions",
)

gauges: typing.Dict[str, prometheus_client.Gauge] = {
    name: prometheus_client.Gauge(
        name=name,
        documentation=documentation,
        labelnames=("port",),
        registry=registry,
    )
    for name, documentation in metrics.items()
}


def update_metrics() -> None:
    statistics: skyrouter.models.RouterStatistics
    for statistics in router.system():
        metric: str
        gauge: prometheus_client.Gauge
        for metric, gauge in gauges.items():
            gauge.labels(port=statistics.port).set(getattr(statistics, metric))


app: fastapi.FastAPI = fastapi.FastAPI(
    default_response_class=fastapi.responses.PlainTextResponse
)


@app.get("/")
async def index() -> str:
    update_metrics()

    return prometheus_client.generate_latest(registry)
