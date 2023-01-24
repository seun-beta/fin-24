from django.core.files import File
from django.core.files.storage import FileSystemStorage

from rest_framework import serializers

from apps.incomes.models import Income, IncomeType
from apps.incomes.tasks import upload_image_task


class IncomeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeType
        exclude = ["created_at", "updated_at", "user", "pkid"]


class IncomeSerializer(serializers.ModelSerializer):

    image = serializers.FileField()
    income_type_name = serializers.CharField(source="income_type.name", read_only=True)

    class Meta:
        model = Income
        exclude = ["created_at", "updated_at", "user", "pkid"]

    def create(self, validated_data):

        image_file = validated_data.pop("image")
        storage = FileSystemStorage()
        image_file.name = storage.get_available_name(image_file.name)
        storage.save(image_file.name, File(image_file))

        income = Income.objects.create(**validated_data)
        upload_image_task.delay(
            path=storage.path(image_file.name),
            file_name=image_file.name,
            id=income.id,
        )
        return income
