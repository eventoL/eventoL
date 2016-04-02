# encoding: UTF-8
import datetime


class Schedule(object):
    def __init__(self, rooms, activities):
        self.rooms = rooms
        self.activities = activities
        if self.activities:
            self.activities.sort()
            self.start_date = self.activities[0].start_date
            self.end_date = self.activities[-1].end_date
            self.total_minutes = int(
                ((self.end_date - self.start_date) + datetime.timedelta(hours=1)).total_seconds() / 60)
            self.size = self.total_minutes * 2
            self.reference_hours = self.calculate_reference_hours()
        self.load_template_data()

    def calculate_reference_hours(self):
        one_hour = datetime.timedelta(hours=1)
        first_hour = {'start': self.start_date, 'end': self.start_date + one_hour}
        first_hour['size'] = self.activity_size(first_hour['start'], first_hour['end'])
        hours = [first_hour]

        last_hour = hours[-1]['end']
        while last_hour.hour < self.end_date.hour:
            new_hour = {'start': last_hour, 'end': last_hour + one_hour}
            new_hour['size'] = self.activity_size(new_hour['start'], new_hour['end'])
            hours.append(new_hour)
            last_hour = new_hour['end']

        return hours

    def load_template_data(self):
        for room in self.rooms:
            room.activities = self.activities_for_room(room)

    def activities_for_room(self, room):
        room_activities = []
        date_anterior = self.start_date
        activities = [activity for activity in self.activities if activity.room == room]
        activities.sort()
        for activity in activities:
            if activity.start_date.time() > date_anterior.time():
                room_activities.append({'dummy': True, 'dummy_size': self.activity_size(date_anterior, activity.start_date)})
            activity.activity_size = self.activity_size(activity.start_date, activity.end_date)
            room_activities.append(activity)
            date_anterior = activity.end_date
        if activity.end_date.time() < self.end_date.time():
            room_activities.append({'dummy': True, 'dummy_size': self.activity_size(activity.end_date, self.end_date)})
        return room_activities

    def activity_size(self, start, end):
        minutes = int((end - start).total_seconds()) / 60
        return minutes * 100 / self.total_minutes
