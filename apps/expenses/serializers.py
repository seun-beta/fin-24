from django.core.files import File
from django.core.files.storage import FileSystemStorage

from rest_framework import serializers

from apps.expenses.models import Expense, ExpenseType
from apps.expenses.tasks import upload_image_task


class ExpenseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseType
        exclude = ["created_at", "updated_at", "user", "pkid"]


class ExpenseSerializer(serializers.ModelSerializer):

    image = serializers.FileField()
    expense_type_name = serializers.CharField(
        source="expense_type.name", read_only=True
    )

    class Meta:
        model = Expense
        exclude = ["created_at", "updated_at", "user", "pkid"]

    def create(self, validated_data):

        image_file = validated_data.pop("image")
        storage = FileSystemStorage()
        image_file.name = storage.get_available_name(image_file.name)
        storage.save(image_file.name, File(image_file))

        expense = Expense.objects.create(**validated_data)
        upload_image_task.delay(
            path=storage.path(image_file.name),
            file_name=image_file.name,
            id=expense.id,
        )
        return expense
