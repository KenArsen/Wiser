from rest_framework import serializers

from apps.driver.models import Driver


class DriverSerializers(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = (
            "id",
            "first_name",
            "last_name",
            "date_of_birth",
            "email",
            "ssn",
            "address",
            "city",
            "state",
            "zip_code",
            "phone_number",
            "emergency_phone",
            "second_driver",
            "lisense_number",
            "lisense_state",
            "type",
            "expiration_date",
        )
