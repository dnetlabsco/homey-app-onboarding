from typing import Any, Never

from homey.homey import Homey


async def get_state(
    *,
    homey: Homey,
    query: dict[str, str],
    params: dict[str, str],
    body: dict[Never, Never],  # Homey.API sends an empty body for GET requests
) -> Any:
    device_id = query.get("device")

    device = await homey.devices.get_device(device_id)


    temperature = await device.get_capability_value(
        "measure_temperature"
    )

    humidity = await device.get_capability_value(
        "measure_humidity"
    )

    pressure = await device.get_capability_value(
        "measure_pressure"
    )

    mode = await device.get_capability_value(
        "mode"
    )


    return {
        "temperature": temperature,
        "humidity": humidity,
        "pressure": pressure,
        "mode": mode
    }

__all__ = [
    "get_weather"
]

async def add_something(
    *, homey: Homey, query: dict[str, str], params: dict[str, str], body: dict[str, Any]
) -> Any:
    return homey.app.add_something(body)


async def update_something(
    *, homey: Homey, query: dict[str, str], params: dict[str, str], body: dict[str, Any]
) -> Any:
    return homey.app.update_something(body)


async def delete_something(
    *,
    homey: Homey,
    query: dict[str, str],
    params: dict[str, str],
    body: dict[Never, Never],  # Homey.API sends an empty body for DELETE requests
) -> Any:
    return homey.app.delete_something(params["id"])


# Export these methods as endpoints
__all__ = ["get_state"]
