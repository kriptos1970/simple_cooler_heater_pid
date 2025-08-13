"""Constants for the PID Controller integration."""

DOMAIN = "simple_cooler_heater_pid"

CONF_NAME = "name"
DEFAULT_NAME = "Rpi Fan PID Controller"

CONF_SENSOR_ENTITY_ID = "sensor_entity_id"

CONF_INPUT_RANGE_MIN = "input_range_min"
CONF_INPUT_RANGE_MAX = "input_range_max"
CONF_OUTPUT_RANGE_MIN = "output_range_min"
CONF_OUTPUT_RANGE_MAX = "output_range_max"

DEFAULT_INPUT_RANGE_MIN = 20.0
DEFAULT_INPUT_RANGE_MAX = 100.0
DEFAULT_OUTPUT_RANGE_MIN = 20.0
DEFAULT_OUTPUT_RANGE_MAX = 100.0

#CONF_OUTPUT_ENTITY = "Fan Entity"
