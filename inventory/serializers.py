from datetime import datetime, timedelta
from rest_framework import serializers
from django.db.models import Avg, Sum
from inventory.models import Box, ConditionParameter


class BoxSerializer(serializers.ModelSerializer):
    """
    this is owner serializer and deserializer
    """
    def validate(self, data):
        length = data["length"] if data["length"] else self.instance.length
        breadth = data["breadth"] if data["breadth"] else self.instance.breadth
        height = data["height"] if data["height"] else self.instance.height
        area = length * breadth
        volume = length * breadth * height
        maximum_area_of_all_boxes = ConditionParameter.objects.get(
            name="maximum_area_of_all_boxes"
        ).value
        average_volume_of_user_boxes = ConditionParameter.objects.get(
            name="average_volume_of_user_boxes"
        ).value
        no_of_boxes_added_in_a_week = ConditionParameter.objects.get(
            name="no_of_boxes_added_in_a_week"
        ).value
        no_of_boxes_added_in_a_week_by_a_user = ConditionParameter.objects.get(
            name="no_of_boxes_added_in_a_week_by_a_user"
        ).value
        print(
            maximum_area_of_all_boxes,
            average_volume_of_user_boxes,
            no_of_boxes_added_in_a_week,
            no_of_boxes_added_in_a_week_by_a_user,
            area,
            volume
        )
        boxes = Box.objects.all()
        if boxes.count() > 0:
            current_area_sum_of_all_boxes = boxes.aggregate(Sum('area'))['area__sum']
            print(
                current_area_sum_of_all_boxes
            )
            expected_avg = (current_area_sum_of_all_boxes + area) / (boxes.count() + 1)
            # check maximum_area_of_all_boxes
            if expected_avg > maximum_area_of_all_boxes:
                error = "maximum area of all boxes should not exceed {}".format(
                    maximum_area_of_all_boxes
                )
                raise serializers.ValidationError(error)
            # check average_volume_of_user_boxes
            boxes_by_current_user = boxes.filter(created_by_id=data["created_by"])
            current_vulume_sum_of_user_boxes = boxes_by_current_user.aggregate(Sum('volume'))['volume__sum']
            expected_volume = (current_vulume_sum_of_user_boxes + volume) / (boxes_by_current_user.count() + 1)
            if expected_volume > average_volume_of_user_boxes:
                error = "average_volume_of_user_boxes should not exceed {}".format(
                    average_volume_of_user_boxes
                )
                raise serializers.ValidationError(error)
            # check no_of_boxes_added_in_a_week        
            today = datetime.now().date()
            start = datetime.combine(today - timedelta(days=today.weekday()), datetime.min.time())
            total_boxes_added_in_a_week = boxes.filter(created_at__gte=start).count()
            if total_boxes_added_in_a_week >= no_of_boxes_added_in_a_week:
                error = "no of boxes added in a week should not exceed {}".format(
                    no_of_boxes_added_in_a_week
                )
                raise serializers.ValidationError(error)
            # check no_of_boxes_added_in_a_week_by_a_user        
            total_boxes_added_in_a_week_by_a_user = boxes.filter(
                created_at__gte=start,
                created_by_id=data["created_by"]
            ).count()
            if total_boxes_added_in_a_week_by_a_user >= no_of_boxes_added_in_a_week_by_a_user:
                error = "no of boxes added in a week by a user should not exceed {}".format(
                    no_of_boxes_added_in_a_week_by_a_user
                )
                raise serializers.ValidationError(error)
        return data

    class Meta:
        model = Box
        fields = ('length', 'breadth', 'height', 'created_by')

class BoxGetSerializer(serializers.ModelSerializer):
    """
    this is getter serializer and deserializer
    """
    class Meta:
        model = Box
        fields = ('length', 'breadth', 'height', 'area', 'volume')

class BoxStaffGetSerializer(serializers.ModelSerializer):
    """
    this is staff serializer and deserializer
    """
    class Meta:
        model = Box
        fields = '__all__'